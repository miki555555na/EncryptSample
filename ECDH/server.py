from src.curve import Curve, Point
from src.node import ECCNode
import socket
import json

def start_server():
    # 1. ソケットの設定 (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 50008)) # ローカルホストのポート50008
    server_socket.listen(1)

    print("サーバー起動：クライアントの接続を待っています...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"接続されました: {addr}")

        # 2. 共通の楕円曲線と生成点を定義
        curve = Curve(a=1, b=1, p=23)
        G = Point(x=6, y=19)

        # 3. サーバーの秘密鍵を生成
        server_node = ECCNode(curve, G)
        pub_key, priv_key = server_node.generate_keys(secret_int=7) # 例として秘密鍵を7に設定
        print("サーバーの秘密鍵を生成しました")

        # 4. 公開鍵をクライアントに送信
        pub_key_data = server_node.serialize_public_key().encode('utf-8')
        conn.sendall(pub_key_data)
        print("サーバーの公開鍵をクライアントに送信しました")

        # 5. クライアントから公開鍵を受信
        client_pub_key_data = conn.recv(1024).decode('utf-8')
        client_pub_key_json = json.loads(client_pub_key_data)
        client_pub_key = Point(x=client_pub_key_json['x'], y=client_pub_key_json['y'])
        print("クライアントの公開鍵を受信しました")

        # 6. 共有秘密を計算
        shared_secret = server_node.compute_shared_secret(client_pub_key)
        print(f"共有秘密を計算しました: ({shared_secret.x}, {shared_secret.y})")

        # 7. 暗号化されたメッセージを受信
        encrypted_message = conn.recv(1024)
        print(f"暗号化されたメッセージを受信しました: {encrypted_message}") 
        
        # 8.共有秘密を利用して復号処理を行う
        # ここでは、共有秘密のx座標をキーとして単純なXOR復号を行う
        key = shared_secret.x
        decrypted_message = bytes([b ^ key for b in encrypted_message])
        print(f"復号されたメッセージ: {decrypted_message.decode('utf-8')}") 
        

if __name__ == "__main__":
    start_server()


