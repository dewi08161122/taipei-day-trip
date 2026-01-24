import jwt
import os 
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
SECRET_KEY = os.getenv("JWT_KEY")
ALGORITHM = "HS256"

def create_token(user_id, name, email):
    payload = {
				"id": user_id,
				"name": name,
				"email": email,
				"exp": datetime.now() + timedelta(days=7)
			}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(authorization: str):
    if not authorization:
        return {"error": True, "message": "未登入系統，拒絕存取"}
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"data":payload}
    except jwt.ExpiredSignatureError:
        return {"error": True, "message": "登入狀態已逾時"}
    except:
        return {"error": True, "message": "登入狀態無效"}