from eth_tester import EthereumTester, MockBackend, PyEVMBackend
from eth_typing import Address
from solcx import install_solc, compile_standard, compile_source, compile_files
from web3 import Web3, EthereumTesterProvider

SOLC_VERSION = "0.8.0"
CONTRACT_NAME = "EDTLP"
CONTRACT_PATH = "../contracts/EDTLP.sol"



class RGMILTP:
    """
        Loads in the ABI of the EDTLP contract
    """
    def load_abi(self):

        install_solc(SOLC_VERSION)

        compiled_sol = compile_files(
            [CONTRACT_PATH],
            output_values=["abi"],
            solc_version = SOLC_VERSION,
        )

        print(compiled_sol)

        self.abi = compiled_sol[CONTRACT_PATH+":"+CONTRACT_NAME]["abi"]


    def __init__(self):
        self.load_abi()
        pass



if __name__ == "__main__":
    rgmitlp = RGMILTP()
