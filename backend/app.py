from flask import Flask, request
from dotenv import load_dotenv
import os
import pymongo

# Load environment variables from .env file.

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
# Create or get the database
db = client.test

collection = db["flask_collection"]

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_example():
    name = request.form.get('name')
    email = request.form.get('email')
    form_data = dict(request.form)
    # Save form data to MongoDB
    collection.insert_one(form_data)
    # Process form data
    if name and email:
        return f"Form submitted successfully! Name: {name}, Email: {email}."
    else:
        return "Please fill out both fields."

@app.route('/api')
def get_data():
    # Retrieve all documents from the collection
    data = list(collection.find())
    # Convert ObjectId to string for JSON
    for item in data:
        item['_id'] = str(item['_id'])
    return {"data": data}

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_desc = request.form.get("itemDescription")
    if item_name and item_desc:
        collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_desc
        })
        return "To-Do item submitted successfully."
    else:
        return "Missing item name or description.", 400


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8000", debug=True)