from cryptography.fernet import Fernet


class FernetWrapper:
    @staticmethod
    def generate_key() -> int:
        key = Fernet.generate_key()
        key_int = int.from_bytes(key, "big")
        return key_int

    @staticmethod
    def __get_sym_cipher(key_int: int) -> Fernet:
        key_bytes = int.to_bytes(key_int, length=128, byteorder="big")
        cipher_suite = Fernet(key_bytes)
        return cipher_suite

    @classmethod
    def encrypt(cls, key_int: int, message: bytes) -> bytes:
        cipher_suite = cls.__get_sym_cipher(key_int)
        encrypted_message = cipher_suite.encrypt(message)
        return encrypted_message

    @classmethod
    def decrypt(cls, key_int: int, encrypted_message: bytes) -> bytes:
        cipher_suite = cls.__get_sym_cipher(key_int)
        message = cipher_suite.decrypt(encrypted_message)
        return message
