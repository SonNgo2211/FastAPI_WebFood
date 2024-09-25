from fastapi import APIRouter, Request, HTTPException, Form, status, Body, Depends, Response
from datetime import timedelta
from models.cart import Cart, CartItem
from db import conn
from schemas.food import foodEntity, foodsEntity
from schemas.cart import CartEntity, CartItemEntity, CartItemsEntity, CartsEntity
from bson import ObjectId
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from route import auth
from datetime import datetime
from starlette.datastructures import URL


templates = Jinja2Templates(directory="templates")
templates.env.autoescape = False
templates.env.globals['URL'] = URL

cart = APIRouter()

@cart.get("/carts/getCart")
async def getCart(request: Request):
    access_token = request.cookies.get('access_token')
    user = None
    if access_token != None:
        try:
            user = auth.get_current_user(access_token)
            cart = conn.foodsell.carts.find_one({"u_id": user["u_id"]})
            if cart != None:
                cart = CartEntity(cart)
                items = cart['items']
                amount = 0
                for i in items:
                    amount += i['price'] * i['quantity']
                return {"cart":cart, "amount":amount}
        except:
            return {"cart":None, "amount":0}
    return {"cart":None, "amount":0}

@cart.post("/carts/addToCart")
async def addToCart(request: Request, response: Response,
                    fid: str = Body(...,embed=True), 
                    qty: int = Body(...,embed=True)):
    if qty <=0:
        raise HTTPException(status_code=500, detail="Quantity not valid")
    access_token = request.cookies.get('access_token')
    user = None
    if access_token != None:
        try:
            user = auth.get_current_user(access_token)
            cart = conn.foodsell.carts.find_one({"u_id": user["u_id"]})
            food = foodEntity(conn.foodsell.foods.find_one({"_id": ObjectId(fid)}))
            item = CartItem(quantity=qty, f_id=fid, price=food['price'], image=food['image'], fname=food['fname'])
            items = []
            amount = 0
            if cart != None:
                cart = CartEntity(cart)
                items = cart['items']
                if dict(item) in items:
                    index = items.index(dict(item))
                    newQty = items[index]["quantity"] + 1
                    items[index].update({"quantity":newQty}) 
                else:
                    items.append(dict(item))
                for i in items:
                    amount += i['price'] * i['quantity']
                cart = Cart(u_id=user['u_id'], items=items,amount=amount)
                cart.items = items
                conn.foodsell.carts.find_one_and_update({'u_id':user["u_id"]},{"$set":dict(cart)})
            else:
                items.append(dict(item))
                amount= item.price
                cart = Cart(u_id=user['u_id'], items=items,amount=amount)
                cart.items = items
                conn.foodsell.carts.insert_one(dict(cart))
            return amount
        except:
            raise HTTPException(status_code=500, detail="Server error")
    raise HTTPException(status_code=500, detail="Server error")

@cart.put("/carts/updateCart")
async def updateCart():
    return

@cart.delete("/carts/deleteCart")
async def deleteCart():
    return 
