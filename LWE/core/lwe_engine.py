# LWEサンプルの生成ロジック
import numpy as np
import sys
import os

from params import n, p, chi   

class LWEEngine:    
    def __init__(self, n, p):
        self.n = n
        self.p = p

    def sample_vector(self, size):
        """ランダムなベクトルをサンプリング"""
        return np.random.randint(0, self.p, size) # ベクトルの要素は0からp-1の整数(sizeのサイズ)

    def sample_matrix(self, rows, cols):
        """ランダムな行列をサンプリング"""
        return np.random.randint(0, self.p, (rows, cols)) # 行列の要素は0からp-1の整数(rows x colsのサイズ)

    def sample_error_vector(self, size):
        """誤差ベクトルをサンプリング"""
        return np.array([chi() for _ in range(size)]) # 誤差ベクトルの要素はchi()関数でサンプリングされた整数(sizeのサイズ)
    