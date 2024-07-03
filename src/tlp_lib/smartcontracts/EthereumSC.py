import functools
from pathlib import Path
from typing import Optional

from eth_tester import EthereumTester, PyEVMBackend
from solcx import compile_files, install_solc
from web3 import EthereumTesterProvider, Web3

SOLC_VERSION = "0.8.0"
CONTRACT_NAME = "SmartContract"
CONTRACT_PATH = str(Path("../../../contracts/SmartContract.sol").resolve())


class EthereumSC:
    web3: Web3

    def __init__(self, account=None, web3: Optional[Web3] = None, contract_path: str = CONTRACT_PATH):
        print("Initiating EthereumSC")
        self._initiate_network(web3)
        print("Network initiated")
        self.account = account

        self._contract = None
        self._contract_path = contract_path

    # Public Properties #

    @property
    def commitments(self):
        return self._contract.functions.commitments().call()

    @commitments.setter
    def commitments(self, commitments):
        if not self._has_succeeded(self._contract.functions.setCommitments(commitments)):
            raise RuntimeError("Commitments were not set correctly")

    @property
    def coins(self):
        return self._contract.functions.coins().call()

    @property
    def upper_bounds(self):
        return self._contract.functions.upperBounds().call()

    @property
    def start_time(self):
        return self._contract.functions.startTime().call()

    @property
    def solutions(self):
        res = self._contract.functions.solutions().call()

        return list(zip(res[0], res[1], res[2]))

    @property
    def initial_timestamp(self):
        return self._contract.functions.initialTimestamp().call()

    @property
    def account(self):
        if self._account is None:
            raise RuntimeError("No Account set.  Please set an account to use the contract.")
        return self._account

    @account.setter
    def account(self, value):
        self._account = value

    # Public Methods #

    def initiate(self, coins, start_time, extra_time, upper_bounds, helper_id):
        """
        Deploys the contract to the network and deposit the coins into the contract
        """

        (abi, sc_bytecode) = self._compile_contract()
        contract_address = self._deploy_contract(
            sc_bytecode, abi, coins, start_time, extra_time, upper_bounds, helper_id
        )
        print("Deployed Contract Successfully: ", contract_address)
        return self

    def load_contract(self, contract_address):
        (abi, _) = self._compile_contract()
        self._contract = self.web3.eth.contract(address=contract_address, abi=abi)

    def switch_to_account(self, account_index):
        self.account = self.web3.eth.accounts[account_index]

    def add_solution(self, solution, witness):
        if not self._has_succeeded(self._contract.functions.addSolution(solution, witness)):
            raise RuntimeError("Solution was not added correctly")

    def get_message_at(self, i):
        return self._contract.functions.getSolutionAt(i).call()

    def pay(self, i):
        if not self._has_succeeded(self._contract.functions.pay(i)):
            raise RuntimeError("Payout was not successful")

    def pay_back(self, i):
        if not self._has_succeeded(self._contract.functions.payBack(i)):
            raise RuntimeError("Payback was not successful")

    # Private Properties #

    @property
    def _contract(self):
        if self.__contract is None:
            raise RuntimeError("No Contract set.  Please load a contract or initiate it first.")
        return self.__contract

    @_contract.setter
    def _contract(self, value):
        self.__contract = value

    # Private Methods #

    def _compile_contract(self):
        """
        Loads in the ABI of the EDTLP contract
        """

        install_solc(SOLC_VERSION)

        compiled_sol = compile_files(
            [self._contract_path],
            output_values=["abi", "bin"],
            solc_version=SOLC_VERSION,
        )

        abi = compiled_sol[self._contract_path + ":" + CONTRACT_NAME]["abi"]
        bytecode = compiled_sol[self._contract_path + ":" + CONTRACT_NAME]["bin"]

        assert abi is not None
        assert bytecode is not None

        return abi, bytecode

    def _deploy_contract(self, bytecode, abi, coins, start_time, extra_times, upper_bounds, helper_id):
        """
        Deploys the contract to the network
        """
        contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)

        tx_hash = contract.constructor(
            coins, start_time, list(map(int, extra_times)), list(map(int, upper_bounds)), helper_id
        ).transact({"from": self.account, "value": functools.reduce(lambda x, y: x + y, coins)})

        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

        self._contract = self.web3.eth.contract(address=tx_receipt["contractAddress"], abi=abi)
        return tx_receipt["contractAddress"]

    def _initiate_network(self, web3: Optional[Web3] = None):
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

    def _has_succeeded(self, tx):
        props = {"from": self.account}

        tx_hash = tx.transact(props)
        return self.web3.eth.wait_for_transaction_receipt(tx_hash)["status"] == 1
