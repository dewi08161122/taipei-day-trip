import mysql.connector ,json ,jwt
import mysql.connector.pooling
def get_connection():
	return mysql.connector.connect(
		user="root",
		password="11221122",
		host="localhost",
		database="taipei"
		)
from fastapi import FastAPI, Body, Request, Query, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta, date
import requests
app=FastAPI()
con = get_connection()
cursor=con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS member(" \
"id BIGINT unsigned not null primary key auto_increment," \
"name varchar(255) not null," \
"email varchar(255) not null," \
"password varchar(255) not null);"
)
cursor.execute("CREATE TABLE IF NOT EXISTS booking(" \
"id BIGINT unsigned not null primary key auto_increment," \
"userId BIGINT unsigned not null," \
"attractionId BIGINT unsigned not null," \
"bookingDate DATE not null," \
"bookingTime varchar(255) not null," \
"price INT not null," \
"FOREIGN KEY (attractionId) REFERENCES travel (id)," \
"FOREIGN KEY (userId) REFERENCES member (id));"
)
cursor.execute("CREATE TABLE IF NOT EXISTS orders(" \
"id BIGINT unsigned not null primary key auto_increment," \
"orderId VARCHAR(255) NOT NULL," \
"userId BIGINT unsigned not null," \
"attractionId BIGINT unsigned not null," \
"orderName varchar(255) not null," \
"orderEmail varchar(255) not null," \
"orderPhone varchar(255) not null," \
"orderDate DATE not null," \
"orderTime varchar(255) not null," \
"paymentTime varchar(255) null," \
"price INT not null," \
"status varchar(255) not null," \
"FOREIGN KEY (attractionId) REFERENCES travel (id)," \
"FOREIGN KEY (userId) REFERENCES member (id));"
)
con.commit()
SECRET_KEY = "11221122"
ALGORITHM = "HS256"
partner_key="partner_L4JiZnrr7qnfKI4BOTiOKWiRRLCp5HspdM5iqR3JDfsns9OGqPFFN3eH"
merchant_id="1122yes_GP_POS_2"

@app.post("/api/user")
def sign(body: dict=Body(...)):
	name=body["name"]
	email=body["email"]
	password=body["password"]
	try:
		con = get_connection()
		cursor=con.cursor()
		cursor.execute("SELECT * FROM member WHERE email=%s",[email])
		result=cursor.fetchone()
		if result==None:
			cursor.execute("INSERT INTO member(name,email,password) VALUES(%s,%s,%s)",[name, email, password])
			con.commit()
			return{"ok":True}
		else:
			return{"error":True,"message":"此信箱已被註冊"}
	except:
		return{"error":True,"message":"伺服器出現未知問題"}

@app.get("/api/user/auth")
def check(authorization: str=Header(None)):
	if authorization is None:
		return {"error": True, "message": "未登入系統，拒絕存取"}
	try:		
		scheme, token = authorization.split()
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		return{"ok":True, "data":payload}
	except :
		return{"error":True}
	
@app.put("/api/user/auth")
def login(body: dict=Body(...)):
	email=body["email"]
	password=body["password"]
	con = get_connection()
	cursor=con.cursor()
	try:
		cursor.execute("SELECT * FROM member WHERE email=%s",[email])
		result=cursor.fetchone()
		if result==None:
			return{"error":True,"message":"信箱輸入錯誤"}
		elif result[3]!=password:
			return{"error":True,"message":"密碼輸入錯誤"}
		else:
			payload = {
				"id": result[0],
				"name": result[1],
				"email": result[2],
				"exp": datetime.now() + timedelta(days=7)
			}
			token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
			return{"token":token}
	except:
		return{"error":True,"message":"伺服器內部錯誤"}

