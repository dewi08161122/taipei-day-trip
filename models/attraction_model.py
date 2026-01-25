from infrastructure.connection import get_connection
import json


def get_attraction_by_keyword(page: int = 0, category: str = None, keyword: str = None):
    page_size = 8
    offset = page * page_size
    try:
        with get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                sql = "SELECT * FROM travel WHERE 1=1"
                count_sql = "SELECT COUNT(*) as total FROM travel WHERE 1=1"
                values = []
                if category:
                    sql += " AND category = %s"
                    count_sql += " AND category = %s"
                    values.append(category)
                if keyword:
                    sql += " AND (mrt = %s OR name LIKE %s)"
                    count_sql += " AND (mrt = %s OR name LIKE %s)"
                    values.extend([keyword, f"%{keyword}%"])
                
                cursor.execute(count_sql, values)  # 資料數量條件組合取出
                total = cursor.fetchone()["total"] 
                sql += " LIMIT %s, %s"

                cursor.execute(sql, values + [offset, page_size]) # 資料內容條件組合取出
                result = cursor.fetchall()
                for i in result: 
                    i["images"] = json.loads(i["images"]) # 修改圖片格式
                next_page = page + 1 if total > (page + 1) * page_size else None
                return {"nextPage": next_page, "attractions": result}
    except Exception as e:
        print(e)

def get_attraction_by_id(attractionId: int):
    try:
        with get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM travel WHERE id=%s",[attractionId])
                result = cursor.fetchone()
                if result:
                    result["images"] = json.loads(result["images"])
                    return result
                return None
    except Exception as e:
        print(e)

def get_categories():
    try:
        with get_connection() as con:
            with con.cursor() as cursor:
                cursor.execute("SELECT DISTINCT category FROM travel") # DISTINCT 可以直接去除重複資料
                result = cursor.fetchall()
                categories=[i[0] for i in result]	
                return categories
    except Exception as e:
        print(e)

def get_mrts():
    try:
        with get_connection() as con:
            with con.cursor() as cursor:
                cursor.execute("SELECT mrt, COUNT(*) AS total FROM travel WHERE mrt IS NOT NULL GROUP BY mrt ORDER BY total DESC") # DISTINCT 可以直接去除重複資料
                result = cursor.fetchall()
                mrts=[i[0] for i in result ]	
                return mrts
    except Exception as e:
        print(e)