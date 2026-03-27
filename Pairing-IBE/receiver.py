import socket
import json
import sys, os
import base64
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

# 受信者: PKGから秘密鍵を取得し、送信者から暗号化メッセージを受信して復号
def start_receiver(identity="alice@example.com"):
    # PKGから公開鍵を取得
    pkg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pkg_socket.connect(('127.0.0.1', 50000))
    request = {'type': 'get_public_key'}
    pkg_socket.sendall(json.dumps(request).encode('utf-8'))
    response = json.loads(pkg_socket.recv(1024).decode('utf-8'))
    P_pub_data = response['P_pub']
    P_pub = (P_pub_data['x'], P_pub_data['y'], 1)  # Sage point format
    pkg_socket.close()
    print("PKGから公開鍵を取得しました")

    # PKGから秘密鍵を取得
    pkg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pkg_socket.connect(('127.0.0.1', 50000))
    request = {'type': 'extract_private_key', 'identity': identity}
    pkg_socket.sendall(json.dumps(request).encode('utf-8'))
    response = json.loads(pkg_socket.recv(1024).decode('utf-8'))
    priv_key_data = response['priv_key']
    priv_key = (priv_key_data['x'], priv_key_data['y'], 1)  # Sage point format
    pkg_socket.close()
    print(f"PKGから秘密鍵を取得しました: {identity}")

    # 受信サーバー起動
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 50001))
    server_socket.listen(1)
    print("受信者待機中...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"送信者接続: {addr}")
        data = conn.recv(4096).decode('utf-8')
        if data:
            cipher_data = json.loads(data)
            U_data = cipher_data['U']
            U = (U_data['x'], U_data['y'], 1)
            V = base64.b64decode(cipher_data['V'])
            pair_val = cipher_data['pair_val']

            # 復号
            from src import ibe
            message = ibe.BonehFranklinIBE.decrypt((U, V, pair_val), priv_key)
            print(f"復号されたメッセージ: {message}")

    server_socket.close()

if __name__ == "__main__":
    start_receiver()
