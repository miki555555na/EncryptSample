import socket
import random

def is_prime(n, k=100):
    """Miller-Rabin素数判定法で素数判定"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # n-1 = 2^r * d の形に分解
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # k回のテストを実行
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def generate_prime(bits):
    """指定したビット数の素数を生成"""
    while True:
        num = random.getrandbits(bits) # 指定されたビット数のランダムな数を生成
        num |= (1 << (bits - 1)) | 1  # MSBとLSBを1にして確実にビット数を満たす
        
        if is_prime(num): # 素数判定
            return num

def start_server():
    # 1. ソケットの設定 (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 50007)) # ローカルホストのポート50007
    server_socket.listen(1)
    
    print("サーバー起動：クライアントの接続を待っています...")
    
    conn, addr = server_socket.accept()
    with conn:
        print(f"接続されました: {addr}")
        
        # 2. クライアントからnの桁数を受信
        key_bits_data = conn.recv(2)
        key_bits = int.from_bytes(key_bits_data, 'big')
        print(f"クライアントが要求した鍵の桁数: {key_bits} bits")
        
        # 3. 公開鍵の生成 (n, e)
        # p,qを相異なる大きな素数とし、n = p*q, φ(n) = (p-1)*(q-1) を計算
        # 指定されたnの桁数に応じてp,qをランダムに生成
        p = generate_prime(key_bits // 2)
        q = generate_prime(key_bits // 2)
        
        # p と q が異なることを確認
        while p == q:
            q = generate_prime(key_bits // 2)
        
        n = p * q
        phi_n = (p - 1) * (q - 1)
        
        # eの選択（一般的に65537を使用）
        e = 65537

        # dの計算（de ≡ 1 mod φ(n)）
        d = pow(e, -1, phi_n)
        
        print(f"\n--- 鍵生成完了 ---")
        print(f"n のビット数: {n.bit_length()}")
        print(f"n の桁数上限: {n_bytes * 8} bits")
        
        # 4. 公開鍵を送信 (数値をバイト列に変換)
        # nのビット数をバイト数に変換（切り上げ）
        n_bytes = (n.bit_length() + 7) // 8
        conn.sendall(n.to_bytes(n_bytes, 'big'))
        conn.sendall(e.to_bytes(4, 'big'))
        print("公開鍵 (n, e) を送信しました。")
        
        # 5. 暗号文を受信
        data = conn.recv(n_bytes)
        if data:
            cipher_int = int.from_bytes(data, 'big')
            print(f"暗号文（数値）を受信しました")
            # print(f"{cipher_int}")
            
            # --- ここで復号処理 ---
            # m = power_mod(cipher_int, d, n) を実行
            print("復号を開始します...")
            message_int = pow(cipher_int, d, n)
            
            # メッセージサイズの確認
            if message_int >= n:
                print("エラー: 復号したメッセージが n 以上です（不正な暗号化）")
            else:
                # 数値を文字列に変換（元のバイト数に合わせる）
                # 注意: ビット長ベースの計算では先頭の0x00が失われる可能性がある
                message_bytes = message_int.to_bytes(n_bytes, 'big')
                # 元のメッセージは n_bytes より短い可能性があるため、
                # ここではランダムなパディングのない「素朴な」RSAの限界と言える
                try:
                    # パディング情報がないため、末尾のNULLバイトまで含める
                    # 実運用ではOAEPパディングを使用する
                    message = message_bytes.rstrip(b'\x00').decode('utf-8')
                    print(f"復号されたメッセージ: {message}")
                except UnicodeDecodeError:
                    print(f"エラー: UTF-8デコード失敗")
                    print(f"復号値（16進数）: {message_int:x}")


if __name__ == "__main__":
    start_server()