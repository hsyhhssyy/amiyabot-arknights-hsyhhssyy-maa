
from ..server.check_password import get_password

import base64
import hmac
import json

# 定义Header和Payload
header = {
    "alg": "HS256",
    "typ": "JWT"
}


def get_jwt(uuid:str):

    payload = {
        "sub": "amiyabot-arknights-hsyhhssyy-maa",
    }


    # 定义Secret Key
    secret_key = get_password() + "U" + uuid

    # 编码Header和Payload
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")

    # 生成Signature
    message = f"{header_encoded}.{payload_encoded}".encode()
    signature = hmac.new(secret_key.encode(), message, digestmod="SHA256").digest()
    signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    # 生成JWT
    jwt = f"{header_encoded}.{payload_encoded}.{signature_encoded}"

    return jwt

def check_jwt(jwt:str,uuid:str):

    jwt_parts = jwt.split(".")
    secret_key = get_password() + "U" + uuid
    
    try:

        header_decoded = json.loads(base64.urlsafe_b64decode(jwt_parts[0] + "==").decode())
        payload_decoded = json.loads(base64.urlsafe_b64decode(jwt_parts[1] + "==").decode())

        # 验证Signature
        message = f"{jwt_parts[0]}.{jwt_parts[1]}".encode()
        signature = hmac.new(secret_key.encode(), message, digestmod="SHA256").digest()
        signature_decoded = base64.urlsafe_b64decode(jwt_parts[2] + "==")
        if not hmac.compare_digest(signature, signature_decoded):
            return False
    
        if payload_decoded.sub != "amiyabot-arknights-hsyhhssyy-maa":
            return False
        
        return True
    except Exception as e:
        return False
