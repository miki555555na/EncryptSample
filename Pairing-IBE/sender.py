import socket
import json
import sys, os
import base64
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from src import curve, field, ibe

# 送信者: PKGから公開鍵を取得し、メッセージを暗号化して受信者に送信
def start_sender(identity="alice@example.com", message="Hello, IBE!"):
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

    # IBEシステムでメッセージを暗号化
    ibe_sys = ibe.BonehFranklinIBE(curve.E, curve.q, curve.P)
    U, V, pair_val = ibe_sys.encrypt(identity, message, P_pub)
    print(f"メッセージを暗号化しました: {message}")

    # 受信者に送信
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 50001))
    cipher_data = {
        'U': {'x': int(U[0]), 'y': int(U[1])},
        'V': base64.b64encode(V).decode('ascii'),
        'pair_val': int(pair_val)
    }
    client_socket.sendall(json.dumps(cipher_data).encode('utf-8'))
    client_socket.close()
    print("暗号化メッセージを送信しました")

if __name__ == "__main__":
    start_sender()
