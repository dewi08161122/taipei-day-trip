import mysql.connector ,json 
con=mysql.connector.connect(
	user="root",
	password="11221122",
	host="localhost",
	database="taipei"
)
with open("data/taipei-attractions.json", "r", encoding="utf-8") as file:
	data=json.load(file)
	cursor=con.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS travel(" \
	"id BIGINT unsigned not null primary key auto_increment," \
	"name varchar(255) not null," \
	"category varchar(255) not null," \
	"description TEXT not null," \
	"address varchar(255) not null," \
	"transport TEXT not null," \
	"mrt varchar(255) ," \
	"lat DECIMAL(10, 6),"\
	"log DECIMAL(10, 6),"\
	"images TEXT not null);"
	)

	for newdata in data["result"]["results"]:
		images=[]
		image=newdata["file"].split("https")
		for img in image:
			if img.lower().endswith((".jpg", ".png")): # .lower()是把img內容都轉成小寫來比對，.endswith是針對字尾比對
				images.append("https"+img)
		images_str = json.dumps(images) # json.dumps()可以把內容轉成json格式並保持結構
		category_clean = "".join(newdata['CAT'].split()) # 用split()分割文字再用"".join連起來去除空白
		cursor.execute("INSERT INTO travel(name,category,description,address,transport,MRT,lat,log,images) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",[newdata['name'],category_clean,newdata['description'],newdata['address'],newdata['direction'],newdata['MRT'],newdata['latitude'],newdata['longitude'],images_str])
		con.commit()
