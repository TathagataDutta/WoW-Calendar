from flask_pymongo import MongoClient
import datetime
import pandas as pd

CON_STR = "mongodb+srv://td:hello123@cluster0.y21dr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# cluster
client = MongoClient(CON_STR)

# database
db = client['wow_calendar']

# users collection
users_colc = db['user_info']

# raid_info colc
raid_info_colc = db['raid_info']


# testing user id and pw insertion if doesn't exist
user_id = "DKR"
user_pw = "123"

# # User Creation
# if users_colc.count_documents({'user_id': user_id}, limit = 1) != 0:
# 	print("User already exists. Try again.")
# else:
# 	users_colc.insert_one({"user_id": user_id, "user_pw": user_pw})


# # User Login
# if users_colc.count_documents({'user_id': user_id}, limit = 1) != 0:
# 	print("Successfully logged in!")
# else:
# 	print("Incorrect ID or Password or User doesn't exist. Try again.")


# Insert Raid Details
# {
#     id: "DKR",
#     toonName: "ac1",
#     raidName: "rd1",
#     guildName: "g1",
#     dt: date
# }
curr_user = user_id
toon_name = "Barrierr"
raid_name = "AQ20"
guild_or_discord_name = "CH"
hour = 20
min = 30
day = 20
month = 5
year = 2021
dt_str = str(year) + "-" + str(month) + "-" + str(day) + "T" + str(hour) + ":" + str(min) + ":00.000Z" 
# dt = datetime.datetime.strptime("2017-10-13T10:53:53.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
# dt = datetime.datetime.utcnow()
dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.000Z")
raid_info_colc.insert_one({"user_id": curr_user, "toon_name": toon_name, "raid_name": raid_name, 
							"guild_or_discord_name": guild_or_discord_name, "dt": dt})


cursor = raid_info_colc.find({"user_id": user_id}, {"_id": 0, "user_id": 0})
# for document in cursor:
# 	print(document)


list_cur = list(cursor)
df = pd.DataFrame(list_cur)

# cursor = raid_info_colc.find({
# 	$and: [
# 		{'user_id': user_id},
# 		{'raid_name': 'BWL'}
# 	]
# })
# for document in cursor:
# 	print(document)


print(df)



client.close()