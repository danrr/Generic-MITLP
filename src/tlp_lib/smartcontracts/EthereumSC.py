import functools
from logging import getLogger
from pathlib import Path
from typing import Literal, Optional, Self

from eth_tester import EthereumTester, PyEVMBackend
from eth_typing import ChecksumAddress
from solcx import compile_files, install_solc  # pyright: ignore[reportUnknownVariableType]
from web3 import EthereumTesterProvider, Web3
from web3.contract import Contract  # pyright: ignore[reportPrivateImportUsage]
from web3.contract.contract import ContractFunction, HexBytes  # pyright: ignore[reportPrivateImportUsage]
from web3.types import TxParams, TxReceipt, Wei

from tlp_lib.protocols import GCTLP_Encrypted_Message, TLP_Digest, TLP_Digests
from tlp_lib.smartcontracts.protocols import SC_Coins, SC_ExtraTime, SC_Solution, SC_Solutions, SC_UpperBounds

SOLC_VERSION = "0.8.0"
CONTRACT_NAME = "SmartContract"
CONTRACT_PATH = str((Path(__file__) / "../../../contracts/SmartContract.sol").resolve())

logger = getLogger(__name__)


class EthereumSC:
    web3: Web3
    _account: Optional[ChecksumAddress]
    __contract: Optional[Contract] = None
    _contract_path: str

    def __init__(
        self, account: Optional[ChecksumAddress] = None, web3: Optional[Web3] = None, contract_path: str = CONTRACT_PATH
    ):
        logger.info("Initiating EthereumSC")
        self._initiate_network(web3)
        logger.info("Network initiated")
        self.account = account

        self._contract_path = contract_path

    # Public Properties #

    @property
    def commitments(self) -> TLP_Digests:
        return self._contract.functions.commitments().call()

    @commitments.setter
    def commitments(self, commitments: TLP_Digests):
        total_commitments = len(commitments)
        start_index = 0

        while start_index < total_commitments:
            end_index = min(start_index + self._SC_PUZZLE_BATCH_SIZE, total_commitments)

            # Create a slice for the current batch
            commitments_batch = commitments[start_index:end_index]

            # Call the setCommitments function for the current batch with the appropriate start index
            if not self._has_succeeded(self._contract.functions.setCommitments(commitments_batch, start_index)):
                raise RuntimeError(f"Commitments were not set correctly for batch starting at index {start_index}")

            # Update start index for the next batch
            start_index = end_index

    def get_commitment_at(self, i: int) -> TLP_Digest:
        return self._contract.functions.getCommitmentAt(i).call()

    @property
    def coins(self) -> SC_Coins:
        return self._contract.functions.coins().call()

    @property
    def upper_bounds(self) -> SC_UpperBounds:
        return self._contract.functions.upperBounds().call()

    def get_upper_bound_at(self, i: int) -> int:
        return self._contract.functions.getUpperBoundAt(i).call()

    @property
    def start_time(self) -> int:
        return self._contract.functions.startTime().call()

    @property  # pyright: ignore
    def solutions(self) -> SC_Solutions:
        res = self._contract.functions.solutions().call()

        return list(zip(res[0], res[1], res[2]))

    def get_solution_at(self, i: int) -> SC_Solution:
        return self._contract.functions.getSolutionAt(i).call()

    @property  # pyright: ignore[reportPropertyTypeMismatch]
    def initial_timestamp(self) -> int:
        return self._contract.functions.initialTimestamp().call()

    @property
    def account(self) -> ChecksumAddress:
        if self._account is None:
            raise RuntimeError("No Account set.  Please set an account to use the contract.")
        return self._account

    @account.setter
    def account(self, value: Optional[ChecksumAddress]):
        self._account = value

    # Public Methods #

    def initiate(
        self,
        coins: SC_Coins,
        start_time: int,
        extra_time: SC_ExtraTime,
        upper_bounds: SC_UpperBounds,
        helper_id: int | ChecksumAddress,
    ) -> Self:
        """
        Deploys the contract to the network and deposit the coins into the contract
        """

        abi, sc_bytecode = self._compile_contract()
        contract_address = self._deploy_contract(
            sc_bytecode, abi, coins, start_time, extra_time, upper_bounds, helper_id
        )
        logger.info("Deployed Contract Successfully: ", contract_address)
        return self

    def load_contract(self, contract_address: ChecksumAddress) -> None:
        abi, _ = self._compile_contract()
        self._contract = self.web3.eth.contract(address=contract_address, abi=abi)

    def switch_to_account(self, account_index: int) -> None:
        self.account = self.web3.eth.accounts[account_index]

    def add_solution(self, solution: GCTLP_Encrypted_Message, witness: TLP_Digest) -> None:
        if not self._has_succeeded(self._contract.functions.addSolution(solution, witness)):
            raise RuntimeError("Solution was not added correctly")

    def get_message_at(self, i: int) -> GCTLP_Encrypted_Message:
        return self._contract.functions.getSolutionAt(i).call()[0]

    def pay(self, i: int) -> None:
        if not self._has_succeeded(self._contract.functions.pay(i)):
            raise RuntimeError("Payout was not successful")

    def pay_back(self, i: int) -> None:
        if not self._has_succeeded(self._contract.functions.payBack(i)):
            raise RuntimeError("Payback was not successful")

    # Private Properties #

    @property
    def _contract(self) -> Contract:
        if self.__contract is None:
            raise RuntimeError("No Contract set.  Please load a contract or initiate it first.")
        return self.__contract

    @_contract.setter
    def _contract(self, value: Contract):
        self.__contract = value

    # Private Methods #

    _SC_PUZZLE_BATCH_SIZE: int = 300

    def _compile_contract(self) -> tuple[str, str]:
        """
        Loads in the ABI of the EDTLP contract
        """

        install_solc(SOLC_VERSION)

        compiled_sol: dict[str, dict[Literal["abi", "bin"], str]] = compile_files(
            [self._contract_path],
            output_values=["abi", "bin"],
            solc_version=SOLC_VERSION,
        )

        compiled_contract = compiled_sol[self._contract_path + ":" + CONTRACT_NAME]

        abi: Optional[str] = compiled_contract["abi"]
        bytecode: Optional[str] = compiled_contract["bin"]

        assert abi is not None
        assert bytecode is not None

        return abi, bytecode

    def _deploy_contract(
        self,
        bytecode: str,
        abi: str,
        coins: SC_Coins,
        start_time: int,
        extra_times: SC_ExtraTime,
        upper_bounds: SC_UpperBounds,
        helper_id: int | ChecksumAddress,
    ) -> Optional[ChecksumAddress]:
        """
        Deploys the contract to the network
        """
        ContractFactory = self.web3.eth.contract(abi=abi, bytecode=bytecode)

        contract = ContractFactory.constructor()

        tx_hash: HexBytes = contract.transact({"from": self.account})

        tx_receipt: TxReceipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

        self._contract = self.web3.eth.contract(
            address=tx_receipt["contractAddress"], abi=abi
        )  # pyright: ignore[reportAttributeAccessIssue]

        self._initialize_in_batches(coins, start_time, extra_times, upper_bounds, helper_id)

        return tx_receipt["contractAddress"]

    def _initialize_in_batches(
        self,
        coins: SC_Coins,
        start_time: int,
        extra_times: SC_ExtraTime,
        upper_bounds: SC_UpperBounds,
        helper_id: int | ChecksumAddress,
    ) -> None:
        # Ensure that all lists have the same length
        assert len(coins) == len(extra_times) == len(upper_bounds), "All input lists must have the same length"

        total_parts = len(coins)
        start_index = 0

        while start_index < total_parts:
            end_index = min(start_index + self._SC_PUZZLE_BATCH_SIZE, total_parts)

            # Create a slice for the current batch
            coins_batch = coins[start_index:end_index]
            extra_times_batch = extra_times[start_index:end_index]
            upper_bounds_batch = upper_bounds[start_index:end_index]

            # Calculate the value to send with this batch
            value_to_send = functools.reduce(lambda x, y: x + y, coins_batch)

            # Call the initialize function for the current batch
            if not self._has_succeeded(
                self._contract.functions.initialize(
                    coins_batch,
                    start_time,
                    list(map(int, extra_times_batch)),
                    list(map(int, upper_bounds_batch)),
                    helper_id,
                ),
                value_to_send,
            ):
                raise RuntimeError("Initialize has failed for batch starting at index {}".format(start_index))

            # Update start index for the next batch
            start_index = end_index

    def _initiate_network(self, web3: Optional[Web3] = None) -> None:
        """
        Initiates the network connection
        @:param provider: The provider to use for the connection
        If no provider is given, use the `EthereumTesterProvider` which runs a local testnet
        """
        #
        if web3 is None:
            provider = EthereumTesterProvider(ethereum_tester=EthereumTester(backend=PyEVMBackend()))
            web3 = Web3(provider)

        self.web3 = web3

        assert self.web3.is_connected()

    def _has_succeeded(self, tx: ContractFunction, value: int = 0) -> bool:
        props = TxParams({"from": self.account, "value": Wei(value)})

        tx_hash = tx.transact(props)
        return self.web3.eth.wait_for_transaction_receipt(tx_hash)["status"] == 1
