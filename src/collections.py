from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["Rehappy"]

usersCollection = db["users"]
communityCollection = db["community"]