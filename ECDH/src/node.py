import json

class ECCNode:
    """サーバー・クライアント共通のECCノードクラス"""
    def __init__(self, curve, gen_point):
        self.curve = curve
        self.gen_point = gen_point
        self.private_key = None
        self.public_key = None
    
    def generate_keys(self, secret_int):
        #秘密鍵を生成し、公開鍵を計算
        self.private_key = secret_int
        self.public_key = self.curve.mul(secret_int, self.gen_point)
        return self.public_key, self.private_key
    
    def compute_shared_secret(self, other_public_key):
        #相手の公開鍵から共有秘密を計算
        if self.private_key is None:
            raise ValueError("秘密鍵が生成されていません")
        return self.curve.mul(self.private_key, other_public_key)
    
    def serialize_public_key(self):
        #公開鍵をJSON形式でシリアライズ
        if self.public_key is None:
            raise ValueError("公開鍵が生成されていません")
        return json.dumps({'x': self.public_key.x, 'y': self.public_key.y})
