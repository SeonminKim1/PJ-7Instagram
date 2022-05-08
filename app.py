from ast import Not
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
    token_receive = request.cookies.get('mytoken')
    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        user_info = db.USER.find_one({"id": payload['id']})  # id, num, nickname, feed_images, content, like, reply
        feed_info = []
        for follower in user_info['following']:
            feed = list(db.FEED.find({'nickname': follower}))  # num, nickname, feed_images, content, like, reply
            if feed is not None:
                feed_info.extend(feed)
        print(feed_info, len(feed_info))

        # 회원님을 위한 추천 리스트 출력
        all_users_nick_list = []
        # 모든 유저의 닉네임 추출
        all_users = list(db.USER.find({}, {'nickname': True, '_id': False}))
        for all_users_nick in all_users:
            print(all_users_nick['nickname'])
            all_users_nick_list.append(all_users_nick['nickname'])
        print(all_users_nick_list)

        print(user_info['follower'])
        recommend_info = []
        recommend_nick = set(all_users_nick_list) - set(user_info['follower'])
        for recommend in recommend_nick:
            reco = list(db.USER.find({'nickname': recommend}))
            if reco is not None:
                recommend_info.extend(reco)
        print(recommend_info)

        # print(user_info)
        return render_template('/Feed/index.html',
                               feeds=feed_info, users=user_info, recommend=recommend_info)
    except jwt.ExpiredSignatureError:
    # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return render_template('/login/login.html')
    except jwt.exceptions.DecodeError:
        return render_template('/login/login.html')


@app.route('/login')
def login():
    return render_template('/login/login.html')


@app.route('/logout')
def logout():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        return jsonify({'msg': '로그아웃 완료!'})


@app.route('/join')
def join():
    return render_template('/login/join.html')


# 회원가입 입력받은 값을 받아 DB에 추가하기
@app.route("/api/join", methods=["POST"])
def api_join():
    # data = json.loads(request.data) request.data로 get()으로 받아오는 방식으로 사용가능
    # id_receive = data.get('id_give')
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
@app.route("/api/id_dup", methods=["POST"])
def id_dup():
    id_receive = request.form['id_give']
    id_dup = bool(db.USER.find_one({'id': id_receive}))
    return jsonify({'duplicate': id_dup})


# ajax에서 비동기식으로 닉네임 중복 확인을 위해 따로 함수 정의
@app.route("/api/nick_dup", methods=["POST"])
def nick_dup():
    nick_receive = request.form['nick_give']
    nick_dup = bool(db.USER.find_one({'nickname': nick_receive}))
    return jsonify({'duplicate': nick_dup})


# 로그인 id, pwd 값 받아와서 판별 후 토큰 생성
@app.route("/api/login", methods=["POST"])
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)  # 기본포트값 5000으로 설정
