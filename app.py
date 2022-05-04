from flask import Flask, render_template, request, jsonify, redirect
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
    return render_template('login.html')


@app.route('/move_login')
def move_login():
    return render_template('login.html')


@app.route('/move_join')
def move_join():
    return render_template('join.html')


# 회원가입 입력받은 값을 받아 DB에 추가하기
@app.route("/join", methods=["POST"])
def signup():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    nick_receive = request.form['nick_give']
    pwd_receive = request.form['pwd_give']
    # 입력받은 패스워드 값 해싱하여 암호화
    hashed_pw = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    # 아이디 중복 여부 체크
    if bool(db.USER.find_one({'ID': id_receive})):
        return jsonify({'result': 'exist', 'msg': '중복된 아이디 입니다.'})
    else:
        doc = {
            'ID': id_receive,
            'PWD': hashed_pw,
            'NAME': name_receive,
            'NICKNAME': nick_receive,
            'FOLLOWER': '',
            'FOLLOWING': '',
            'FROFILE_IMG': '',
            'MYPAGE_LINK': ''
        }
        db.USER.insert_one(doc)
        return jsonify({'result': 'success', 'msg': '회원 가입 완료'})


# 회원가입 아이디 중복 체크
@app.route('/join_check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 로그인
@app.route("/login", methods=["POST"])
def login():
    id_receive = request.form['id_give']
    pwd_receive = request.form['pwd_give']
    # 입력받은 패스워드 값 해싱하여 암호화
    hashed_pw = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    # DB에 저장된 값 가져오기
    user = db.USER.find_one({'ID': id_receive, 'PWD': hashed_pw})
    print(user)

    if user is not None:
        # JWT(Json Wep Token)생성
        # 토큰을 풀었을 때 얻을 수 있는 id 값과, 유효기간(exp)를 담음
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token, 'msg': '로그인 성공'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)  # 기본포트값 5000으로 설정
