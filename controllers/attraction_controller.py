from fastapi import APIRouter, Query
from models.attraction_model import get_attraction_by_keyword,get_attraction_by_id,get_categories,get_mrts

router = APIRouter()

@router.get("/api/attractions")
def getAttractions(page: int = Query(0, ge=0),category: str = Query(None), 
    keyword: str = Query(None)):
    try:
        attractions = get_attraction_by_keyword(page,category,keyword)
        if attractions is None: 
            return {"error": True, "message": "無法取得資料"}
        return{"nextPage":attractions["nextPage"],"data":attractions["attractions"]}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}
    
@router.get("/api/attraction/{attractionId}")
def getAttraction(attractionId: int):
    try:
        attraction = get_attraction_by_id(attractionId)
        if attraction is None: 
            return {"error": True, "message": "景點編號不正確"}
        return{"data":attraction}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}

@router.get("/api/categories")
def getCategories():
    try:
        categories = get_categories()
        return{"data":categories}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}
    
@router.get("/api/mrts")
def getMrts():
    try:
        mrts = get_mrts()
        return{"data":mrts}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}	