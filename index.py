from fastapi import FastAPI
import uvicorn
from route.user import user
from route.food import food
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from db import Base, engine


app = FastAPI()
app.include_router(user)
app.include_router(food)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
