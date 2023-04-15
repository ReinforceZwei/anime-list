import flask
import time
from config import AppConfig
from database import AnimeDatabase
from model import AnimeModel, UserModel

config = AppConfig.load()
db = AnimeDatabase(
    host=config.db_host,
    user=config.db_user,
    password=config.db_password,
    dbname=config.db_name,
    port=config.db_port
)
anime = AnimeModel(db)
user = UserModel(db)

input("Press enter to start testing")

print("Add user (None mean already exist) -", user.add('reinforce', 'password'))
me = user.get_by_name('reinforce')
print("Get user -", me)
print("Verify user password -", user.verify('reinforce', 'password'))

print("Get last modify -", anime.last_modify(me.user_id))
print("Wait 2 seconds")
time.sleep(2)
oshinoko = anime.add(me.user_id, "oshinoko")
print("Add anime -", oshinoko)
print("Get last modify -", anime.last_modify(me.user_id))
print("Wait 2 seconds")
time.sleep(2)
print("Update anime -", anime.update(me.user_id, oshinoko.id, {'comment': 'What a great anime'}))
oshinoko = anime.get(me.user_id, oshinoko.id)
print("Get oshinoko -", oshinoko)
print("Update anime -", anime.update(me.user_id, oshinoko.id, {'downloaded': 1, 'watched': 1}))
oshinoko = anime.get(me.user_id, oshinoko.id)
print("Get oshinoko -", oshinoko)
print("Delete oshinoko -", anime.delete(me.user_id, oshinoko.id))