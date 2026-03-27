# 楕円曲線と点の演算
from src.field import Fp

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Curve:
    def __init__(self, a, b, p):
        # a, b は曲線 y^2 = x^3 + ax + b の係数
        # p は素数 (有限体のモジュロ)
        self.a = a
        self.b = b
        # 内部では整数として扱う。Fp インスタンスも保持して便利な演算に利用する。
        if isinstance(p, Fp):
            self.p = p.p
        else:
            self.p = int(p)
        self.field = Fp(self.p)

    def is_on_curve(self, point): # 点が曲線上にあるか確認
        if point is None:
            return True
        # Fp オブジェクトは使わず、mod p で演算
        left = (point.y * point.y) % self.p
        right = (point.x * point.x * point.x + self.a * point.x + self.b) % self.p
        return left == right

    def add(self, P, Q): # 点PとQを加算する
        if P is None:
            return Q
        if Q is None:
            return P
        
        if P.x == Q.x and P.y != Q.y:
            return None
        
        if P == Q:
            # 点Pでの接線の傾きを計算
            # y座標が0の場合、接線は垂直になり点の2倍は無限遠（None）
            if P.y % self.p == 0:
                return None
            # 逆元は pow(base, -1, mod) で取得できる
            m = (3 * P.x * P.x + self.a) * pow(2 * P.y, -1, self.p) % self.p
        else:
            # 点PとQを結ぶ直線の傾きを計算
            m = (Q.y - P.y) * pow(Q.x - P.x, -1, self.p) % self.p
        
        x_r = (m * m - P.x - Q.x) % self.p
        y_r = (m * (P.x - x_r) - P.y) % self.p
        
        return Point(x_r, y_r)

    def mul(self, k, P): # 点Pをk倍する（スカラー倍）
        result = None
        addend = P
        
        while k:
            if k & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            k >>= 1
        
        return result
    
    