from sage.all import EllipticCurve
from src.field import Fp, Fp2

# E / Fp: y^2 = x^3 + x　有限体上の楕円曲線
E = EllipticCurve(Fp, [0, 0, 0, 1, 0]) 
# E / Fp2: 拡大体上の点も扱えるようにする
E2 = E.base_extend(Fp2)

# 生成元と位数の取得
P = E.gens()[0] #Eの生成元
q = P.order() #Pの位数
