import pymongo


def display_db():
    for i in cursor.find():
        print(i['password'])


client = pymongo.MongoClient(
    "mongodb+srv://user:yigitinsifresi@project.mlvsxim.mongodb.net/test")
cursor = client["kriptoloji"].project

display_db()

client.close()
