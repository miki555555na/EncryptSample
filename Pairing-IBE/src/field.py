from sage.all import GF

# パラメータ設定 (p = 3 mod 4 の素数)
p = 593 
Fp = GF(p)
# 埋め込み次数 k=2 の拡大体 i^2 + 1 = 0
R = Fp['x']
x = R.gen()
Fp2 = Fp.extension(x**2 + 1, 'i')