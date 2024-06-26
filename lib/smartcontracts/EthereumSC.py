import functools

from eth_tester import EthereumTester, PyEVMBackend
from solcx import install_solc, compile_files
from web3 import EthereumTesterProvider, Web3

from lib.smartcontracts.SCInterface import SCInterface

SOLC_VERSION = "0.8.0"
CONTRACT_NAME = "SmartContract"
CONTRACT_PATH = "../../contracts/SmartContract.sol"


class EthereumSC(SCInterface):
    web3 = None

    def __init__(self, account=None, web3=None):
        print("Initiating EthereumSC")
        self._initiate_network(web3)
        print("Network initiated")
        self.__account = account
        print("Account initiated")
        self.contract = None

    # Public Properties #

    @property
    def commitments(self):
        return self._contract.functions.commitments().call()

    @commitments.setter
    def commitments(self, commitments):
        self._send_and_wait(
            self._contract.functions.setCommitments(commitments)
        )
        # Check if the commitments were set correctly
        assert commitments == self._contract.functions.commitments().call()

    @property
    def coins(self):
        return self._contract.functions.coins().call()

    @property
    def upper_bounds(self):
        return self._contract.functions.upperBounds().call()

    @property
    def start_time(self):
        return self._contract.functions.startTime().call()

    # Public Methods #

    def initiate(self, coins, start_time, extra_time, upper_bounds, helper_id):
        """
             Deploys the contract to the network and deposit the coins into the contract
        """

        (abi, sc_bytecode) = self._compile_contract()
        contract_address = self._deploy_contract(sc_bytecode, abi, coins, start_time, extra_time, upper_bounds,
                                                 helper_id)
        print("Deployed Contract Successfully: ", contract_address)
        return self

    def load_contract(self, contract_address):
        (abi, _) = self._compile_contract()
        self.contract = self.web3.eth.contract(address=contract_address, abi=abi)

    def add_solution(self, solution, witness):
        pass

    def get_message_at(self, i):
        pass

    # Private Properties #

    @property
    def _contract(self):
        if self.contract is None:
            raise RuntimeError("No Contract set.  Please load a contract or initiate it first.")
        return self.contract

    @_contract.setter
    def _contract(self, value):
        if self.contract is not None:
            raise RuntimeError("Contract already set.  Please create a new instance to set a new contract.")
        self.__contract = value

    @property
    def _account(self):
        if self._account is None:
            raise RuntimeError("No Account set.  Please set an account to use the contract.")
        return self._account

    @_account.setter
    def _account(self, value):
        self.__account = value

    # Private Methods #

    def _setup_account_from_index(self, account_index):
        self._account = self.web3.eth.accounts[account_index]

    def _compile_contract(self):
        """
            Loads in the ABI of the EDTLP contract
        """

        install_solc(SOLC_VERSION)

        compiled_sol = compile_files(
            [CONTRACT_PATH],
            output_values=["abi", "bin"],
            solc_version=SOLC_VERSION,
        )

        abi = compiled_sol[CONTRACT_PATH + ":" + CONTRACT_NAME]["abi"]
        bytecode = compiled_sol[CONTRACT_PATH + ":" + CONTRACT_NAME]["bin"]

        assert abi is not None
        assert bytecode is not None

        return abi, bytecode

    def _deploy_contract(self, bytecode, abi, coins, start_time, extra_time, upper_bounds, helper_id):
        """
            Deploys the contract to the network
        """
        contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)

        tx_receipt = self._send_and_wait(
            contract.constructor(
                coins,
                start_time,
                extra_time,
                upper_bounds,
                helper_id
            ),
            value=functools.reduce(lambda x, y: x + y, coins)
        )

        self.contract = self.web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        return tx_receipt.contractAddress

    def _initiate_network(self, web3=None):
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

    def _send_and_wait(self, tx, value=None):
        props = {"from": self.__account}
        if value is not None:
            props["value"] = value

        tx_hash = tx.transact(props)
        return self.web3.eth.wait_for_transaction_receipt(tx_hash)


if __name__ == "__main__":
    test_provider = EthereumTesterProvider(ethereum_tester=EthereumTester(backend=PyEVMBackend()))
    test_web3 = Web3(test_provider)
    test_account = test_web3.eth.accounts[1]
    print(test_account)

    sc = EthereumSC(account=test_account, web3=test_web3)
    sc.initiate([1, 2], 10, 1, [1, 2], test_account)
    sc.commitments = [143, 244]
    print(sc.commitments)
    print(sc.coins)
    print(sc.start_time)
    print(sc.upper_bounds)
    print("EthereumSC ran successfully")