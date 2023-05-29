from dataclasses import asdict
from datetime import datetime
from flask import Flask, Response, render_template, redirect, request, url_for, g, make_response
from functools import wraps
import json
from config import AppConfig
from database import AnimeDatabase
from model import AnimeModel, UserModel, UserSetting
from controller import AnimeController, UserController
from utils import timestamp, days_to_seconds
from middleware import PrefixMiddleware
from import_data import DataImportHelper
from log import logger
import logging

config = AppConfig.load()
logger.setLevel(logging.DEBUG if config.debug else logging.INFO)

logger.debug('App launched in debug mode. Please disable debug in production environment!')
logger.debug(config)

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
_user_setting = UserSetting(0, config.app_name, "Watched Animes", "To watch")
user = UserController(user_db, _user_setting, config.secret_key)

app = Flask(__name__)

if config.prefix_path != "":
    app.config['APPLICATION_ROOT'] = config.prefix_path
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=config.prefix_path)

@app.context_processor
def inject_app_info():
    # Make app_name variable available for all templates
    return dict(app_name=config.app_name, allow_register=config.allow_register)

# App routes:
# GET / -> index
# GET /get -> Get all anime. Return json
# GET /get/:id -> Get anime. Return json
# POST /add -> Add anime. Return nothing
#   - animeName
# GET /search[[/:query]?q=] -> Search anime. Return json
# POST /update/:id -> Update anime. Return nothing
# GET /mtime -> Get last modify time. Return int

def require_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        access_token = request.cookies.get('animelist_access_token', '')
        if access_token == "":
            logger.debug('@require_login access token empty')
            return redirect(url_for('logout'))
        
        t_user = user.verify_token(access_token)
        if t_user is None:
            logger.debug('@require_login access token invalid')
            return redirect(url_for('logout'))
        
        g.user_id = t_user.user_id
        g.name = t_user.name
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
        access_token = request.cookies.get('animelist_access_token', '')
        if access_token != '':
            logger.debug('/login check access token %s', access_token)
            if user.verify_token(access_token) is not None:
                logger.debug('/login access token ok')
                return redirect(url_for('index'))
        # Check refresh token
        refresh_token = request.cookies.get('animelist_refresh_token', '')
        if refresh_token != '':
            logger.debug('/login check refresh token %s', refresh_token)
            new_tokens = user.refresh_token(refresh_token)
            if new_tokens is not None:
                # Token valid
                logger.debug('/login refresh token valid')
                access, refresh = new_tokens
                response = make_response(redirect(url_for('index')))
                response.set_cookie(
                    'animelist_access_token',
                    access,
                    expires=timestamp()+days_to_seconds(14),
                    httponly=True,
                    samesite='strict')
                response.set_cookie(
                    'animelist_refresh_token',
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
        remember_me = request.form.get('remember_me', False)
        new_tokens = user.authenticate(name, password)
        if new_tokens is not None:
            # Token valid
            access, refresh = new_tokens
            response = make_response(redirect(url_for('index')))
            if remember_me:
                # Keep login
                response.set_cookie(
                    'animelist_access_token',
                    access,
                    expires=timestamp()+days_to_seconds(14),
                    httponly=True,
                    samesite='strict')
                response.set_cookie(
                    'animelist_refresh_token',
                    refresh,
                    expires=timestamp()+days_to_seconds(30),
                    httponly=True,
                    samesite='strict')
            else:
                # Session cookie
                response.set_cookie(
                    'animelist_access_token',
                    access,
                    httponly=True,
                    samesite='strict')
            # Redirect to index
            return response
        else:
            # Auth failed
            return render_template('login.html', hint='Invalid username or password')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Doesn't require valid login. We always delete user cookies
    response = make_response(redirect(url_for('login')))
    response.set_cookie('animelist_access_token', '', expires=0)
    response.set_cookie('animelist_refresh_token', '', expires=0)
    return response

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if user._user.app_user_count() > 0 and not config.allow_register:
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
    setting = user.get_setting(g.user_id)
    for i in watched:
        css_class = []
        if i.downloaded:
            css_class.append('downloaded')
        if i.rating < 0:
            css_class.append('deleteLine')
        if i.remark:
            i.remark = '（{}）'.format(i.remark)
        i._css_class = ', '.join(css_class)
    for i in unwatched:
        css_class = []
        if i.downloaded:
            css_class.append('downloaded')
        if i.rating < 0:
            css_class.append('deleteLine')
        if i.remark:
            i.remark = '（{}）'.format(i.remark)
        i._css_class = ', '.join(css_class)
    return render_template('index.html', watched=watched, unwatched=unwatched, **asdict(setting))

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

@app.route('/import', methods=['GET', 'POST'])
@require_login
def import_data():
    if request.method == 'GET':
        return render_template('import_data.html')
    elif request.method == 'POST':
        data_file = request.files.get('data')
        print(request.files)
        if not data_file:
            return 'No file uploaded', 400
        data = data_file.stream.read()
        import_helper = DataImportHelper(anime_db)
        err = import_helper.import_data(g.user_id, data)
        title = 'Import done'
        content = ''
        if len(err):
            title = 'Import done with errors'
            content = '<br>'.join(err)
        return render_template('result.html', title=title, content=content)
    else:
        # Never reach
        return redirect(url_for('login'))

@app.get('/export_data')
@require_login
def export_data():
    result = anime.get_all(g.user_id)
    result = [x.to_client_dict() for x in result]
    json_str = json.dumps(result, ensure_ascii=False)
    file_name = 'animelist-export-{}'.format(datetime.now().strftime("%Y%m%d-%H%M"))
    return Response(
        json_str,
        mimetype='application/json',
        headers={
            'Content-Disposition':'attachment;filename={}.json'.format(file_name)
        })

@app.post('/delete/<int:id>')
@require_login
def delete(id: int):
    anime.delete(g.user_id, id)
    return '', 200

@app.post('/delete_account')
@require_login
def delete_account():
    password = request.form.get('password', '')
    if user.authenticate(g.name, password) is not None:
        user.delete(g.user_id)
        return redirect(url_for('logout'))
    else:
        return '', 400

@app.post('/change_password')
@require_login
def change_password():
    old_password = request.form.get('password_old')
    new_password = request.form.get('password_new')
    if user.change_password(g.user_id, old_password, new_password):
        return '', 200
    else:
        return '', 400

@app.route('/setting', methods=['GET', 'POST'])
@require_login
def setting():
    if request.method == 'GET':
        setting = user.get_setting(g.user_id)
        if setting is not None:
            return asdict(setting)
        else:
            return '', 404
    elif request.method == 'POST':
        if user.update_setting(g.user_id, request.form.to_dict()):
            return '', 200
        else:
            return '', 500


if __name__ == "__main__":
    if config.debug:
        app.debug = True
    app.run(port = config.port, host='0.0.0.0')