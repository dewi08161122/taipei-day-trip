import os 
from dotenv import load_dotenv
import requests

load_dotenv()
partner_key = os.getenv("PARTNER_KEY")
merchant_id = os.getenv("MERCHANT_ID")

def pay_by_tappay(prime, price:int, orderPhone, orderName, orderEmail):
    url="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    headers={
        "Content-Type": "application/json",
        "x-api-key" : partner_key
        }
    body={
        "prime": prime,
        "partner_key": partner_key,
        "merchant_id": merchant_id,
        "details":"TapPay Test",
        "amount": int(price),
        "cardholder": {
            "phone_number": orderPhone,
            "name": orderName,
            "email": orderEmail,
            },
            "remember": False
        }
    try:
        response =requests.post(url, json=body, headers=headers, timeout=10) # 加上時間限制確保程式不會無限期等待
        response.raise_for_status() # 即使出現報錯依然會回傳一個 response 物件防止解析json炸掉
        return response.json()

    except Exception as e:
        print(e)
        return {"status": -1, "msg": "與支付閘道連線失敗"}