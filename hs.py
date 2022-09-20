from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

# client = MongoClient('3.35.136.132', 27017, username="test", password="sparta")
client = MongoClient('mongodb+srv://test:sparta@cluster0.kafwra4.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta_plus_week4

@app.route('/')
def home():
        return render_template('index.html')
@app.route("/main", methods=["GET"])
def movie_get():
    all_movies= list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies':all_movies})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)