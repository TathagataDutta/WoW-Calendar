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

app = FastAPI()
templates = Jinja2Templates(directory="templates/")















if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8080, reload=True)