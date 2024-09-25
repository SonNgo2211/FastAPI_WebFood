from fastapi import APIRouter, Request, HTTPException, Form, status, Depends, Response
from datetime import timedelta
from models.user import User
from db import conn
from schemas.user import userEntity, usersEntity
from bson import ObjectId
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from route import auth
from schemas.food import foodsEntity
from json import JSONDecodeError
from starlette.datastructures import FormData, URL


templates = Jinja2Templates(directory="templates")
templates.env.globals['URL'] = URL

user = APIRouter()

@user.get('/')
def get_home(response: Response, request: Request):
    foods = foodsEntity(conn.foodsell.foods.find())
    access_token = request.cookies.get('access_token')
    user = None
    if access_token != None:
        try:
            user = auth.get_current_user(access_token)
        except:
            response = templates.TemplateResponse("index.html", {"request":request, "current_user":user, "foods": foods})
            response.delete_cookie("access_token")
            return response
    return templates.TemplateResponse("index.html", {"request":request, "current_user":user, "foods": foods})

@user.get('/user_by_id')
async def find_one_user(id):
    user = conn.foodsell.users.find_one({"_id": ObjectId(id)})
    if user:
        return userEntity(user)
    return "Cannot find user"

@user.get('/user_by_username')
async def find_user_by_username(username):
    user = conn.foodsell.users.find_one({"username": username})
    if user:
        return userEntity(user)
    else:
        return "Cannot find user"

@user.post('/addUser')
async def create_user(user: User):
    conn.foodsell.users.insert_one(dict(user))
    return usersEntity(conn.foodsell.users.find())


@user.put('/editUser')
async def edit_user(username, user: User):
    conn.foodsell.users.find_one_and_update(
        {"username": username}, {"$set": dict(user)})
    return userEntity(conn.foodsell.users.find_one({"username": username}))


@user.delete('/deleteUser')
async def delete_user(username):
    return userEntity(conn.foodsell.users.find_one_and_delete({"username": username}))

@user.get('/login', response_class=HTMLResponse)
async def get_loginPage(request: Request):
    return templates.TemplateResponse("login.html", {"request":request})
    
@user.get('/register', response_class=HTMLResponse)
async def get_loginPage(request: Request):
    return templates.TemplateResponse("register.html", {"request":request})

# @user.post('/login')
# async def check_login(response: Response, 
#                       request: Request, 
#                       username: str = Form(...), password: str = Form(...)):
#     user = auth.authenticate_user(username, password)
#     if user:
#         access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = auth.create_access_token(
#             data={"sub": user["username"]}, expires_delta=access_token_expires)
#         response = RedirectResponse(
#             url=request.url_for("get_home"), 
#             status_code=status.HTTP_302_FOUND,
#         )
#         response.set_cookie(key="access_token", value =access_token, httponly=True)
#         return response
#     return templates.TemplateResponse("login.html", {'request': request, 'error':'The username or password is incorrect'})

# Test NoSQL Injection
async def get_body(request: Request):
    content_type = request.headers.get('Content-Type')
    if content_type is None:
        raise HTTPException(status_code=400, detail='No Content-Type provided!')
    elif content_type == 'application/json':
        try:
            return await request.json()
        except JSONDecodeError:
            raise HTTPException(status_code=400, detail='Invalid JSON data')
    elif (content_type == 'application/x-www-form-urlencoded' or
          content_type.startswith('multipart/form-data')):
        try:
            return await request.form()
        except Exception:
            raise HTTPException(status_code=400, detail='Invalid Form data')
    else:
        raise HTTPException(status_code=400, detail='Content-Type not supported!')

@user.post('/login')
async def check_login(response: Response, 
                      request: Request, 
                      body= Depends(get_body)):
    if isinstance(body, dict):
        query = {
            "username": body["username"],
            "password": body["password"]
        }
    elif isinstance(body, FormData):
        try: 
            query = {
                "username": body.get("username"),
                "password": body.get("password")
            }
        except JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON data")
    user = conn.foodsell.users.find_one(query)
    if user:
        user = userEntity(user)
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user["username"]}, expires_delta=access_token_expires)
        response = RedirectResponse(
            url=request.url_for("get_home"), 
            status_code=status.HTTP_302_FOUND,
        )
        response.set_cookie(key="access_token", value =access_token, httponly=True)
        return response
    return templates.TemplateResponse("login.html", {'request': request, 'error':'The username or password is incorrect'})

@user.post('/register')
async def submit_register(
    request: Request, fullname: str = Form(...),
    username: str = Form(...), email: str = Form(...),
    password: str = Form(...), repassword: str = Form(...)):
    user = auth.get_user(username)
    if user:
        return templates.TemplateResponse("register.html", {'request':request, 'error':'Username already exists'})
    if password != repassword:
        return templates.TemplateResponse("register.html", {'request':request, 'error':'Password & Confirm Password do not match'})
    newUser = User(fullname=fullname,username=username,email=email,password=auth.get_password_hash(password))
    conn.foodsell.users.insert_one(dict(newUser))
    return RedirectResponse(request.url_for("get_loginPage"), status_code=status.HTTP_302_FOUND)

@user.get('/logout')
async def logout_user(response: Response, request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie('access_token')
    return response


