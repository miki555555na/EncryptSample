class PublicKeyEncryptionScheme:
    def keygen(self):
        """鍵生成アルゴリズム"""
        raise NotImplementedError

    def encrypt(self, public_key, plaintext):
        """暗号化アルゴリズム"""
        raise NotImplementedError

    def decrypt(self, private_key, ciphertext):
        """復号アルゴリズム"""
        raise NotImplementedError