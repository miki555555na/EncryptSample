import socket
import secrets
import sys

def recv_exact(sock, n):
    """指定したバイト数nが揃うまで繰り返し受信する"""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError('socket closed')
        data += chunk
    return data

def recv_len_prefixed_int(sock):
    """2バイトで長さを受け取り、その後データを受信"""
    len_b = recv_exact(sock, 2)
    L = int.from_bytes(len_b, 'big')
    data = recv_exact(sock, L)
    return int.from_bytes(data, 'big')

def send_len_prefixed_int(sock, v):
    """整数vをバイト列に変換し、2バイトの長さとともに送信"""
    b = v.to_bytes((v.bit_length() + 7) // 8 or 1, 'big')
    sock.sendall(len(b).to_bytes(2, 'big'))
    sock.sendall(b)

def elgamal_encrypt(m_int, p, g, y):
    # m_int must be 0 <= m < p
    if not (0 <= m_int < p):
        raise ValueError('message integer must satisfy 0 <= m < p')

    k = secrets.randbelow(p - 2) + 1  # 1 <= k <= p-2
    c1 = pow(g, k, p)
    s = pow(y, k, p)
    c2 = (m_int * s) % p
    return c1, c2

def start_client():
    # 1. サーバーへ接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 50007))

    # 2. 公開鍵（p, g, y）を受信
    p = recv_len_prefixed_int(client_socket)
    g = recv_len_prefixed_int(client_socket)
    y = recv_len_prefixed_int(client_socket)

    print(f"受信した公開鍵: p(bitlen)={p.bit_length()}, g={g}, y={y}")

    # 3. メッセージ入力
    msg = input("暗号化したいメッセージを入力してください: ")
    m_int = int.from_bytes(msg.encode('utf-8'), 'big') # 文字列を数値に変換
    if m_int >= p:
        print('メッセージが大きすぎます: p より小さな整数に変換してください（短くするか分割を実装してください）')
        return

    c1, c2 = elgamal_encrypt(m_int, p, g, y)
    print('暗号化完了: ')
    print(f"c1={c1}")
    print(f"c2={c2}")

    # 4. 暗号文を長さ付きで送信
    send_len_prefixed_int(client_socket, c1)
    send_len_prefixed_int(client_socket, c2)

    print('暗号文を送信しました。')

if __name__ == '__main__':
    start_client()
