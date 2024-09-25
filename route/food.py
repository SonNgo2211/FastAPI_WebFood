from fastapi import APIRouter, Request, Form, status, Depends, Response, HTTPException
from datetime import timedelta
from models.food import Food, FoodModel
from models.review import Review
from sqlalchemy.orm import Session
from db import get_db
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
async def find_all_food(db: Session = Depends(get_db)):
    foods = db.query(Food).all()
    return foodsEntity(foods)

@food.get('/get_food_by_id')
async def find_one_food(id, db: Session = Depends(get_db)):
    food = db.query(Food).filter(Food.id == id).first()
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
async def add_food(food: Food, db: Session = Depends(get_db)):
    db.add(food)
    db.commit()
    db.refresh(food)
    return foodsEntity(db.query(Food).all())


@food.put('/editFood')
async def edit_food(foodId, food_update: Food, db: Session = Depends(get_db)):
    food = db.query(Food).filter(Food.id == foodId)
    for key, value in food_update.dict().items():
        setattr(food, key, value)
    db.commit() 
    db.refresh(food)
    return foodEntity(food)


@food.delete('/deleteFood')
async def delete_food(foodId, db: Session = Depends(get_db)):
    food = db.query(Food).filter(Food.id == foodId).first()
    if not food:
        raise HTTPException(status_code=404, detail="User not found")  # Kiểm tra nếu người dùng không tồn tại

    db.delete(food)  # Xóa người dùng
    db.commit()
    return foodEntity(food)


@food.get('/searchFood')
async def search_food(textsearch: str, response: Response, request: Request, db: Session = Depends(get_db)):
    foods = db.query(FoodModel).filter(FoodModel.fname.ilike(f'%{textsearch}%')).all()
    result = None
    if not foods:
        foods = foodsEntity(db.query(FoodModel).all())
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
async def getDetailFoodById(request: Request, respose: Response, fid: int, db: Session = Depends(get_db)):
    food = foodEntity(db.query(Food).filter(Food.id == fid).first())
    reviews = reviewsEntity(db.query(Review).all())
    return templates.TemplateResponse("detail.html", {"request":request, "food":food, "reviews": reviews})

@food.post('/food/review/save')
async def saveReview(request: Request, f_id: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    access_token = request.cookies.get('access_token')
    user = None
    if access_token != None:
        try:
            user = auth.get_current_user(access_token)
            review = Review(f_id=f_id, user=dict(user), content=content, time= datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.add(review)
            db.commit()
            db.refresh(review)
            url = URL(request.url_for("getDetailFoodById")).include_query_params(fid =f_id)
            return RedirectResponse(url, status_code=status.HTTP_302_FOUND)
        except:
            response = RedirectResponse(request.url_for("get_loginPage"), status_code=status.HTTP_302_FOUND)
            response.delete_cookie("access_token")
            return response
    return RedirectResponse(request.url_for("get_loginPage"), status_code=status.HTTP_302_FOUND)