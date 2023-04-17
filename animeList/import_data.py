import json
from getpass import getpass
from config import AppConfig
from database import AnimeDatabase
from model import AnimeModel, UserModel
from controller import AnimeController, UserController
from utils import timestamp, days_to_seconds
from log import logger

if __name__ == "__main__":
    config = AppConfig.load()
    db = AnimeDatabase(
        host=config.db_host,
        user=config.db_user,
        password=config.db_password,
        dbname=config.db_name,
        port=config.db_port
    )
    anime_db = AnimeModel(db)
    user_db = UserModel(db)
    anime = AnimeController(anime_db)

    username = input('Import data for:')
    u = user_db.get_by_name(username)
    if u is None:
        print('User does not exist')
        password = getpass('Create new password:')
        u = user_db.add(username, password)
    
    print('Import data for {} (user_id: {})'.format(u.name, u.user_id))
    data_file = input('Path of the .json file:')

    f = open(data_file, 'r', encoding='utf-8')
    json_data = json.loads(f.read())
    f.close()

    # {"animeName":"Kiss×sis 親吻姊姊","animeID":149,"addedTime":1517410740,"downloaded":0,"watched":0,"watchedTime":0,"rating":0,"comment":null,"url":null,"remark":null,"tags":[]}

    for i in json_data:
        new_name_mapping = {
            'animeID': 'id',
            'animeName': 'name',
            'addedTime': 'added_time',
            'watchedTime': 'watched_time',
        }
        for old_name, new_name in new_name_mapping.items():
            if old_name in i:
                i[new_name] = i.pop(old_name)
        if 'tags' in i:
            i['tags'] = json.dumps(i['tags'], ensure_ascii=False)
        i['user_id'] = u.user_id
        sql = "INSERT INTO anime VALUES(%(name)s,%(id)s,%(user_id)s,%(added_time)s,%(watched_time)s,%(downloaded)s,%(watched)s,%(rating)s,%(comment)s,%(url)s,%(remark)s,%(tags)s)"
        result = anime_db._execute(sql, i)
        if result is None:
            print('Error inserting:', i)
    
    print('Import done')