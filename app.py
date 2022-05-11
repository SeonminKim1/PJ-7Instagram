from flask import Flask, render_template, request, jsonify, redirect, url_for
import hashlib
import jwt
import datetime
import random
import certifi

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

SECRET_KEY = '$lucky7'

# DB 연결 코드
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.luckyseven


### ================ Login / Logout Page ================
@app.route('/login')
def login():
    return render_template('/login/login.html')


@app.route('/logout')
def logout():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        return jsonify({'msg': '로그아웃 완료!'})


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
        # 토큰 생성 payload의 값 인코딩, 암호키 필수 유출금지!, 암호화형태 지정
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token, 'msg': '로그인 성공'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저(유효한 Token)만 접근 할 수 있는 API
@app.route('/api/valid', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        # 웹 접속자가 가지고 있는 token을 시크릿키로 디코딩
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # payload 안에 id가 들어있습니다. 이 id로 유저정보 조회
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})

    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


### ================ Join Page ================
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
        'like': [],
        'bookmark': [],
        'profile_img': 'profile_default.png'
    }
    db.USER.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '회원 가입 완료'})


### ================ Feed Main Page ================
@app.route('/')
def home():
    # 현재 컴퓨터에 저장 된 'mytoken'인 쿠키 확인
    token_receive = request.cookies.get('mytoken')
    try:
        # 암호화되어있는 token의 값 디코딩(암호화 풀기)
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # USER의 Following 들의 nickname 필드로 Feed들 조회
        user_info = db.USER.find_one({"id": payload['id']})  # id, num, nickname, feed_images, content, like, reply
        feed_info = []
        if user_info is not None:  # Following이 한명이라도 있을 떄
            for follower in user_info['following']:
                feed = list(db.FEED.find({'nickname': follower}))  # num, nickname, feed_images, content, like, reply
                if feed is not None:
                    feed_info.extend(feed)
            # Feed 시간 순으로 Sorting
            feed_info = sorted(feed_info, key=lambda x: x['date'], reverse=True) # 최신 글 순서로 Sorting

        # 회원님을 위한 추천 리스트 출력
        all_users_nick_list = []
        # 모든 유저의 닉네임 추출
        all_users = list(db.USER.find({}, {'nickname': True, '_id': False}))
        if len(all_users) != 0:
            for all_users_nick in all_users:
                all_users_nick_list.append(all_users_nick['nickname'])
            # print(all_users_nick_list)  # 모든 유저의 닉 리스트
            # print(user_info['following'])  # 내가 팔로우한 유저의 닉 리스트

            # 모든 유저 닉 - 내가 팔로잉중인 유저 닉 - 나의 닉네임 = 추천 친구 리스트
            recommend_info = []
            recommend_nick = list(set(all_users_nick_list) - set(user_info['following']))  # 내 팔로잉 유저들 제외
            recommend_nick.remove(user_info['nickname'])  # 나 제외
            for recommend in recommend_nick:
                reco = list(db.USER.find({'nickname': recommend}))
                if reco is not None:
                    recommend_info.extend(reco)

            # print(recommend_info)
            # 추천 친구 리스트 중 랜덤으로 중복 허용하지 않으면서 3개만 뽑아서 출력
            if len(recommend_info) >= 3:
                recommend_3 = random.sample(recommend_info, 3)
                return render_template('/Feed/index.html',
                                feeds=feed_info, users=user_info, recommend=recommend_3)
            else:
                recommend_3 = '추천 할 회원이 없습니다.'
                return render_template('/Feed/index.html',
                                    feeds=feed_info, users=user_info, recommend=recommend_3)
        return render_template('/Feed/index.html',feeds=feed_info, users=user_info)

    except jwt.ExpiredSignatureError: # 해당 token의 로그인 시간이 만료시 login 페이지로 redirect
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:  # 해당 token이 다르다면 login 페이지로 redirect
        return redirect(url_for("login"))


# 댓글 작성
@app.route('/api/reply/writing', methods=['POST'])
def write_reply():
    # 1) Request 에서 넘겨받은 값
    nickname = request.form['nickname']
    reply_content = request.form['reply_content']
    feed_num = request.form['feed_num']

    # 2) Feed Number로 Feed 조회
    feed = db.FEED.find_one({'num': feed_num})
    feed_reply = feed['reply']  # list[dict, dict]

    # 3) DB Update 할 Reply Dictionary 만들기
    num = int(feed['reply'][-1]['num']) + 1  # 맨 마지막 num의 +1
    date = datetime.datetime.today().strftime("%Y.%m.%d.%H.%M.%S")
    feed_reply.append({'num': num, 'nickname': nickname, 'date': date, 'content': reply_content})

    # 4) Feed DB reply Update
    db.FEED.update_one({'num': feed_num}, {'$set': {'reply': feed_reply}})
    return jsonify({'msg': '댓글 작성 완료'})


