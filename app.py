from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

# MONGO DB
from pymongo import MongoClient
db_path = "mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db_port = 27017
client = MongoClient(db_path, db_port)
db = client.luckyseven # DataBase 명

# Collection
# ex) db.users.insert_one()
# ex) db.feeds.insert_one()

# API
@app.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)