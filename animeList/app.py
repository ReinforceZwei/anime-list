import flask
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

# App routes:
# GET / -> index
# GET /get -> Get all anime. Return json
# GET /get/:id -> Get anime. Return json
# POST /add -> Add anime. Return nothing
#   - animeName
# GET /search[[/:query]?q=] -> Search anime. Return json
# POST /update/:id -> Update anime. Return nothing
# GET /mtime -> Get last modify time. Return int

app = flask.Flask(__name__)

@app.get('/')
def index():
    return flask.render_template('index.html')

@app.get('/get')
def get():
    return '?'

if __name__ == "__main__":
    app.run(port = config.port)