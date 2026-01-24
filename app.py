from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
app=FastAPI()

from controllers.user_controller import router as user_router
from controllers.attraction_controller import router as attraction_router
from controllers.booking_controller import router as booking_router
from controllers.order_controller import router as order_router

app.include_router(user_router)
app.include_router(attraction_router)
app.include_router(booking_router)
app.include_router(order_router)


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