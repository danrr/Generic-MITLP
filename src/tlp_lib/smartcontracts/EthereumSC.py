import itertools
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

from tlp_lib.protocols import GCTLP_Encrypted_Message, GCTLP_Encrypted_Messages, GCTLPInterface, TLP_Digest, TLP_Digests
from tlp_lib.smartcontracts.protocols import SC_Coins, SC_UpperBounds

SOLC_VERSION = "0.8.0"
CONTRACT_NAME = "SmartContract"
CONTRACT_PATH = str((Path(__file__) / "../../../contracts/SmartContract.sol").resolve())

logger = getLogger(__name__)

type PuzzleIndex = int
type PuzzleDetailsSH = bytes
type PuzzleCommitmentSH = bytes
type PuzzleDetailsEvent = tuple[PuzzleIndex, SC_Coins, SC_UpperBounds, PuzzleDetailsSH]
type PuzzleCommitmentEvent = tuple[PuzzleIndex, GCTLP_Encrypted_Message, PuzzleCommitmentSH]
type PuzzleSolutionEvent = tuple[PuzzleIndex, GCTLP_Encrypted_Message, TLP_Digest]


class EthereumSC:
    web3: Web3
    _account: Optional[ChecksumAddress]
    __contract: Optional[Contract] = None
    _contract_path: str
    _backend: Optional[PyEVMBackend] = None
    _initialized_events: Optional[list[PuzzleDetailsEvent]] = None
    _set_commitment_events: Optional[list[PuzzleCommitmentEvent]] = None
    _received_solution_events: Optional[list[PuzzleSolutionEvent]] = None
    _sc_init_block: Optional[int] = None

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
        start_index = 0
        # Call the setCommitments function for the current batch with the appropriate start index
        if not self._has_succeeded(self._contract.functions.setCommitments(commitments)):
            raise RuntimeError(f"Commitments were not set correctly for batch starting at index {start_index}")

    def get_commitment_at(self, i: int) -> TLP_Digest:
        return self._contract.functions.getCommitmentAt(i).call()

    @property
    def coins(self) -> SC_Coins:
        if self._initialized_events is None:
            self._load_initialized_events()
        return [coins for (_, coins, _, _) in self._initialized_events]

    @property
    def upper_bounds(self) -> SC_UpperBounds:
        if self._initialized_events is None:
            self._load_initialized_events()
        return [upper_bounds for (_, _, upper_bounds, _) in self._initialized_events]

    def get_upper_bound_at(self, i: int) -> int:
        return self.upper_bounds[i]

    @property
    def start_time(self) -> int:
        return self._contract.functions.startTime().call()

    @property  # pyright: ignore
    def solutions(self) -> GCTLP_Encrypted_Messages:
        if self._received_solution_events is None or len(self._received_solution_events) != len(self._initialized_events):
            self.load_received_solution_events()
        return [solution for (_, solution, _) in self._received_solution_events]

    def get_solution_at(self, i: int) -> GCTLP_Encrypted_Message:
        return self.solutions[i]

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
        upper_bounds: SC_UpperBounds,
        gctlp: GCTLPInterface,
        helper_id: int | ChecksumAddress,
    ) -> Self:
        """
        Deploys the contract to the network and deposit the coins into the contract
        """
        # Check that the hash function is Keccak256
        if gctlp.hash.name != "KECCAK256":
            raise ValueError("The hash function must be Keccak256")

        abi, sc_bytecode = self._compile_contract()
        contract_address = self._deploy_contract(sc_bytecode, abi, coins, upper_bounds, helper_id)
        logger.info("Deployed Contract Successfully: ", contract_address)
        return self

    def load_contract(self, contract_address: ChecksumAddress) -> None:
        abi, _ = self._compile_contract()
        self._contract = self.web3.eth.contract(address=contract_address, abi=abi)

    def switch_to_account(self, account_index: int) -> None:
        self.account = self.web3.eth.accounts[account_index]

    def add_solution(self, solution: GCTLP_Encrypted_Message, witness: TLP_Digest) -> None:

        if self._initialized_events is None:
            self._load_initialized_events()

        if self._set_commitment_events is None:
            self.load_set_commitment_events()

        amount_of_puzzles = len(self._initialized_events)
        amount_of_puzzles_left = self._contract.functions.amountOfPuzzleParts().call()
        solution_index = amount_of_puzzles - amount_of_puzzles_left

        (_, commitment, prev_puzzle_commitment_sh) = self._set_commitment_events[solution_index]
        (_, coin, upper_bound, prev_puzzle_details_sh) = self._initialized_events[solution_index]

        if not self._has_succeeded(
            self._contract.functions.addSolution(
                solution, witness, commitment, prev_puzzle_commitment_sh, coin, upper_bound, prev_puzzle_details_sh
            )
        ):
            raise RuntimeError("Solution was not added correctly")

    def verify_solution(self, i: int, /) -> bool:
        try:
            self.get_solution_at(i)
            return True
        except IndexError:
            return False

    def pay_back(self, _i: int) -> None:

        solution_index = self._contract.functions.amountOfPuzzleParts().call() - 1

        (_, commitment, prev_puzzle_commitment_sh) = self._set_commitment_events[solution_index]
        (_, coin, upper_bound, prev_puzzle_details_sh) = self._initialized_events[solution_index]

        if not self._has_succeeded(
            self._contract.functions.payBack(
                commitment, prev_puzzle_commitment_sh, coin, upper_bound, prev_puzzle_details_sh
            )
        ):
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

    _SC_PUZZLE_BATCH_SIZE: int = 250

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
        self._sc_init_block = tx_receipt["blockNumber"]

        self._contract = self.web3.eth.contract(
            address=tx_receipt["contractAddress"], abi=abi
        )  # pyright: ignore[reportAttributeAccessIssue]

        self._initialized_events = None
        self._set_commitment_events = None
        self._received_solution_events = None

        # TODO - support for multiple batches
        # Calculate the value to send with this batch
        value_to_send = sum(coins)
        # Call the initialize function for the current batch
        if not self._has_succeeded(
            self._contract.functions.initialize(
                coins,
                list(map(int, upper_bounds)),
                helper_id,
            ),
            value_to_send,
        ):
            raise RuntimeError("Initialize has failed for single-call")

        return tx_receipt["contractAddress"]

    def _initialize_in_batches(
        self,
        coins: SC_Coins,
        upper_bounds: SC_UpperBounds,
        helper_id: int | ChecksumAddress,
    ) -> None:
        # Ensure that all lists have the same length
        assert len(coins) == len(upper_bounds), "All input lists must have the same length"

        batches = [itertools.batched(lst, self._SC_PUZZLE_BATCH_SIZE) for lst in (coins, upper_bounds)]

        for coins_batch, upper_bounds_batch in zip(*batches):

            # Calculate the value to send with this batch
            value_to_send = sum(coins_batch)

            # Call the initialize function for the current batch
            if not self._has_succeeded(
                self._contract.functions.initialize(
                    coins_batch,
                    list(map(int, upper_bounds_batch)),
                    helper_id,
                ),
                value_to_send,
            ):
                raise RuntimeError("Initialize has failed for batch")

    def _initiate_network(self, web3: Optional[Web3] = None) -> None:
        """
        Initiates the network connection
        @:param provider: The provider to use for the connection
        If no provider is given, use the `EthereumTesterProvider` which runs a local testnet
        """
        if web3 is None:
            self._backend = PyEVMBackend.from_mnemonic(
                "test test test test test test test test test test test junk",
                genesis_state_overrides={"balance": Wei(1_000_000 * 10**18)},
            )

            provider = EthereumTesterProvider(ethereum_tester=EthereumTester(backend=self._backend))
            web3 = Web3(provider)

        self.web3 = web3

        assert self.web3.is_connected()

    def _has_succeeded(self, tx: ContractFunction, value: int = 0) -> bool:
        max_fee_per_gas = 1_000_000_000
        max_priority_fee_per_gas = 1_000_000_000

        self._gas_fee_control(1_000_000_000)

        props: TxParams = {
            "from": self.account,
            "value": Wei(value),
            "maxFeePerGas": Wei(max_fee_per_gas),
            "maxPriorityFeePerGas": Wei(max_priority_fee_per_gas),
        }

        tx_hash = tx.transact(props)
        return self.web3.eth.wait_for_transaction_receipt(tx_hash)["status"] == 1

    def _gas_fee_control(self, max_fee_per_gas: int):
        """
        Checks the base fee per gas and mines a block if it is too high to prevent the transaction from failing
        If the backend is not set, this function does nothing
        :return:
        """
        latest_block = self.web3.eth.get_block("latest")
        base_fee_per_gas = latest_block["baseFeePerGas"]  # pyright: ignore[reportTypedDictNotRequiredAccess]

        if base_fee_per_gas > max_fee_per_gas * 0.9 and self._backend is not None:
            self._backend.mine_blocks(1)

    def _load_initialized_events(self):
        if self._sc_init_block is None:
            self._sc_init_block = 0

        logs = self._contract.events.Initialized().get_logs(fromBlock=self._sc_init_block)
        self._initialized_events = [
            (
                log["args"]["index"],
                log["args"]["coins"],
                log["args"]["upperBound"],
                log["args"]["prevPuzzleDetailsStorageHash"],
            )
            for log in logs
        ]
        self._initialized_events.sort(key=lambda x: x[0])

    def load_set_commitment_events(self):
        if self._sc_init_block is None:
            self._sc_init_block = 0

        logs = self._contract.events.CommitmentSet().get_logs(fromBlock=self._sc_init_block)
        self._set_commitment_events = [
            (log["args"]["index"], log["args"]["commitment"], log["args"]["prevPuzzleCommitmentStorageHash"])
            for log in logs
        ]
        self._set_commitment_events.sort(key=lambda x: x[0])

    def load_received_solution_events(self):
        if self._sc_init_block is None:
            self._sc_init_block = 0

        logs = self._contract.events.SolutionReceived().get_logs(fromBlock=self._sc_init_block)
        self._received_solution_events = [
            (log["args"]["revIndex"], log["args"]["solution"], log["args"]["witness"]) for log in logs
        ]
        self._received_solution_events.sort(key=lambda x: -x[0])
