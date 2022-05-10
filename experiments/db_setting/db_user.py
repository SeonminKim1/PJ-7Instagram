# MONGO DB
from pymongo import MongoClient
db_path = "mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db_port = 27017
client = MongoClient(db_path, db_port)
db = client.luckyseven # DataBase 명

my_collections = db.USER

import hashlib

user_list = [
    {
        'id':"psb6604@gmail.com",
        'pwd': 'psb6604',
        'name': "박재현",
        'nickname':"jhpark",
        'follower':["smkim",'mgkim'],
        'following':['shhwang', 'yhgong'],
        'like':['1'],
        'bookmark':['1'],
        'profile_img': "https://cdn.econovill.com/news/photo/201603/285365_95988_038.png",
    },
    {
        'id':"yubi5050@naver.com",
        'pwd': 'yubi5050',
        'name': "김선민",
        'nickname':"smkim",
        'follower':["jhpark",'mgkim'],
        'following':['shhwang', 'jhpark'],
        'like':[],
        'bookmark':[],
        'profile_img': 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/133.png'
    },
    {
        'id':"hwangshinhye.work@gmail.com",
        'pwd': 'hwangshinhye.work',
        'name': "황신혜",
        'nickname':"shhwang",
        'follower':["jhpark",'mgkim', 'yhgong'],
        'following':['smkim', 'yhgong'],
        'like':['1','2','3'],
        'bookmark':['1','2','3'],
        'profile_img': 'http://img.marieclairekorea.com/2017/01/mck_586f4006b4e9f-375x375.jpg',
    },
    {
        'id':"minki.kim@kakao.com",
        'pwd': 'minki.kim',
        'name': "김민기",
        'nickname':"mgkim",
        'follower':["jhpark", 'shhwang', 'yhgong'],
        'following': ["jhpark", 'shhwang', 'yhgong'],
        'like':['2'],
        'bookmark':['2'],
        'profile_img': "https://i.pinimg.com/736x/8e/5b/a9/8e5ba9d814a3a3eba006a2dccab26c2e--pokemon-mignon-piggy-bank.jpg"
    },
]

for user in user_list:
    user['pwd'] = hashlib.sha256(user['pwd'].encode('utf-8')).hexdigest()

print(user_list)

my_collections.insert(user_list)
print('DB 저장 완료')
# all_value = list(my_collections.find({}))
# same_ages = list(my_collections.find({'age':21}, {'_id':False}))
# my_collections.update_one({'name':'bobby'}, {'$set':{'age':1000}})
# my_collections.delete_one({'name':'bobby'})
