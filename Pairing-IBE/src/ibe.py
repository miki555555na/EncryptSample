import hashlib
from src.field import Fp2
from src.curve import E, E2, P, q
import random   
from pairing_Miller import weil_pairing

class BonehFranklinIBE:
    def __init__(self, curve, m, P):
        self.curve = curve
        self.m = m  # 群の位数
        self.P = P  # 生成元
        # 補助点はランダムに生成した multiple of P で代用
        self.S = self.random_point()

    def random_point(self):
        """曲線上のランダムな点として P のランダムスカラー倍を返す"""
        r = random.randint(1, self.m - 1)
        return r * self.P

    def hash_to_point(self, identity: str):
        """ID を曲線上の点に簡易的にマップするハッシュ関数

        実装では SHA256 の出力を整数とみなし、
        それを生成元 P のスカラー倍として点を決定する。
        """
        h = int(hashlib.sha256(identity.encode()).hexdigest(), 16)
        return (h % self.m) * self.P

    def setup(self):
        # マスター秘密鍵 s
        self.s = random.randint(1, self.m - 1)
        # システム公開鍵 P_pub = sP
        # Sage の点についてはスカラー倍が ``*`` 演算子で出来る
        self.P_pub = self.s * self.P
        return self.P_pub

    def extract(self, identity):
        # H1: IDを楕円曲線上の点にマップ (Hash-to-Point)
        Q_ID = self.hash_to_point(identity)
        # ユーザー秘密鍵 d_ID = s * Q_ID
        d_ID = self.s * Q_ID
        return d_ID

    def encrypt(self, identity, message, P_pub):
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
        elif isinstance(message, bytes):
            message_bytes = message
        else:
            raise TypeError("message must be str or bytes")

        Q_ID = self.hash_to_point(identity)
        r = random.randint(1, self.m - 1)

        # U = rP
        U = r * self.P

        # r倍されたペアリング値を計算: g^r = e(Q_ID, P_pub)^r
        # 双線性により e(Q_ID, P_pub)^r = e(Q_ID, r * P_pub)
        pair_val = weil_pairing(self.m, Q_ID, r * P_pub, self.S, self.curve) 

        key_int = self.hash_h2(pair_val)
        key_bytes = key_int.to_bytes((key_int.bit_length() + 7) // 8, 'big')
        key_repeated = (key_bytes * ((len(message_bytes) + len(key_bytes) - 1) // len(key_bytes)))[:len(message_bytes)]
        V = bytes(a ^ b for a, b in zip(message_bytes, key_repeated))

        return (U, V, pair_val)

    @staticmethod
    def decrypt(ciphertext, d_ID):
        U, V, pair_val = ciphertext

        key_int = BonehFranklinIBE.hash_h2_static(pair_val)
        key_bytes = key_int.to_bytes((key_int.bit_length() + 7) // 8, 'big')
        key_repeated = (key_bytes * ((len(V) + len(key_bytes) - 1) // len(key_bytes)))[:len(V)] # Vの長さに合わせてキーを繰り返す
        decrypted_bytes = bytes(a ^ b for a, b in zip(V, key_repeated))

        try:
            return decrypted_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return decrypted_bytes

    def hash_h2(self, pairing_element):
        # ターゲット群の要素からビット列（数値）へのハッシュ
        return BonehFranklinIBE.hash_h2_static(pairing_element)

    @staticmethod
    def hash_h2_static(pairing_element):
        # ターゲット群の要素からビット列（数値）へのハッシュ
        return int(hashlib.sha256(str(pairing_element).encode()).hexdigest(), 16)