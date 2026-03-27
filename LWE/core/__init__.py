import sys
import os
import numpy as np

# 親ディレクトリのパスを追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .lwe_engine import LWEEngine

def sample_error(size, sigma):
    """誤差ベクトルをサンプリング"""
    return np.array([int(np.random.normal(0, sigma)) for _ in range(size)])

__all__ = ['LWEEngine', 'sample_error']

