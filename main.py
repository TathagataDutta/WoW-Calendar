from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import connection
from bson import ObjectId
from bson.json_util import loads, dumps
from datetime import datetime, timedelta
import pandas as pd
import json


class User(BaseModel):
    _id: ObjectId
    user_id: str
    user_pw: str

class Raid(BaseModel):
    _id: ObjectId()
    user_id: str
    char_name: str
    raid_name: str
    guild_or_discord_name: str
    start_date_and_time: datetime
    # has to be positive, (is in seconds)
    approx_duration: timedelta


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DEFAULT PAGE
@app.get("/")
async def default():
    return {"message": "HomePage"}




# USER SIGN UP
@app.post("/user_signup/")
async def user_signup(user: User):
    # convert to a dict
    d = dict(user)
    user_id = d['user_id']
    user_pw = d['user_pw']

    if connection.db.user_info.count_documents({'user_id': user_id}, limit = 1) != 0:
        # print("User already exists. Try again.")
        return {"message": "User Exists"}
    else:
        connection.db.user_info.insert_one({"user_id": user_id, "user_pw": user_pw})
        bson_data = connection.db.user_info.find_one({'user_id': user_id})
        json_data = dumps(bson_data)
        return {"status": "success", "data": json_data}

        return {"message": "User Created", "user_id": d['user_id'], "user_pw": d['user_pw']}

        # print(dict(connection.db.user_info.find_one({"user_id": user_id}, {"_id": 0})))
        # return json.dumps(dict(connection.db.user_info.find_one({"user_id": user_id})))
        # return {"a": "aa"}

# # USER LOG IN
# @app.get("/user_login/{user_id}/{user_pw}")
# async def user_login(user_id: str, user_pw: str):
#     # if user_id exists
#     if connection.db.user_info.count_documents({'user_id': user_id}, limit = 1) != 0:
#         # check if password is correct
#         if connection.db.user_info.count_documents({'user_id': user_id, 'user_pw': user_pw}, limit = 1) != 0:
#             print("Successfully logged in!")
#             return {"message": user_id + " successfully logged in."}
#         # if password incorrect
#         else:
#             return {"message": "Invalid credentials."}
        
#     # if user_id does not exist
#     else:
#         print("Incorrect ID or Password or User doesn't exist. Try again.")
#         return {"message": "user_id does not exist."}

# USER LOG IN
@app.post("/user_login/")
async def user_login(user: User):
    # if user_id exists
    d = dict(user)
    user_id = d['user_id']
    user_pw = d['user_pw']
    if connection.db.user_info.count_documents({'user_id': user_id}, limit = 1) != 0:
        # check if password is correct
        if connection.db.user_info.count_documents({'user_id': user_id, 'user_pw': user_pw}, limit = 1) != 0:
            # print("Successfully logged in!")
            # return {"message": user_id + " successfully logged in."}
            # return {"status": "success", "message": user_id + " successfully logged in."}
            bson_data = connection.db.user_info.find_one({'user_id': user_id})
            json_data = dumps(bson_data)
            return {"status": "success", "data": json_data}
        # if password incorrect
        else:
            return {"status": "failed", "message": "Invalid credentials."}
        
    # if user_id does not exist
    else:
        print("Incorrect ID or Password or User doesn't exist. Try again.")
        return {"status": "failed", "message": "user_id does not exist."}



# RAID DETAILS ENTRY
@app.post("/raid_signup/")
async def raid_signup(raid: Raid):
    # convert to a dict
    d = dict(raid)

    # if no errors, can remove these later
    user_id = d['user_id']
    char_name = d['char_name']
    raid_name = d['raid_name']
    guild_or_discord_name = d['guild_or_discord_name']
    # type casting maybe required for next 3
    # start_date_and_time = d['start_date_and_time']
    # or this format
    start_date_and_time = datetime(2020, 5, 16, 20, 30, 0, 0)
    # has to be in seconds
    approx_duration = d['approx_duration']
    # print(f'Type of td: {type(approx_duration)}')
    # print(f'td: {approx_duration}')
    approx_end = start_date_and_time + approx_duration

    # return {"new time": approx_end}

    connection.db.raid_info.insert_one({
        "user_id": user_id, 
        "char_name": char_name, 
        "raid_name": raid_name, 
        "guild_or_discord_name": guild_or_discord_name, 
        "start_date_and_time": start_date_and_time, 
        "approx_duration": str(approx_duration),
        "approx_end": approx_end
        })

    return {"message": "Raid info successfully added."}


# RAID DETAILS FETCH
@app.get("/fetch_raids/{user_id}")
async def fetch_raids(user_id: str):
    pass
    # how to know if the correct user is logged in

    # 2nd argument means which fields to not fetch
    cursor = connection.db.raid_info.find({"user_id": user_id}, {"_id": 0, "user_id": 0})
    list_cur = list(cursor)
    df = pd.DataFrame(list_cur)

    # olny recent dates (from past 7 days to any future date)
    curr_date = datetime.now() - timedelta(days=7)
    # return df
    return df[(df['start_date_and_time'] > curr_date)]



## FUTURE WORK ##
# RAID DOCUMENT/ENTRY DELETE i.e. delete full row/document

# RAID DOCUMENT/ENTRY UPDATE i.e. update/change 1 or more fields in a document/row

# RAID DOCUMENT/ENTRY CLEANUP i.e. remove past records

# USER DOCUMENT/ENTRY DELETE i.e. delete user

# USER DOCUMENT/ENTRY UPDATE i.e. change password


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080, workers=2, reload=True)