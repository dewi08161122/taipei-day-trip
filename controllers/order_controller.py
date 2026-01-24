from fastapi import APIRouter, Body, Header
from models.order_model import increase_order,update_order,get_order
from models.member_model import get_member_by_email
from infrastructure.jwt import verify_token
from infrastructure.tappay import pay_by_tappay
from datetime import datetime,date

router = APIRouter()

@router.post("/api/orders")
def order(body: dict=Body(...),authorization: str=Header(None)):
    now = datetime.now()
    prime=body["prime"]
    attractionId=int(body["order"]["trip"]["attraction"]["id"])
    orderName=body["order"]["contact"]["name"]
    orderEmail=body["order"]["contact"]["email"]
    orderPhone=body["order"]["contact"]["phone"]
    orderDate=date.fromisoformat(body["order"]["trip"]["date"])
    orderTime=body["order"]["trip"]["time"]
    price=int(body["order"]["price"])
    paymentTime = now.strftime("%Y-%m-%d %H:%M:%S")
    status="unpaid"
    if authorization is None:
        return {"error": True, "message": "未登入系統，拒絕存取"}
    if not orderName or not orderEmail or not orderPhone:
        return {"error": True, "message": "請填寫聯絡資訊"}
    try:		
        payload = verify_token(authorization)
        if "error" in payload:
            return payload
        member = get_member_by_email(payload["data"]["email"])
        if member is None:
            return{"error":True,"message":"此帳號已暫停使用"}
        orderId = now.strftime("%Y%m%d%H%M%S") + str(payload["data"]["id"])
        increaseOrder=increase_order(orderId, payload["data"]["id"], attractionId, orderName, orderEmail, orderPhone, orderDate, orderTime, paymentTime, price , status)
        if increaseOrder:
            response=pay_by_tappay(prime, price, orderPhone, orderName, orderEmail)
            if response["status"] == 0:
                update_order(payload["data"]["id"], orderId)
                data={
                    "number": orderId,
                    "payment": {
                        "status": 0,
                        "message": "付款成功"
                    }
                }
                return{"data":data}
            else:
                data={
                    "number": orderId,
                    "payment": {
                        "status": response.get("status"),
                        "message": "付款失敗"
                    }
                }
                return {"error":True,"message":data}
        else:
            return{"error":True,"message":"訂單建立失敗"}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}


@router.get("/api/order/{orderNumber}")
def getorder(orderNumber: str,authorization: str=Header(None),):
    if authorization is None:
        return {"error": True, "message": "未登入系統，拒絕存取"}
    try:		
        payload = verify_token(authorization)
        if "error" in payload:
            return payload
        result = get_order(payload["data"]["id"],orderNumber)

        if result==None:
            return{"data": None}
        return{"data":result}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}
