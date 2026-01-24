from fastapi import APIRouter, Body, Header
from models.booking_model import increase_booking,get_booking_by_user,delete_booking
from infrastructure.jwt import verify_token
from datetime import date

router = APIRouter()

@router.post("/api/booking")
def booking(body: dict=Body(...), authorization: str=Header(None)):
    attractionId=int(body["attractionId"])
    bookingDate = date.fromisoformat(body["bookingDate"]) # 把字串轉換成date型式
    bookingTime=body["bookingTime"]
    price=int(body["price"])
    if authorization is None:
        return {"error": True, "message": "未登入系統，拒絕存取"}
    if bookingDate < date.today():
        return {"error": True, "message": "不能選過去的日期"}
    try:
        payload = verify_token(authorization)
        if "error" in payload:
            return payload
        	
        result=increase_booking(payload["data"]["id"], attractionId, bookingDate, bookingTime, price)
        if result:
            return {"ok": True}
        else:
            return {"error": True, "message": "預約失敗，資料庫操作異常"}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}
    
@router.get("/api/booking")
def getbooking(authorization: str=Header(None)):
    if authorization is None:
        return {"error": True, "message": "未登入系統，拒絕存取"}
    try:
        payload = verify_token(authorization)
        if "error" in payload:
            return payload
        result = get_booking_by_user(payload["data"]["id"])

        if result==None:
            return{"data": None}
        return{"data":result}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}

@router.delete("/api/booking")
def cancle(authorization: str=Header(None)):
    if authorization is None:
        return {"error": True, "message": "未登入系統，拒絕存取"}
    try:
        payload = verify_token(authorization)
        if "error" in payload:
            return payload
        result = delete_booking(payload["data"]["id"])
        if result:
            return {"ok": True}
        else:
            return {"error": True, "message": "刪除失敗，資料庫操作異常"}

    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}
