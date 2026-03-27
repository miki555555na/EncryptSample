# Regev方式の具体的な実装
import sys
import os
import numpy as np

from core import LWEEngine, sample_error

class RegevPKE:
    def __init__(self, n, p, sigma):
        self.n = n
        self.p = p
        self.sigma = sigma
        self.lwe_engine = LWEEngine(n, p)

    def keygen(self):
        # 公開鍵と秘密鍵の生成
        A = self.lwe_engine.sample_matrix(self.n, self.n)  # ランダムな行列A(n x n)
        s = self.lwe_engine.sample_vector(self.n)  # 秘密ベクトルs (n次元)
        e = sample_error(self.n, self.sigma)  # 誤差ベクトルe (n次元)
        b = (A @ s + e) % self.p  # 公開鍵b
        return (A, b), s  # 公開鍵と秘密鍵を返す

    def encrypt(self, pk, m):
        A, b = pk
        # メッセージmを暗号化
        # ランダムな部分集合Sを選ぶ
        # n/2個のインデックスをランダムに選ぶ
        S = np.random.choice(self.n, size=self.n//2, replace=False)
        a_sum = np.sum(A[S], axis=0) % self.p  # 選んだ行の和を取る
        b_sum = np.sum(b[S]) % self.p  # 選んだ要素の和を取る
        if m == 1:
            b_sum = (b_sum + self.p // 2) % self.p
        return (a_sum, b_sum)  # 暗号文を返す

    def decrypt(self, sk, ciphertext):
        s = sk
        u, v = ciphertext
        #暗号文(a,b)を受け取った時、
        # diff = b - <a,s> (mod p)を計算する。
        diff = (v - np.dot(u, s)) % self.p
        # diffが0に近ければ0と判定し、[p/2]に近ければ1と判定する。
        if diff < self.p // 4 or diff > 3 * self.p // 4:
            return 0
        else:
            return 1