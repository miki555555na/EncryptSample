import socket

def start_client():
    # 1. サーバーへ接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 50007))
    
    # 2. 鍵の桁数をユーザーから入力
    # nの桁数を指定する
    n_key_bits = int(input("公開鍵に含まれるnのビット数を指定してください (例: 256): "))
    client_socket.sendall(n_key_bits.to_bytes(2, 'big'))

    # 3. 公開鍵を受信
    # nのバイト数を計算（ビット数 / 8 = バイト数）
    n_bytes = (n_key_bits + 7) // 8  # 切り上げ計算
    n_data = client_socket.recv(n_bytes)
    e_data = client_socket.recv(4)
    
    n_received = int.from_bytes(n_data, 'big')
    e_received = int.from_bytes(e_data, 'big')
    print(f"サーバーから公開鍵を受信")
    # print(f"n={n_received}, e={e_received}")
    
    # 4. メッセージを暗号化
    message = input("暗号化したいメッセージを入力してください: ")
    message_bytes = message.encode('utf-8')
    
    # メッセージが小さすぎないかチェック
    if len(message_bytes) > n_bytes - 1:
        print(f"エラー: メッセージが長すぎます。最大{n_bytes - 1}バイトを入力してください")
        client_socket.close()
        return
    
    # パディングなしでは、メッセージのサイズ情報が失われる問題がある
    # 実運用ではOAEPパディングを使用すべき
    # ここでは、メッセージを n_bytes バイトにパディング
    padded_bytes = message_bytes + b'\x00' * (n_bytes - len(message_bytes))
    m_int = int.from_bytes(padded_bytes, 'big')
    
    # メッセージが n より小さいことを確認
    if m_int >= n_received:
        print(f"エラー: 暗号化に失敗しました（メッセージが大きすぎます）")
        client_socket.close()
        return
    
    # 暗号化: c = m^e mod n
    cipher_val = pow(m_int, e_received, n_received)
    print(f"メッセージ '{message}' を暗号化しました")
    
    # 5. 暗号文を送信
    client_socket.sendall(cipher_val.to_bytes(n_bytes, 'big'))
    print("暗号文を送信しました。")
    
    client_socket.close()

if __name__ == "__main__":
    start_client()