import socket
import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from src import curve, field, ibe

# PKGサーバー: IBEシステムのセットアップと秘密鍵抽出
def start_pkg_server():
    # IBEシステムのセットアップ
    ibe_sys = ibe.BonehFranklinIBE(curve.E, curve.q, curve.P)
    P_pub = ibe_sys.setup()
    print("PKGサーバー起動: IBEシステムセットアップ完了")

    # ソケット設定
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(5)
    print("PKGサーバー待機中...")

    try:
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"接続: {addr}")
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    continue

                request = json.loads(data)
                if request['type'] == 'get_public_key':
                    # 公開鍵を提供
                    response = {'P_pub': {'x': int(P_pub[0]), 'y': int(P_pub[1])}}
                elif request['type'] == 'extract_private_key':
                    # 秘密鍵を抽出
                    identity = request['identity']
                    priv_key = ibe_sys.extract(identity)
                    response = {'priv_key': {'x': int(priv_key[0]), 'y': int(priv_key[1])}}
                else:
                    response = {'error': 'Unknown request type'}

                conn.sendall(json.dumps(response).encode('utf-8'))
    except KeyboardInterrupt:
        print("PKGサーバー停止")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_pkg_server()
