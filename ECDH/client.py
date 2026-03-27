from src.curve import Curve, Point
from src.node import ECCNode
import socket
import json
import random

def start_client():
    # 1. サーバーへ接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 50008))

    # 2. 共通の楕円曲線と生成点を定義
    curve = Curve(a=1, b=1, p=23)
    G = Point(x=6, y=19)

    # 3. クライアントの秘密鍵を生成
    client_node = ECCNode(curve, G)
    pub_key, priv_key = client_node.generate_keys(secret_int=3) # 例として秘密鍵を3に設定
    print("クライアントの秘密鍵を生成しました") 

    # 4. 公開鍵をサーバーに送信
    pub_key_json = json.dumps({'x': pub_key.x, 'y': pub_key.y})
    client_socket.sendall(pub_key_json.encode('utf-8'))
    print("クライアントの公開鍵をサーバーに送信しました")   

    # 5. サーバーから公開鍵を受信
    server_pub_key_data = client_socket.recv(1024).decode('utf-8')
    server_pub_key_json = json.loads(server_pub_key_data)
    server_pub_key = Point(x=server_pub_key_json['x'], y=server_pub_key_json['y'])
    print("サーバーの公開鍵を受信しました") 

    # 6. 共有秘密を計算
    shared_secret = client_node.compute_shared_secret(server_pub_key)
    print(f"共有秘密を計算しました: ({shared_secret.x}, {shared_secret.y})")    

    # 7. 暗号化されたメッセージを送信
    message = random.choice(["Hello, Server!", "This is a secret message.", "ECDH is fun!"])
    # ここでは、共有秘密のx座標をキーとして単純なXOR暗号化を行う例を示します
    key = shared_secret.x
    encrypted_message = bytes([b ^ key for b in message.encode('utf-8')])
    client_socket.sendall(encrypted_message)
    print(f"暗号化されたメッセージを送信しました: {encrypted_message}")

    client_socket.close()

if __name__ == "__main__":
    start_client()    

