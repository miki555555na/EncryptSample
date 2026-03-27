# 離散ガウスサンプリングや行列演算の補助関数
import numpy as np
from ..params import n, p, chi       
def sample_error(size, sigma=3.2):
    """離散ガウス分布から誤差をサンプリングする関数"""
    return np.array([chi() for _ in range(size)])   
