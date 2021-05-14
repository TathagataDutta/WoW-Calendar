from typing import Optional

from fastapi import FastAPI, Request
import uvicorn
import connection
from bson import ObjectId
from schematics.models import Model
from fastapi.templating import Jinja2Templates
from schematics.types import StringType

class User(Model):
    _id = ObjectId()
    user_id = StringType(required=True)
    user_pw = StringType(required=True)

# An instance of class User
newuser = User()

# funtion to create and assign values to the instanse of class User created
def create_user(username, password):
    newuser._id = ObjectId()
    newuser.user_id = username
    newuser.user_pw = password
    return dict(newuser)

# def user_exists(username):
#     user_exist = True
#     if connection.db.user.info.find({'user_id': username}).count() == 0:
#         user_exist = False
#     return user_exist

# def check_login_creds(username, password):
#     if not user_exists(username):
#         activeuser = connection.db.users.find({'user_id': username})
#         for actuser in activeuser:
#             actuser = dict(actuser)
#             actuser['_id'] = str(actuser['_id'])    
#             return actuser



app = FastAPI()
templates = Jinja2Templates(directory="templates/")


@app.get("/")
def index():
    return {"message": "Hello World"}


# Signup endpoint with the POST method
@app.post("/signup/{email}/{username}/{password}")
def signup(email, username: str, password: str):
    user_exists = False
    data = create_user(email, username, password)

    # Covert data to dict so it can be easily inserted to MongoDB
    dict(data)

    # Checks if an email exists from the collection of users
    if connection.db.users.find(
        {'email': data['email']}
        ).count() > 0:
        user_exists = True
        print("USer Exists")
        return {"message":"User Exists"}
    # If the email doesn't exist, create the user
    elif user_exists == False:
        connection.db.users.insert_one(data)
        return {"message":"User Created","email": data['email'], "name": data['name'], "pass": data['password']}









if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8080, reload=True)