# 좋아요 - USER DB, FEED DB Update
# 좋아요 누름 - USER DB의 like에 Feed Number ID 추가 / Feed DB의 like에 {nickname, date } 추가
# 좋아요 취소 - USER DB의 like에 Feed Number ID 제거 / Feed DB의 like에 해당 {nickname, date } 제거
@app.route('/api/like', methods=['POST'])
def is_like():
    # 1) Request 에서 넘겨받은 값
    is_like = request.form['is_like']
    nickname = request.form['nickname']  # 현재 계정 nickname
    feed_num = request.form['feed_num']  # 현재 Feed Num
    # print('==', is_like, nickname, feed_num)

    # 2) Feed Number로 Feed 조회
    feed = db.FEED.find_one({'num': feed_num})  # 해당 Feed Info
    user = db.USER.find_one({'nickname': nickname})  # 해당 User Info
    feed_like, user_like = feed['like'], user['like']

    # 3) DB Update 할 List 만들기
    if is_like == '1':  # 제거
        user_like.remove(feed_num)  # USER DB의 like에서 Feed Number 제거
        # Feed DB의 like에서 해당 Nickname 제거
        for like_dict in feed_like:
            if like_dict['nickname'] == nickname:
                feed_like.remove(like_dict)
                break

    else:  # is_like == '0' # 추가
        x_cond = (feed_num not in user_like)
        y_cond = (nickname not in [x['nickname'] for x in feed_like])
        if x_cond and y_cond:
            user_like.append(feed_num)  # USER DB의 like에 Feed Number ID 추가
            # Feed DB의 like에 {nickname, date } 추가
            date = datetime.datetime.today().strftime("%Y.%m.%d.%H.%M.%S")
            feed_like.append({'nickname': nickname, 'date': date})

    # 4) Feed DB like 필드 Update
    db.FEED.update_one({'num': feed_num}, {'$set': {'like': feed_like}})
    db.USER.update_one({'nickname': nickname}, {'$set': {'like': user_like}})

    if is_like =='1':
        return jsonify({'msg': '좋아요 제거 Update 완료', 'is_like':0})
    else:
        return jsonify({'msg': '좋아요 Update 완료', 'is_like':1})


# 북마크 - USER DB, FEED DB Update
# 북마크 누름 - USER DB의 bookmark에 Feed Number ID 추가 / Feed DB의 bookmark에 {nickname, date } 추가
# 북마크 취소 - USER DB의 bookmark에 Feed Number ID 제거 / Feed DB의 bookmark에 해당 {nickname, date } 제거
@app.route('/api/bookmark', methods=['POST'])
def is_bookmark():
    # 1) Request 에서 넘겨받은 값
    is_bookmark = request.form['is_bookmark']
    nickname = request.form['nickname']  # 현재 계정 nickname
    feed_num = request.form['feed_num']  # 현재 Feed Num

    # 2) Feed Number로 Feed 조회
    feed = db.FEED.find_one({'num': feed_num})  # 해당 Feed Info
    user = db.USER.find_one({'nickname': nickname})  # 해당 User Info
    feed_bookmark, user_bookmark = feed['bookmark'], user['bookmark']

    # 3) DB Update 할 List 만들기
    if is_bookmark == '1':  # 제거
        user_bookmark.remove(feed_num)  # USER DB의 bookmark에서 Feed Number 제거
        # Feed DB의 bookmark에서 해당 Nickname 제거
        for bookmark_dict in feed_bookmark:
            if bookmark_dict['nickname'] == nickname:
                feed_bookmark.remove(bookmark_dict)
                break

    else:  # is_bookmark == '0' # 추가
        x_cond = (feed_num not in user_bookmark)
        y_cond = (nickname not in [x['nickname'] for x in feed_bookmark])
        if x_cond and y_cond:
            user_bookmark.append(feed_num)  # USER DB의 bookmark에 Feed Number ID 추가
            # Feed DB의 bookmark에 {nickname, date } 추가
            date = datetime.datetime.today().strftime("%Y.%m.%d.%H.%M.%S")
            feed_bookmark.append({'nickname': nickname, 'date': date})

    # 4) Feed DB bookmark 필드 Update
    db.FEED.update_one({'num': feed_num}, {'$set': {'bookmark': feed_bookmark}})
    db.USER.update_one({'nickname': nickname}, {'$set': {'bookmark': user_bookmark}})

    if is_bookmark == '1':
        return jsonify({'msg': '북마크 취소 Update 완료'})
    else:
        return jsonify({'msg': '북마크 등록 Update 완료'})

### nickname을 받아와서 내 계정에 팔로우 되어있는지 확인
### 팔로우 - nickname 을 받아와서 DB에 저장
### 언팔로우 - nickname 을 받아와서 DB에서 제거
@app.route('/api/follow', methods=['POST'])
def is_following():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    print(payload['id'])
    follow_nick = request.form['nick_give']
    print(follow_nick)

    my_follow = db.USER.find_one({'id':payload['id']})
    print(my_follow['following'])

    if follow_nick in my_follow['following']:
        db.USER.update_one({'id': payload['id']}, {'$pull': {'following': follow_nick}})
        db.USER.update_one({'id': follow_nick}, {'$pull': {'follower': payload['id']}})
        print('DB 에 팔로우 제거 완료!')
        return jsonify(({'result': 'success', 'is_following': 0}))

    else:
        db.USER.update_one({'id': payload['id']}, {'$push': {'following': follow_nick}})
        db.USER.update_one({'id': follow_nick}, {'$push': {'follower': payload['id']}})
        print('DB 에 팔로우 추가 완료!')
        return jsonify({'result': 'success', 'is_following': 1})

