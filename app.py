from flask import Flask, render_template, request, jsonify, redirect, url_for
import hashlib
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = '$lucky7'

# DB 연결 코드
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.luckyseven


# 최초 접속 시 연결되는 홈 페이지 지정
@app.route('/')
def home():
    # 현재 컴퓨터에 저장 된 쿠키 중 'mytoken'인 쿠키 가져 와 변수에 저장
    token_receive = request.cookies.get('mytoken')
    try:
        # 암호화되어있는 token의 값을 우리가 사용할 수 있도록 디코딩(암호화 풀기)해줍니다!
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      #   print(payload)
        user_info = list(db.USER.find_one({"id": payload['id']}))
        feed_info = list(db.FEED.find({})) # num, nickname, feed_images, content, like, reply

      #   print(user_info)
        return render_template('/Feed/index.html',
                               feeds=feed_info, users=user_info)
        # 만약 해당 token의 로그인 시간이 만료되었다면, 아래와 같은 코드를 실행합니다.
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:
        # 만약 해당 token이 올바르게 디코딩되지 않는다면, 아래와 같은 코드를 실행합니다.
        return redirect(url_for("login"))

@app.route('/login')
def login():
    return render_template('/login/login.html')


@app.route('/join')
def join():
    return render_template('/login/join.html')


# 회원가입 입력받은 값을 받아 DB에 추가하기
@app.route("/app/join", methods=["POST"])
def api_join():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    nick_receive = request.form['nick_give']
    pwd_receive = request.form['pwd_give']
    # 입력받은 패스워드 값 해싱하여 암호화
    hashed_pw = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'pwd': hashed_pw,
        'name': name_receive,
        'nickname': nick_receive,
        'follower': [],
        'following': [],
        'profile_img': ''
    }
    db.USER.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '회원 가입 완료'})


# ajax에서 비동기식으로 아이디 중복 확인을 위해 따로 함수 정의
@app.route("/app/id_dup", methods=["POST"])
def id_dup():
    id_receive = request.form['id_give']
    id_dup = bool(db.USER.find_one({'id': id_receive}))
    return jsonify({'duplicate': id_dup})


# ajax에서 비동기식으로 닉네임 중복 확인을 위해 따로 함수 정의
@app.route("/app/nick_dup", methods=["POST"])
def nick_dup():
    nick_receive = request.form['nick_give']
    nick_dup = bool(db.USER.find_one({'nickname': nick_receive}))
    return jsonify({'duplicate': nick_dup})


# 로그인 id, pwd 값 받아와서 판별 후 토큰 생성
@app.route("/app/login", methods=["POST"])
def api_login():
    id_receive = request.form['id_give']
    pwd_receive = request.form['pwd_give']
    # 입력받은 패스워드 값 해싱하여 암호화
    hashed_pw = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    # DB에 저장된 값 가져오기
    user = db.USER.find_one({'id': id_receive, 'pwd': hashed_pw})
    print(user)

    if user is not None:
        # JWT(Json Wep Token)생성
        # 토큰을 풀었을 때 얻을 수 있는 id 값과, 유효기간(exp)를 담음
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)
        }
        print(payload)
        # 토큰 생성 payload의 값 인코딩, 암호키 필수 유출금지!, 암호화형태 지정
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print(token)
        return jsonify({'result': 'success', 'token': token, 'msg': '로그인 성공'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
@app.route('/api/valid', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})

    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route('/feed', methods=['POST'])
def Feed():
   feeds = list(db.FEED.find({})) # num, nickname, feed_images, content, like, reply
   users = list(db.USER.find({})) # id, pwd, name, nickname, follower, following, profile_img
   return render_template('Feed/index.html', feeds=feeds, users=users)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)  # 기본포트값 5000으로 설정
