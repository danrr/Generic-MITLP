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
    abi = None

    # TODO - add the rest of the contract variables
    commitments = []
    start_time = 0
    upper_bounds = []
    coins = []

    def initiate(self, coins, start_time, extra_time, upper_bounds, helper_id):
        """
             Deploys the contract to the network and deposit the coins into the contract
        """

        sc_bytecode = self._compile_contract()
        contract_address = self._deploy_contract(sc_bytecode, coins, start_time, extra_time, upper_bounds, helper_id)
        print("Deployed Contract Successfully: ", contract_address)
        return self

    def __init__(self, account_index=0, provider=None):
        print("Initiating EthereumSC")
        self._initiate_network(provider)
        print("Network initiated")
        self.setup_account_from_index(account_index)
        print("Account initiated")

    def add_solution(self, solution, witness):
        pass

    def get_message_at(self, i):
        pass

    def load_contract(contract_address):
        pass

    # Private Properties #

    @property
    def _account(self):
        if self._account is None:
            raise RuntimeError("No Account set.  Please set an account to use the contract.")
        return self._account

    @_account.setter
    def _account(self, value):
        self.__account = value

    def setup_account_from_index(self, account_index):
        self._account = self.web3.eth.accounts[account_index]

    # Private Methods #

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

        self.abi = compiled_sol[CONTRACT_PATH + ":" + CONTRACT_NAME]["abi"]
        bytecode = compiled_sol[CONTRACT_PATH + ":" + CONTRACT_NAME]["bin"]

        assert self.abi is not None
        assert bytecode is not None

        return bytecode

    def _deploy_contract(self, bytecode, coins, start_time, extra_time, upper_bounds, helper_id):
        """
            Deploys the contract to the network
        """
        contract = self.web3.eth.contract(abi=self.abi, bytecode=bytecode)

        tx_hash = contract.constructor(
            coins,
            start_time,
            extra_time,
            upper_bounds,
            helper_id

        ).transact(
            {
                "from": self.__account,
                'value': functools.reduce(lambda x, y: x + y, coins)
             }
        )
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.contractAddress

    def _initiate_network(self, provider=None):
        """
            Initiates the network connection
            @:param provider: The provider to use for the connection
            If no provider is given, use the `EthereumTesterProvider` which runs a local testnet
        """
        #
        if provider is None:
            provider = EthereumTesterProvider(ethereum_tester=EthereumTester(backend=PyEVMBackend()))

        self.web3 = Web3(provider)

        assert self.web3.is_connected()


if __name__ == "__main__":
    sc = EthereumSC(1)
    sc.initiate([1, 2], 10, 1, [1, 2], "0x9ac103735E60c4D3445A068162e943f6784bE104")
