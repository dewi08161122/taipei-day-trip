from infrastructure.connection import get_connection
import json

def increase_order(orderId:str, user_id:int, attractionId:int, orderName:str, orderEmail:str, orderPhone:str, orderDate:str, orderTime:str, paymentTime:str, price:int , status:str):
    try:
        with get_connection() as con:
            with con.cursor() as cursor:
                cursor.execute("INSERT INTO orders (orderId,userId,attractionId,orderName,orderEmail,orderPhone,orderDate,orderTime,paymentTime,price,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[orderId, user_id,attractionId, orderName, orderEmail, orderPhone, orderDate, orderTime, paymentTime, price, status])
                con.commit()	
                return True
    except Exception as e:
        print(e)
        return False
    
def update_order(user_id:int, orderId:str):
    try:
        with get_connection() as con:
            with con.cursor() as cursor:
                cursor.execute("UPDATE orders SET status=%s WHERE orderId=%s",["paid",orderId])
                cursor.execute("DELETE FROM booking WHERE userId=%s",[user_id])	
                con.commit()
                return True
    except Exception as e:
        print(e)
        return False
    
def get_order(user_id:int, orderNumber:str):
    try:
        with get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT o.*, t.id AS attraction_id, t.name AS attraction_name, t.address AS attraction_address, t.images AS attraction_images FROM orders o INNER JOIN travel t ON t.id=o.attractionId WHERE o.userId =%s AND o.orderId=%s",[user_id, orderNumber])
                result=cursor.fetchone()
                if not result:
                    return None
                images = json.loads(result["attraction_images"])
                result["first_image"] = images[0] if images else None
                data={
                    "number": result["orderId"],
                    "price": int(result["price"]),
                    "trip": {
                        "attraction": {
                            "id": int(result["attraction_id"]),
                            "name": result["attraction_name"],
                            "address": result["attraction_address"],
                            "image": result["first_image"]
                        },
                        "date": result["orderDate"].isoformat(),
                        "time": result["orderTime"]
                    },
                    "contact": {
                        "name": result["orderName"],
                        "email": result["orderEmail"],
                        "phone": result["orderPhone"]
                    },
                    "status": result["status"]
                }
                return data
    except Exception as e:
        print(e)
        return False