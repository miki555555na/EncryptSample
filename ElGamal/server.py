import socket
import secrets
import random

def recv_exact(sock, n):
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError('socket closed')
        data += chunk
    return data

def recv_len_prefixed_int(sock):
    len_b = recv_exact(sock, 2)
    L = int.from_bytes(len_b, 'big')
    data = recv_exact(sock, L)
    return int.from_bytes(data, 'big')

def send_len_prefixed_int(sock, v):
    b = v.to_bytes((v.bit_length() + 7) // 8 or 1, 'big')
    sock.sendall(len(b).to_bytes(2, 'big'))
    sock.sendall(b)

def is_prime(n, k=40):
    """Miller-Rabin素数判定法で素数判定"""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

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
        num = secrets.randbits(bits)
        num |= (1 << (bits - 1)) | 1
        if is_prime(num):
            return num

def find_generator(p):
    """pの原始元を見つける（簡易的な方法）"""
    for _ in range(1000):
        g = random.randrange(2, p - 1)
        if pow(g, p - 1, p) == 1 and g != 1:
            return g
    return 2

def start_server():
    # 1. ソケットの設定 (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 50007)) # ローカルホストのポート50007
    server_socket.listen(1)

    print("サーバー起動：クライアントの接続を待っています...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"接続されました: {addr}")

        # 2. 公開鍵・秘密鍵の生成
        p_bits = 256
        p = generate_prime(p_bits) # 256ビットの素数を生成
        g = find_generator(p) # pの原始元を見つける（簡易的な方法）
        x = secrets.randbelow(p - 2) + 1
        y = pow(g, x, p)

        print('公開鍵(p,g,y)を送信しました')
        send_len_prefixed_int(conn, p)
        send_len_prefixed_int(conn, g)
        send_len_prefixed_int(conn, y)

        # 暗号文を受信
        c1 = recv_len_prefixed_int(conn)
        c2 = recv_len_prefixed_int(conn)
        print('受信: c1=', c1)
        print('受信: c2=', c2)

        # 復号: m = c2 * s^{-1} mod p, s = c1^x
        s = pow(c1, x, p)
        # inverse via Fermat
        inv_s = pow(s, p - 2, p)
        m = (c2 * inv_s) % p

        # バイト列にして表示
        m_len = (m.bit_length() + 7) // 8 or 1
        m_bytes = m.to_bytes(m_len, 'big')
        try:
            text = m_bytes.decode('utf-8')
        except Exception:
            text = repr(m_bytes)

        print('復号結果:', text)

if __name__ == '__main__':
    start_server()
