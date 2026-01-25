import json 
from infrastructure.connection import get_connection

try:
	with open("data/taipei-attractions.json", "r", encoding="utf-8") as file:
		data=json.load(file)
	with get_connection() as con:
		with con.cursor() as cursor:
			cursor.execute("CREATE TABLE IF NOT EXISTS travel(" \
			"id BIGINT unsigned not null primary key auto_increment," \
			"name varchar(255) not null," \
			"category varchar(255) not null," \
			"description TEXT not null," \
			"address varchar(255) not null," \
			"transport TEXT not null," \
			"mrt varchar(255) ," \
			"lat DECIMAL(10, 6),"\
			"lng DECIMAL(10, 6),"\
			"images TEXT not null);"
			)
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

			for newdata in data["result"]["results"]:
				images=[]
				image=newdata["file"].split("https")
				for img in image:
					if img.lower().endswith((".jpg", ".png")): # .lower()是把img內容都轉成小寫來比對，.endswith是針對字尾比對
						images.append("https"+img)
				images_str = json.dumps(images) # json.dumps()可以把內容轉成json格式並保持結構
				category_clean = "".join(newdata['CAT'].split()) # 用split()分割文字再用"".join連起來去除空白
				cursor.execute("INSERT INTO travel(name,category,description,address,transport,MRT,lat,lng,images) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",[newdata['name'],category_clean,newdata['description'],newdata['address'],newdata['direction'],newdata['MRT'],newdata['latitude'],newdata['longitude'],images_str])			
			con.commit()
except Exception as e:
    print(f"初始化資料庫失敗: {e}")