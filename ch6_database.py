from flask import Flask, jsonify
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


def get_user(user_id):
    query = """
        SELECT id, name, email, profile
        FROM users
        WHERE id = :user_id"""

    user = current_app.database.execute(text(query, {"user_id":user_id})).fetchone()
    return {
        'id'    :user['id'],
        'name'  :user['name'],
        'email' :user['email'],
        'profile':user['profile']
    } if user else None


def insert_user(user):
    query = """
        INSERT INTO users (
            name, email, profile, hashed_password
        ) VALUE (
            :name,
            :email,
            :profile,
            :password
        )
    """
    return current_app.database.execute(text(query, user)).lastrowid


def insert_tweet(user_tweet):
    query = """
        INSERT INTO tweets (
            user_id,
            tweet
        ) VALUE (
            :id,
            :tweet
        )
    """
    return current_app.database.execute(text(query, user)).rowcount


def insert_follow(user_follow):
    query = """
        INSERT INTO tweets (
            user_id,
            follow_user_id
        ) VALUE (
            :id,
            :follow
        )
    """
    return current_app.database.execute(text(query, user_follow)).rowcount


def remove_follow(user_unfollow):
    query = """
        DELETE FROM users_follow_list
        WHERE user_id = :id
        AND follow_user_id = :unfollow
    """
    return current_app.database.execute(text(query, user_unfollow)).rowcount


def get_timeline(user_id):
    query = """
        SELECT
            t.user_id,
            t.tweet
        FROM tweets t
        LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
        WHERE t.user_id = :user_id
        OR t.user_id = ufl.follow_user_id
    """
    timeline = current_app.database.execute(text(query, {"user_id":user_id}))

    return [{
        'user_id':tweet['user_id'],
        'tweet':tweet['tweet']
    } for tweet in timeline]
    

def 









def create_app(test_config = None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("dbconfig.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='UTF-8', max_overflow=0)
    app.database = database






    @app.route("/sign-up", methods=['POST'])
    def funcname(self, parameter_list):
        pass
        pass