@app.get("/api/attractions")
def search(page: int = Query(0, ge=0),category: str = Query(None), 
    keyword: str = Query(None)):
	con = get_connection()
	cursor=con.cursor()
	try:
		if category == None and keyword == None:
			cursor.execute("SELECT COUNT(*) FROM travel")
			total=cursor.fetchone()[0]
			cursor.execute("SELECT * FROM travel LIMIT %s,%s",[page*8,8])
		elif keyword==None:
			cursor.execute("SELECT COUNT(*) FROM travel WHERE category=%s",[category])
			total=cursor.fetchone()[0]
			cursor.execute("SELECT * FROM travel WHERE category=%s LIMIT %s,%s",[category,page*8,8])
		elif category ==None:
			likekeyword="%"+keyword+"%"
			cursor.execute("SELECT COUNT(*) FROM travel WHERE mrt=%s OR name LIKE %s",[keyword,likekeyword])
			total=cursor.fetchone()[0]
			cursor.execute("SELECT * FROM travel WHERE mrt=%s OR name LIKE %s LIMIT %s,%s",[keyword,likekeyword,page*8,8])
		else:
			likekeyword="%"+keyword+"%"
			cursor.execute("SELECT COUNT(*) FROM travel WHERE  category=%s OR mrt=%s OR name LIKE %s",[category,keyword,likekeyword])
			total=cursor.fetchone()[0]
			cursor.execute("SELECT * FROM travel WHERE category=%s OR mrt=%s OR name LIKE %s LIMIT %s,%s",[category,keyword,likekeyword,page*8,8])
		if total/8 < page+1:
			nextpage=None
		else:
			nextpage=page+1

		result=cursor.fetchall()
		data=[]
		for i in result:
			data1={"id":i[0],
				"name":i[1],
				"category":i[2],
				"description":i[3],
				"address":i[4],
				"transport":i[5],
				"mrt":i[6],
				"lat":i[7],
				"lng":i[8],
				"images":json.loads(i[9]),
			}
			data.append(data1)
		return{"nextpage":nextpage,"data":data}
	except:
		return{"error":True,"message":"伺服器內部錯誤"}

@app.get("/api/attraction/{attractionId}")
def searchID(attractionId: int):
	con = get_connection()
	cursor=con.cursor()
	try:
		cursor.execute("SELECT * FROM travel WHERE id=%s",[attractionId])
		result=cursor.fetchone()
		if result==None:
			return{"error":True,"message":"景點編號不正確"}
		else:
			data={
				"id": result[0],
				"name": result[1],
				"category": result[2],
				"description": result[3],
				"address": result[4],
				"transport": result[5],
				"mrt": result[6],
				"lat": result[7],
				"lng": result[8],
				"images": json.loads(result[9])
			}
			return{"data":data}
	except:
		return{"error":True,"message":"伺服器內部錯誤"}

@app.get("/api/categories")
def listCategories():
	con = get_connection()
	cursor=con.cursor()
	try:
		cursor.execute("SELECT DISTINCT category FROM travel") # DISTINCT 可以直接去除重複資料
		result=cursor.fetchall()
		data=[i[0] for i in result]				
		return{"data":data}
	except:
		return{"error":True,"message":"伺服器內部錯誤"}

@app.get("/api/mrts")
def listMrts():
	con = get_connection()
	cursor=con.cursor()
	try:
		cursor.execute("SELECT mrt, COUNT(*) AS total FROM travel GROUP BY mrt ORDER BY total DESC")
		result=cursor.fetchall()
		data=[i[0] for i in result if i[0] != None]			
		return{"data":data}
	except:
		return{"error":True,"message":"伺服器內部錯誤"}

@app.get("/api/booking")
def getbooking(authorization: str=Header(None)):
	try:
		if authorization is None:
			return {"error": True, "message": "未登入系統，拒絕存取"}
		con = get_connection()
		cursor=con.cursor()
		scheme, token = authorization.split()
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		cursor.execute("SELECT * FROM member WHERE id=%s and name=%s and email=%s",[payload["id"],payload["name"],payload["email"]])
		result=cursor.fetchone()
		if result==None:
			return{"error":True, "message": "未登入系統，拒絕存取"}
		cursor.execute("SELECT * FROM booking WHERE userId=%s",[payload["id"]])
		result=cursor.fetchone()
		if result==None:
			return{"data": None}
		cursor.execute("SELECT * FROM travel WHERE id=%s",[result[2]])
		resultAttraction=cursor.fetchone()
		images = json.loads(resultAttraction[9])
		data={
			"attraction": {
				"id": resultAttraction[0],
				"name": resultAttraction[1],
				"address": resultAttraction[4],
				"image": images[0]
			},
			"date": result[3].isoformat(),
			"time": result[4],
			"price": result[5]
		}
		return{"data":data}
	except:
		return{"error":True,"message":"伺服器出現未知問題"}