### ================ Profile Page (Mypage) ================
@app.route('/api/profile')
def profile():
    # 현재 컴퓨터에 저장 된 'mytoken'인 쿠키 확인
    token_receive = request.cookies.get('mytoken')
    try:
        # 암호화되어있는 token의 값 디코딩(암호화 풀기)
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        feed_nickname = request.args.get('feed_nickname')

        user_info = db.USER.find_one({"nickname": feed_nickname})  # id, num, nickname, feed_images, content, like, reply
        my_feed_list = list(db.FEED.find({"nickname": feed_nickname}))
        # print(my_feed_list)

        post_count = len(my_feed_list)
        follower_count = len(user_info['follower'])
        following_count = len(user_info['following'])

        my_follower_list = []
        for my_followers in user_info['follower']:
            my_follower = db.USER.find_one({'nickname': my_followers})
            my_follower_list.append(my_follower)


        my_following_list = []
        for my_followings in user_info['following']:
            my_following = db.USER.find_one({'nickname': my_followings})
            my_following_list.append(my_following)

        return render_template('/profile/profile.html', post_count=post_count, users=user_info, follower_count=follower_count,
                               following_count=following_count, my_feed_list=my_feed_list, my_follower_list=my_follower_list, my_following_list=my_following_list)

    except jwt.ExpiredSignatureError:  # 해당 token의 로그인 시간이 만료시 login 페이지로 redirect
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:  # 해당 token이 다르다면 login 페이지로 redirect
        return redirect(url_for("login"))


@app.route('/api/feed/upload', methods=['POST'])
def feed_upload():
    file = request.files['file']
    image = request.form['image']
    content = request.form['content']
    profile_image = request.form['profile_image']
    user_nick = request.form['user_nick']

    # 해당 파일에서 확장자명만 추출
    extension = file.filename.split('.')[-1]
    # 파일 이름이 중복되면 안되므로, 지금 시간을 해당 파일 이름으로 만들어서 중복이 되지 않게 함!
    today = datetime.datetime.utcnow()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{user_nick}-{mytime}'
    # 파일 저장 경로 설정 (파일은 db가 아니라, 서버 컴퓨터 자체에 저장됨)
    save_to = f'static/upload/{filename}.{extension}'
    # 파일 저장!
    file.save(save_to)

    count_list = [0]
    feed_list = list(db.FEED.find({}, {'num': True, '_id': False}))
    for number in feed_list:
        print(number['num'])
        count_list.append(int(number['num']))

    count = max(count_list) + 1

    print(count)
    print(file)
    print(image)
    print(content)
    print(profile_image)
    print(user_nick)

    # 아래와 같이 입력하면 db에 추가 가능!
    doc = {
        'num': str(count),
        'date': mytime,
        'nickname': user_nick,
        'feed_images': [f'{filename}.{extension}'],
        'profile_img': profile_image,
        'content': content,
        'like': [],
        'bookmark': [],
        'reply': []
    }
    db.FEED.insert_one(doc)

    return jsonify({'result': 'success'})

@app.route('/change_profile')
def change_profile():
    # 현재 컴퓨터에 저장 된 'mytoken'인 쿠키 확인
    token_receive = request.cookies.get('mytoken')
    # 암호화되어있는 token의 값 디코딩(암호화 풀기)
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    my_info = db.USER.find_one({'id':payload['id']})

    return render_template('/profile/change_profile.html', my_info=my_info)


# 방식1 : DB에는 파일 이름만 넣어놓고, 이미지 자체는 서버 컴퓨터에 저장하는 방식
@app.route('/fileupload', methods=['POST'])
def file_upload():
    print('file_upload() 도착')
    nick_receive = request.form['nick_give']
    file = request.files['file_give']
    # 해당 파일에서 확장자명만 추출
    extension = file.filename.split('.')[-1]
    # 파일 이름이 중복되면 안되므로, 지금 시간을 해당 파일 이름으로 만들어서 중복이 되지 않게 함!
    today = datetime.datetime.utcnow()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{nick_receive}-{mytime}'
    # 파일 저장 경로 설정 (파일은 db가 아니라, 서버 컴퓨터 자체에 저장됨)
    save_to = f'static/profile_images/{filename}.{extension}'
    # 파일 저장!
    file.save(save_to)

    db.USER.update_one({'nickname': nick_receive}, {'$set': {'profile_img': f'{filename}.{extension}'}})
    feed = list(db.FEED.find({'nickname': nick_receive}))  # num, nickname, feed_images, content, like, reply

    db.FEED.update({'nickname': nick_receive}, {'$set': {'profile_img': f'{filename}.{extension}'}})
    for nick in feed:
        print(nick)
    return jsonify({'result': 'success'})


### ================ Main ================
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)  # 기본포트값 5000으로 설정

