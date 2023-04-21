import json
import dataclasses
from getpass import getpass
from config import AppConfig
from database import AnimeDatabase
from model import AnimeModel, UserModel, Anime
from controller import AnimeController, UserController
from utils import timestamp, days_to_seconds
from log import logger

class DataImportHelper:
    def __init__(self, db: AnimeModel):
        self._db = db
    
    def import_data(self, user_id: int, data: str) -> list:
        # We trust user exist here
        json_data = {}
        try:
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return ['Cannot decode json data']
        json_data = sorted(json_data, key=lambda d: d['animeID'])
        err_list = []
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
            
            i['user_id'] = user_id
            del i['id']

            # Remove fields that not in Anime class
            fields_name = [x.name for x in dataclasses.fields(Anime)]
            i = {k: v for k, v in i.items() if k in fields_name}

            sql = "INSERT INTO anime(name,user_id,added_time,watched_time,downloaded,watched,rating,comment,url,remark,tags) VALUES(%(name)s,%(user_id)s,%(added_time)s,%(watched_time)s,%(downloaded)s,%(watched)s,%(rating)s,%(comment)s,%(url)s,%(remark)s,%(tags)s)"
            result = self._db._execute(sql, i)
            if result is None:
                err_list.append("Failed to insert: {}".format(i))
        return err_list

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
    data = f.read()
    f.close()

    # {"animeName":"Kiss×sis 親吻姊姊","animeID":149,"addedTime":1517410740,"downloaded":0,"watched":0,"watchedTime":0,"rating":0,"comment":null,"url":null,"remark":null,"tags":[]}

    err_list = DataImportHelper(anime_db).import_data(u.user_id, data)

    if len(err_list):
        for e in err_list:
            print(e)
    
    print('Import done')