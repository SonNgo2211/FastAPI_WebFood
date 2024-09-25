from fastapi import APIRouter, Request, Form, status, Depends, Response
from datetime import timedelta
from models.food import Food
from models.review import Review
from db import conn
from schemas.food import foodEntity, foodsEntity
from schemas.review import reviewEntity, reviewsEntity
from bson import ObjectId
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from route import auth
from datetime import datetime
from starlette.datastructures import URL


templates = Jinja2Templates(directory="templates")


food = APIRouter()

@food.get('/get_all_food')
async def find_all_food():
    foods = conn.foodsell.foods.find()
    return foodsEntity(foods)

@food.get('/get_food_by_id')
async def find_one_food(id):
    food = conn.foodsell.foods.find_one({"_id": ObjectId(id)})
    if food:
        return foodEntity(food)
    return "Cannot find food"

# @food.get('/get_food_by_name')
# async def find_food_by_name(fname):
#     food = conn.foodsell.foods.find_one({"fname": fname})
#     if food:
#         return foodEntity(food)
#     else:
#         return "Cannot find food"

@food.post('/addFood')
async def add_food(food: Food):
    conn.foodsell.foods.insert_one(dict(food))
    return foodsEntity(conn.foodsell.foods.find())


@food.put('/editFood')
async def edit_food(foodId, food: Food):
    conn.foodsell.foods.find_one_and_update(
        {"_id": ObjectId(foodId)}, {"$set": dict(food)})
    return foodEntity(conn.foodsell.foods.find_one({"_id": ObjectId(foodId)}))


@food.delete('/deleteFood')
async def delete_food(foodId):
    return foodEntity(conn.foodsell.foods.find_one_and_delete({"_id": ObjectId(foodId)}))


@food.get('/searchFood')
async def search_food(textsearch: str, response: Response, request: Request):
    query = {"fname": {"$regex": '.*' + textsearch + '.*', "$options": 'i'}}
    foods = foodsEntity(conn.foodsell.foods.find(query))
    result = None
    if not foods:
        foods = foodsEntity(conn.foodsell.foods.find())
        result = "Can't find food"
    else:
        result = f'''Results for: "{textsearch}" '''
    access_token = request.cookies.get('access_token')
    user = None
    if access_token != None:
        try:
            user = auth.get_current_user(access_token)
        except:
            response = templates.TemplateResponse("index.html", {"request":request, "current_user":user, "foods": foods, "result": result})
            response.delete_cookie("access_token")
            return response
    return templates.TemplateResponse("index.html", {"request":request, "current_user":user, "foods": foods, "result": result})


@food.get('/food/detail')
async def getDetailFoodById(request: Request, respose: Response, fid: str):
    food = foodEntity(conn.foodsell.foods.find_one({"_id":ObjectId(fid)}))
    reviews = reviewsEntity(conn.foodsell.reviews.find())
    return templates.TemplateResponse("detail.html", {"request":request, "food":food, "reviews": reviews})

@food.post('/food/review/save')
async def saveReview(request: Request, f_id: str = Form(...), content: str = Form(...)):
    access_token = request.cookies.get('access_token')
    user = None
    if access_token != None:
        try:
            user = auth.get_current_user(access_token)
            review = Review(f_id=f_id, user=dict(user), content=content, time= datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            conn.foodsell.reviews.insert_one(dict(review))
            url = URL(request.url_for("getDetailFoodById")).include_query_params(fid =f_id)
            return RedirectResponse(url, status_code=status.HTTP_302_FOUND)
        except:
            response = RedirectResponse(request.url_for("get_loginPage"), status_code=status.HTTP_302_FOUND)
            response.delete_cookie("access_token")
            return response
    return RedirectResponse(request.url_for("get_loginPage"), status_code=status.HTTP_302_FOUND)