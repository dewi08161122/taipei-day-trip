import mysql.connector ,json ,jwt
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
from datetime import datetime, timedelta
app=FastAPI()
con = get_connection()
cursor=con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS member(" \
"id BIGINT unsigned not null primary key auto_increment," \
"name varchar(255) not null," \
"email varchar(255) not null," \
"password varchar(255) not null);"
)
con.commit()
SECRET_KEY = "11221122"
ALGORITHM = "HS256"

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
	con = get_connection()
	cursor=con.cursor()
	try:
		scheme, token = authorization.split()
		if token=="":
			return{"error":True}
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		cursor.execute("SELECT * FROM member WHERE id=%s and name=%s and email=%s",[payload["id"],payload["name"],payload["email"]])
		result=cursor.fetchone()
		if result==None:
			return{"error":True}
		else:
			return{"ok":True}
	except:
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