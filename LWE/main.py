# 実行用
import sys
import os
import numpy as np
from schemes.regev_pke import RegevPKE

if __name__ == "__main__":
    # パラメータ設定
    n = 512  # 次元
    p = 12289  # 素数
    sigma = 3.2  # 誤差の標準偏差

    # Regev PKEのインスタンス化
    regev = RegevPKE(n, p, sigma)

    # 鍵生成
    public_key, secret_key = regev.keygen()
    print("鍵生成完了")

    # メッセージの暗号化
    # ランダムに0か1を選ぶ
    message = np.random.randint(0, 2)
    ciphertext = regev.encrypt(public_key, message)
    print(f"メッセージ {message} を暗号化しました")
    

    # メッセージを復号
    decrypted_message = regev.decrypt(secret_key, ciphertext)
    print(f"復号されたメッセージ: {decrypted_message}")
    print(f"復号成功: {message == decrypted_message}")
    