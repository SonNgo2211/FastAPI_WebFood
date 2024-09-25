from pymongo import MongoClient
import pymongo
from dotenv import dotenv_values

# config = dotenv_values(".env")

# conn = MongoClient(config.get("DATABASE_CONNECTION_URL"))
conn = MongoClient('mongodb+srv://sonngo:son221101@cluster0.zjjgol6.mongodb.net/')

db = conn["foodsell"]