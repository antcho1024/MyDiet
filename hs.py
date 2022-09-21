from pymongo import MongoClient
# import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
#
# SECRET_KEY = 'SPARTA'

# client = MongoClient('3.35.136.132', 27017, username="test", password="sparta")
client = MongoClient('mongodb+srv://test:sparta@cluster0.kafwra4.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta_plus_week4


@app.route('/posting_test', methods=['POST'])
def test_post():
    comment_receive = request.form['comment_give']
    image_receive = request.form['image_give']
    category_receive = request.form['category']
    post_id = len(list(db.posts_test.find({},{'_id':False}))) + 1
    doc = {'post_id': post_id, 'cooment' : comment_receive, 'image':image_receive, 'category':category_receive }
    db.posts_test.insert_one(doc)

    # print(comment_receive)
    return jsonify({'result':'success', 'msg': '이 요청은 우크 POST!'})


@app.route('/')
def home():
        return render_template('index.html')
@app.route("/get_posts", methods=['GET'])
def get_posts():
    category_receive = request.args.get('category_give')
    all_posts = list(db.posts_test.find({'category': category_receive}, {'_id': False}))
    return jsonify({'all_posts': all_posts})

@app.route('/update_like', methods=['POST'])
def update_like():
    # token_receive = request.cookies.get('mytoken')
    try:
        # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # user_info = db.users.find_one({"username": payload["id"]})
        post_id_receive = request.form["post_id_give"]
        action_receive = request.form["action_give"]
        doc = {
            "post_id": post_id_receive,
            # "username": user_info["username"],
        }
        if action_receive == "like":
            db.likes.insert_one(doc)
        else:
            db.likes.delete_one(doc)
        count = db.likes.count_documents({"post_id": post_id_receive})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except ():
        return redirect(url_for("home"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

