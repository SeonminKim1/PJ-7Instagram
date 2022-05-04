from flask import Flask, render_template, request, jsonify, redirect
import hashlib
app = Flask(__name__)

#DB 연결 코드
from pymongo import MongoClient
client = MongoClient('mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
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

    doc = {
        'ID': id_receive,
        'PWD': hashed_pw,
        'NAME': name_receive,
        'NICKNAME' : nick_receive,
        'FOLLOWER' : '',
        'FOLLOWING' : '',
        'FROFILE_IMG': '',
        'MYPAGE_LINK': ''
    }
    db.USER.insert_one(doc)
    return jsonify({'msg': '회원 가입 완료'})

#로그인
@app.route("/login", methods=["POST"])
def login():
    id_receive = request.form['id_give']
    pwd_receive = request.form['pwd_give']
    # 입력받은 패스워드 값 해싱하여 암호화
    hashed_pw = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    #DB에 저장된 값 가져오기
    user = db.USER.find_one({'ID':id_receive})
    print(user)

    if user is not None:
        print('아이디있음')
        if user['PWD'] == hashed_pw:
            msg = '로그인 성공'
    else:
        msg = '로그인 실패'
    return jsonify({'msg' : msg})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)  # 기본포트값 5000으로 설정
