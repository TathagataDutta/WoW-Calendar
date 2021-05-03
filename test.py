# import pymongo
from flask_pymongo import MongoClient

CON_STR = "mongodb+srv://td:hello123@cluster0.y21dr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

cluster = MongoClient(CON_STR)

db = cluster['db1']

colc = db['colc1']

cluster.close()