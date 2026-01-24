from fastapi import APIRouter, Body, Header
from models.member_model import get_member_by_email,increase_member
from infrastructure.jwt import create_token,verify_token

router = APIRouter()

@router.post("/api/user")
def sign(body: dict=Body(...)):
    name=body["name"]
    email=body["email"]
    password=body["password"]
    try:
        member = get_member_by_email(email)
        if member is not None:
            return{"error":True,"message":"此信箱已被註冊"}
        success = increase_member(name, email, password)
        return{"ok":success}
            
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}

@router.get("/api/user/auth")
def check(authorization: str=Header(None)):
    if authorization is None:
        return {"error": True, "message": "未登入系統，拒絕存取"}
    try:
        payload = verify_token(authorization)
        if "error" in payload:
            return payload
        return {"ok":True, "data":payload["data"]}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}
    
@router.put("/api/user/auth")
def login(body: dict=Body(...)):
    email=body["email"]
    password=body["password"]
    try:
        member = get_member_by_email(email)
        if member==None:
            return{"error":True,"message":"信箱輸入錯誤"}
        elif member["password"]!=password:
            return{"error":True,"message":"密碼輸入錯誤"}
        else:
            token=create_token(member["id"], member["name"], member["email"])
            return{"token":token}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}