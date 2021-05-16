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

def user_exists(username):
    user_exist = True
    if connection.db.user_info.find({'user_id': username}).count() == 0:
        user_exist = False
    return user_exist

def check_login_creds(username, password):
    # if not user_exists(username):
    if user_exists(username):
        active_user = connection.db.user_info.find({'user_id': username}) # , 'user_pw': password})

        # convert to dict with string
        for actuser in active_user:
            actuser = dict(actuser)
            actuser['_id'] = str(actuser['_id'])
            return actuser



app = FastAPI()
# templates = Jinja2Templates(directory="templates/")


@app.get("/")
def index():
    return {"message": "Hello World"}


# Signup endpoint with the POST method
@app.post("/signup/{username}/{password}")
def signup(username: str, password: str):
    user_exists = False
    data = create_user(username, password)


    # Checks if an username exists from the collection of users
    if connection.db.user_info.find({'user_id': data['user_id']}).count() > 0:
        user_exists = True
        print("User Exists")
        return {"message": "User Exists"}
    # If the email doesn't exist, create the user
    elif user_exists == False:
        connection.db.user_info.insert_one(data)
        return {"message":"User Created", "user_id": data['user_id'], "user_pw": data['user_pw']}



# Login endpoint
@app.get("/login/{username}/{password}")
def login(username, password):
    def log_user_in(creds):
        if creds['user_id'] == username and creds['user_pw'] == password:
            return {"message": creds['user_id'] + ' successfully logged in'}
        else:
            return {"message": "Invalid credentials!!"}
    # Read user_id from database to validate if user exists and checks if password matches
    logger = check_login_creds(username, password)
    print(logger)
    if bool(logger) != True:
        if logger == None:
            logger = "Invalid user_id"
            return {"message": logger}
    else:
        status = log_user_in(logger)
        return {"Info": status}






if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080, workers=2, reload=True)