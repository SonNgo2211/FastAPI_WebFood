from fastapi import FastAPI
import uvicorn
from route.user import user
from route.food import food
from route.cart import cart
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
ORIGINS = ['*']

app = FastAPI()
app.include_router(user)
app.include_router(food)
app.include_router(cart)

app.add_middleware(
            CORSMiddleware,
            allow_origins=ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