@app.post("/api/booking")
def booking(body: dict=Body(...), authorization: str=Header(None)):
	attractionId=int(body["attractionId"])
	bookingDate = date.fromisoformat(body["bookingDate"]) # 把字串轉換成date型式
	bookingTime=body["bookingTime"]
	price=int(body["price"])
	try:
		if authorization is None:
			return {"error": True, "message": "未登入系統，拒絕存取"}
		con = get_connection()
		cursor=con.cursor()
		scheme, token = authorization.split()
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		cursor.execute("SELECT * FROM member WHERE id=%s and name=%s and email=%s",[payload["id"],payload["name"],payload["email"]])
		result=cursor.fetchone()
		cursor.execute("SELECT * FROM booking WHERE userId=%s",[payload["id"]])
		resultBooking=cursor.fetchone()
		if result==None:
			return{"error":True, "message": "未登入系統，拒絕存取"}
		elif bookingDate < date.today():
			return {"error": True, "message": "不能選過去的日期"}
		elif resultBooking != None:
			cursor.execute("DELETE FROM booking WHERE userId=%s",[payload["id"]])
		cursor.execute("INSERT INTO booking (userId,attractionId,bookingDate,bookingTime,price) VALUES(%s,%s,%s,%s,%s)",[payload["id"],attractionId, bookingDate, bookingTime, price])
		con.commit()
		return{"ok":True}
	except:
		return{"error":True,"message":"伺服器出現未知問題"}

@app.delete("/api/booking")
def cancle(authorization: str=Header(None)):
	try:
		if authorization is None:
			return {"error": True, "message": "未登入系統，拒絕存取"}
		con = get_connection()
		cursor=con.cursor()
		scheme, token = authorization.split()
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		cursor.execute("SELECT * FROM member WHERE id=%s and name=%s and email=%s",[payload["id"],payload["name"],payload["email"]])
		result=cursor.fetchone()
		if result==None:
			return{"error":True, "message": "未登入系統，拒絕存取"}
		else:
			cursor.execute("DELETE FROM booking WHERE userId=%s",[payload["id"]])
			con.commit()
			return{"ok":True}
	except:
		return{"error":True,"message":"伺服器出現未知問題"}

@app.post("/api/orders")
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
		con = get_connection()
		cursor=con.cursor()
		scheme, token = authorization.split()
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		id=int(payload["id"])
		orderId = now.strftime("%Y%m%d%H%M%S") + str(id)
		cursor.execute("INSERT INTO orders (orderId,userId,attractionId,orderName,orderEmail,orderPhone,orderDate,orderTime,paymentTime,price,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[orderId, id,attractionId, orderName, orderEmail, orderPhone, orderDate, orderTime, paymentTime, price, status])
		con.commit()
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
			"amount": price,
			"cardholder": {
				"phone_number": orderPhone,
				"name": orderName,
				"email": orderEmail,
				},
				"remember": False
			}
		response = requests.post(url, json=body, headers=headers).json()
		if response["status"] == 0:
			cursor.execute("UPDATE orders SET status=%s WHERE orderId=%s",["paid",orderId])
			cursor.execute("DELETE FROM booking WHERE userId=%s",[id])
			con.commit()
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
	except:
		return{"error":True,"message":"伺服器出現未知問題"}
	finally:
		if con and con.is_connected():
			cursor.close()
			con.close()

@app.get("/api/order/{orderNumber}")
def getbooking(orderNumber: str,authorization: str=Header(None),):
	if authorization is None:
		return {"error": True, "message": "未登入系統，拒絕存取"}
	try:		
		con = get_connection()
		cursor=con.cursor()
		scheme, token = authorization.split()
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		id=int(payload["id"])
		cursor.execute("SELECT o.*, t.id AS attraction_id, t.name AS attraction_name, t.address AS attraction_address, t.images AS attraction_images FROM orders o INNER JOIN travel t ON t.id=o.attractionId WHERE o.userId =%s AND o.orderId=%s",[id, orderNumber])
		result=cursor.fetchone()
		print(result)
		image = json.loads(result[15])
		data={
			"number": result[1],
			"price": int(result[10]),
			"trip": {
				"attraction": {
					"id": int(result[12]),
					"name": result[13],
					"address": result[14],
					"image": image
				},
				"date": result[7],
				"time": result[8]
			},
			"contact": {
				"name": result[4],
				"email": result[5],
				"phone": result[6]
			},
			"status": result[11]
		}
		return{"data":data}
	except:
		return{"error":True,"message":"伺服器出現未知問題"}


# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")

app.mount("/css", StaticFiles(directory="public/css"), name="css")
app.mount("/js", StaticFiles(directory="public/javascript"), name="js")
app.mount("/img", StaticFiles(directory="public/image"), name="img")
app.mount("/", StaticFiles(directory="static", html=True))