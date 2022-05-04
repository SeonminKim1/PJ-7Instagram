# MONGO DB
from pymongo import MongoClient
db_path = "mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db_port = 27017
client = MongoClient(db_path, db_port)
db = client.luckyseven # DataBase 명

my_collections = db.FEED
my_collections.insert_many([
    {
        'num':'1',
        'date':'2020.05.01',
        'nickname':'jhpark', 
        'feed_images':["https://images.chosun.com/resizer/XdUHAMF4ZGd_4l8Ze0lyx93Z37Y=/464x0/smart/cloudfront-ap-northeast-1.images.arcpublishing.com/chosun/6UHBHL2DZ7ISPMQ5UO6XAHUYNQ.jpg"],
        'profile_img': "https://cdn.econovill.com/news/photo/201603/285365_95988_038.png",
        'content' : 'CONTENT1',
        'like':[
            {'nickname':'mgkim', 'date':'2020.05.03'},
        ],
        'reply':[
            {'num':1, 'nickname':'mgkim','date':'2021.07.04', 'content':'REPLY111'},
        ]
    },    
    {
        'num':'2',
        'date':'2020.05.03',
        'nickname':'shhwang', 
        'feed_images':["https://mblogthumb-phinf.pstatic.net/20150109_32/dpaaksndpf1_1420737682470GfGRp_JPEG/galaxy_4-wallpaper-1920x1080.jpg?type=w2"],
        'profile_img': 'http://img.marieclairekorea.com/2017/01/mck_586f4006b4e9f-375x375.jpg',
        'content' : 'CONTENT2',
        'like':[
            {'nickname':'jhpark', 'date':'2020.05.05'},
            {'nickname':'mgkim', 'date':'2020.05.06'}
        ],
        'reply':[
            {'num':1, 'nickname':'mgkim','date':'2021.07.14', 'content':'REPLY111reply111'},
            {'num':2, 'nickname':'smkim','date':'2021.07.15', 'content':'REPLY222reply222'},
            {'num':3, 'nickname':'jhpark','date':'2021.07.16', 'content':'REPLY333reply333'}
        ]
    },
    {
        'num':'3',
        'date':'2020.06.01',
        'nickname':'mgkim', 
        'feed_images':["https://png.pngtree.com/background/20210716/original/pngtree-tranquil-universe-background-picture-image_1337175.jpg"],
        'profile_img': "https://i.pinimg.com/736x/8e/5b/a9/8e5ba9d814a3a3eba006a2dccab26c2e--pokemon-mignon-piggy-bank.jpg",
        'content' : 'CONTENT3',
        'like':[
            {'nickname':'jhpark', 'date':'2020.06.13'},
            {'nickname':'shhwang', 'date':'2020.06.14'},
            {'nickname':'smkim', 'date':'2020.06.14'}
        ],
        'reply':[
            {'num':1, 'nickname':'smkim','date':'2021.08.04', 'content':'REPLY111ASD'},
            {'num':2, 'nickname':'shhwang','date':'2021.08.05', 'content':'REPLY222asS'},
        ]
    }
])
print('DB 저장 완료')

# all_value = list(my_collections.find({}))
# same_ages = list(my_collections.find({'age':21}, {'_id':False}))
# my_collections.update_one({'name':'bobby'}, {'$set':{'age':1000}})
# my_collections.delete_one({'name':'bobby'})
