from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)

# MONGO DB
from pymongo import MongoClient
db_path = "mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db_port = 27017
client = MongoClient(db_path, db_port)
db = client.luckyseven # DataBase 명

# Collection
# ex) db.USER.insert_one()
# ex) db.FEED.insert_one()

# API
@app.route('/')
def home():
   return render_template('Feed/test.html')

@app.route('/feed', methods=['POST'])
def Feed():
   feeds = list(db.FEED.find({})) # num, nickname, feed_images, content, like, reply
   users = list(db.USER.find({})) # id, pwd, name, nickname, follower, following, profile_img
   return render_template('Feed/index.html', feeds=feeds, users=users)

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)