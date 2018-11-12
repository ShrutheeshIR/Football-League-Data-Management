import pymongo
from predictions import predGoalPlayer
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["footballleague"]
mycol = mydb["userreport"]

# graphJSON=predGoalPlayer.goalplayer()

# mydict = { "username": "user3", "report": graphJSON }

# x = mycol.insert_one(mydict)

myquery = { "username": "user3" }

mydoc = mycol.find(myquery)

for x in mydoc:
  print(x)