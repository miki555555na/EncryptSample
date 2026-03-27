# 有限体Fpの演算
class Fp:
    def __init__(self, p):
        self.p = p

    def add(self, a, b):
        return (a + b) % self.p

    def sub(self, a, b):
        return (a - b) % self.p

    def mul(self, a, b):
        return (a * b) % self.p

    def inv(self, a):
        # 拡張ユークリッドアルゴリズムで逆元を計算
        t, newt = 0, 1
        r, newr = self.p, a
        while newr != 0:
            quotient = r // newr
            t, newt = newt, t - quotient * newt
            r, newr = newr, r - quotient * newr
        if r > 1:
            raise ValueError(f"{a}は逆元を持ちません")
        if t < 0:
            t += self.p
        return t

    def div(self, a, b):
        return self.mul(a, self.inv(b))