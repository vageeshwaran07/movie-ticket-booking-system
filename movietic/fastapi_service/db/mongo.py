from pymongo import MongoClient, errors
import os
import time


MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")


def get_client(uri, max_retries=5, wait=3):
    for i in range(max_retries):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")  # force connection
            print("✅ Connected to MongoDB")
            return client
        except errors.ServerSelectionTimeoutError as e:
            print(f" MongoDB connection failed ({i+1}/{max_retries}): {e}")
            time.sleep(wait)

    raise Exception("Could not connect to MongoDB after retries")


client = get_client(MONGO_URI)
db = client["movie_booking"]
seats_collection = db["seats"]


def create_ttl_index():
    try:
        seats_collection.create_index(
            "lock_expiry",
            expireAfterSeconds=0
        )
        print(" TTL index ensured on seats.lock_expiry")
    except errors.PyMongoError as e:
        print(f"TTL index creation failed: {e}")
