from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["DevOps"]
collection = db["flask_tutorial"]

# Route 1: /api : Reads data.json and returns it as JSON
@app.route("/api")
def get_data():
    with open("data.json") as f:
        data = json.load(f)
    return jsonify(data)


# Route 2: /home (Form page) 
@app.route("/")
def home():
    return render_template("index.html")

# Route 3: /submit (Handle form)
@app.route("/submit", methods=["POST"])
def submit():
    form_data = dict(request.form)
    collection.insert_one(form_data)
    form_data['_id'] = str(form_data['_id'])
    
    return 'Data submitted successfully'

if __name__ == "__main__":
    app.run(debug=True)
