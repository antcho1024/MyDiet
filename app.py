from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from bson.json_util import dumps

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
#
SECRET_KEY = 'SPARTA'

# client = MongoClient('3.35.136.132', 27017, username="test", password="sparta")
client = MongoClient('mongodb+srv://test:sparta@cluster0.kafwra4.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta_plus_week4



@app.route('/posting_test', methods=['POST'])
def test_post():

    comment_receive = request.form['comment_give']
    image_receive = request.form['image_give']
    category_receive = request.form['category']
    username_receive = request.form['username_give']
    date_receive = request.form['date']
    post_id = len(list(db.posts_test.find({},{'_id':False}))) + 1
    doc = {'post_id': post_id, 'cooment' : comment_receive, 'image':image_receive, 'category':category_receive, 'username': username_receive, 'date': date_receive }

    db.posts_test.insert_one(doc)

    # print(comment_receive)
    return jsonify({'result':'success', 'msg': '이 요청은 우크 POST!'})


@app.route('/')
def home():
    # return render_template('index.html')
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        login_status= True
        print(user_info)
        return render_template('index.html', user_info=user_info, login_status=login_status)
    except:
        login_status= False
        return render_template('index.html', user_info=None, login_status=login_status)
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))




@app.route("/get_posts", methods=['GET'])
def get_posts():
    category_receive = request.args.get('category_give')
    posts = list(db.posts_test.find({'category': category_receive}, {'_id': False})) #.sort("date",-1)
    return jsonify({'all_posts': posts})


@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        post_id_receive = request.form["post_id_give"]
        action_receive = request.form["action_give"]
        doc = {
            "post_id": post_id_receive,
            "username": user_info["username"],
        }
        if action_receive == "like":
            db.likes.insert_one(doc)
        else:
            db.likes.delete_one(doc)
        count = db.likes.count_documents({"post_id": post_id_receive})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except ():
        return redirect(url_for("home"))


#############로그인 회원가입#####
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# BBTEST

@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        user_info = db.users.find_one({"username": payload["id"]})
        comment_receive = request.form["comment_give"]
        image = request.images['image_give']
        category_receive = request.form['category_give']
        date_receive = request.form["date_give"]
        extension = image.imagename.split('.')[-1]

        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

        imagename = f'image-{mytime}'

        save_to = f'static/{imagename}.{extension}'
        image.save(save_to)

        print(type(date_receive))
        doc = {
            "username": user_info["username"],
            "profile_name": user_info["profile_name"],
            "profile_pic_real": user_info["profile_pic_real"],
            "comment": comment_receive,
            "category": category_receive,
            "date": date_receive,
            "image": f'{imagename}.{extension}'

        }
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)

        db.posts.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

