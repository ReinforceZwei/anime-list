from flask import Flask, render_template, redirect, request, url_for, g, make_response
from functools import wraps
import json
from config import AppConfig
from database import AnimeDatabase
from model import AnimeModel, UserModel
from controller import AnimeController, UserController
from utils import timestamp, days_to_seconds
from log import logger

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
user = UserController(user_db, config.secret_key)

# App routes:
# GET / -> index
# GET /get -> Get all anime. Return json
# GET /get/:id -> Get anime. Return json
# POST /add -> Add anime. Return nothing
#   - animeName
# GET /search[[/:query]?q=] -> Search anime. Return json
# POST /update/:id -> Update anime. Return nothing
# GET /mtime -> Get last modify time. Return int

app = Flask(__name__)

def require_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        access_token = request.cookies.get('__access_token', '')
        if access_token == "":
            logger.debug('@require_login access token empty')
            return redirect(url_for('login'))
        
        user_id = user.verify_token(access_token)
        if user_id is None:
            logger.debug('@require_login access token invalid')
            return redirect(url_for('login'))
        g.user_id = user_id
        logger.debug('@require_login user ok')
        return func(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Redirect to create user if no users
        if user._user.app_user_count() == 0:
            return redirect(url_for('new_user'))
        # Check access token
        access_token = request.cookies.get('__access_token', '')
        if access_token != '':
            logger.debug('/login check access token %s', access_token)
            if user.verify_token(access_token) is not None:
                logger.debug('/login access token ok')
                return redirect(url_for('index'))
        # Check refresh token
        refresh_token = request.cookies.get('__refresh_token', '')
        if refresh_token != '':
            logger.debug('/login check refresh token %s', refresh_token)
            new_tokens = user.refresh_token(refresh_token)
            if new_tokens is not None:
                # Token valid
                logger.debug('/login refresh token valid')
                access, refresh = new_tokens
                response = make_response(redirect(url_for('index')))
                response.set_cookie(
                    '__access_token',
                    access,
                    expires=timestamp()+days_to_seconds(14),
                    httponly=True,
                    samesite='strict')
                response.set_cookie(
                    '__refresh_token',
                    refresh,
                    expires=timestamp()+days_to_seconds(30),
                    httponly=True,
                    samesite='strict')
                # Redirect to index
                return response
        # Else show login page
        logger.debug('/login show page')
        return render_template('login.html')
    elif request.method == 'POST':
        name = request.form.get('name', '')
        password = request.form.get('password', '')
        new_tokens = user.authenticate(name, password)
        if new_tokens is not None:
            # Token valid
            access, refresh = new_tokens
            response = make_response(redirect(url_for('index')))
            response.set_cookie(
                '__access_token',
                access,
                expires=timestamp()+days_to_seconds(14),
                httponly=True,
                samesite='strict')
            response.set_cookie(
                '__refresh_token',
                refresh,
                expires=timestamp()+days_to_seconds(30),
                httponly=True,
                samesite='strict')
            # Redirect to index
            return response
        else:
            # Auth failed
            return render_template('login.html', hint='Invalid username or password')

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if user._user.app_user_count() > 0:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('new_user.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        if user.new_user(name, password):
            return redirect(url_for('login'))
        else:
            return 'Cannot create new user', 400
    else:
        # Never reach
        return redirect(url_for('login'))

@app.get('/')
@require_login
def index():
    watched = anime._anime.get_watched_sorted(g.user_id)
    unwatched = anime._anime.get_unwatched_sorted(g.user_id)
    for i in watched:
        css_class = []
        if i.downloaded:
            css_class.append('downloaded')
        if i.rating < 0:
            css_class.append('deleteLine')
        if i.remark:
            i.remark = '（%s）'.format(i.remark)
        i._css_class = ', '.join(css_class)
    for i in unwatched:
        css_class = []
        if i.downloaded:
            css_class.append('downloaded')
        if i.rating < 0:
            css_class.append('deleteLine')
        if i.remark:
            i.remark = '（%s）'.format(i.remark)
        i._css_class = ', '.join(css_class)
    return render_template('index.html', watched=watched, unwatched=unwatched)

@app.get('/get')
@require_login
def get():
    result = anime.get_all(g.user_id)
    result = [x.to_client_dict() for x in result]
    return result

@app.get('/get/<int:id>')
@require_login
def get_id(id: int):
    result = anime.get(g.user_id, id)
    if result is None:
        return '', 404
    else:
        return result.to_client_dict()

@app.post('/add')
@require_login
def add():
    name = request.form.get('animeName', '')
    if name != '':
        result = anime.add(g.user_id, name)
        if result is not None:
            return result.to_client_dict()
    return '', 400

@app.post('/update/<int:id>')
@require_login
def update(id: int):
    values = request.form.to_dict()
    logger.debug('Value from update: %s', request.form)
    new_name_mapping = {
        'animeID': 'id',
        'animeName': 'name',
        'addedTime': 'added_time',
        'watchedTime': 'watched_time',
    }
    for old_name, new_name in new_name_mapping.items():
        if old_name in values:
            values[new_name] = values.pop(old_name)
    if 'tags[]' in values:
        values['tags'] = json.dumps(request.form.getlist('tags[]'), ensure_ascii=False)
    logger.debug('Processed values: %s', values)
    anime.update(g.user_id, id, values)
    return '', 200

@app.get('/mtime')
@require_login
def mtime():
    return str(anime.last_modify(g.user_id))

if __name__ == "__main__":
    app.run(port = config.port)