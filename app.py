import os
from flask import Flask, jsonify, render_template, redirect, url_for, request, session
import hashlib
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# Tambah parameter serverSelectionTimeoutMS ke URI koneksi
client = MongoClient('mongodb+srv://dandi:hqKMlzFY7QwLhUkS@cluster0.gfzf0gt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&serverSelectionTimeoutMS=30000')
# client = MongoClient('mongodb://localhost:27017/')
db = client.diary

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)
    
    profile = request.files["profile_give"]
    extension = profile.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    profile_filename = f'profile-{mytime}.{extension}'
    save_to = f'static/profile/{profile_filename}'
    profile.save(save_to)

    doc = {
        'title': title_receive,
        'content': content_receive,
        'file': filename,
        'profile': profile_filename,
        'date': today
    }
    db.data.insert_one(doc)

    return jsonify({'msg': 'Upload complete!'})

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.data.find({}, {'_id': False}))
    return jsonify({'articles': articles})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
