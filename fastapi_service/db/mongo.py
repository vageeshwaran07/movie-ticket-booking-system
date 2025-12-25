from pymongo import MongoClient, errors
import os
import time

# Use 127.0.0.1 instead of localhost
MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")

# Retry connection until MongoDB is reachable
def get_client(uri, max_retries=5, wait=3):
    for i in range(max_retries):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")  # forces connection
            print("Connected to MongoDB!")
            return client
        except errors.ServerSelectionTimeoutError as e:
            print(f"MongoDB connection failed (attempt {i+1}/{max_retries}): {e}")
            time.sleep(wait)
    raise Exception("Could not connect to MongoDB after multiple attempts.")

client = get_client(MONGO_URI)
db = client["movie_booking"]
seats_collection = db["seats"]

def create_ttl_index():
    try:
        seats_collection.create_index(
            "lock_expiry",
            expireAfterSeconds=0
        )
        print("TTL index created successfully.")
    except errors.PyMongoError as e:
        print(f"Failed to create TTL index: {e}")
