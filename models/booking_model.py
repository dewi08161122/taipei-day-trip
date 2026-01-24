from infrastructure.connection import get_connection
import json

def increase_booking(user_id:int, attractionId:int, bookingDate:str, bookingTime:str, price:int):
    try:
        with get_connection() as con:
            with con.cursor() as cursor:
                cursor.execute("DELETE FROM booking WHERE userId = %s", [user_id])
                cursor.execute("INSERT INTO booking (userId,attractionId,bookingDate,bookingTime,price) VALUES(%s,%s,%s,%s,%s)",[user_id,attractionId, bookingDate, bookingTime, price])
                con.commit()	
                return True
    except Exception as e:
        print(e)
        return False


def get_booking_by_user(user_id:int):
    try:
        with get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT b.bookingDate, b.bookingTime, b.price, t.id AS attractionId, t.name, t.address, t.images FROM booking b JOIN travel t ON b.attractionId = t.id WHERE b.userId = %s",[user_id]) 
                result = cursor.fetchone()
            if not result:
                    return None
            images = json.loads(result["images"])
            result["first_image"] = images[0] if images else None
            data={
                "attraction": {
                    "id": result["attractionId"],
                    "name": result["name"],
                    "address": result["address"],
                    "image": result["first_image"]
                },
                "date": result["bookingDate"].isoformat(),
                "time": result["bookingTime"],
                "price": result["price"]
            }
            return data
    except Exception as e:
        print(e)

def delete_booking(user_id:int):
    try:
        with get_connection() as con:
            with con.cursor() as cursor:
                cursor.execute("DELETE FROM booking WHERE userId=%s",[user_id]) 
                con.commit()	
                return True
    except Exception as e:
        print(e)