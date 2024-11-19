# db.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()
try:
    # Initialize MongoDB client
    client = MongoClient(os.getenv('MONGO_URI'))

    # Access the specified database
    db = client['User']

    # Access a collection
    contacts_collection = db["users"]
    print('connected')
except Exception as e:
    print(e)
