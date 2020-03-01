from flask import Flask, jsonify, request
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


def get_user(user_id):
    query = """
        SELECT id, name, email, profile FROM users WHERE id = :user_id
    """

    user = current_app.database.execute(text(query), {"user_id": user_id}).fetchone()
    return (
        {"id": user["id"], "name": user["name"], "email": user["email"], "profile": user["profile"]}
        if user
        else None
    )


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
    return current_app.database.execute(text(query), user).lastrowid


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
    return current_app.database.execute(text(query), user_tweet).rowcount


def insert_follow(user_follow):
    query = """
        INSERT INTO users_follow_list (
            user_id,
            follow_user_id
        ) VALUE (
            :id,
            :follow
        )
    """
    return current_app.database.execute(text(query), user_follow).rowcount


def remove_follow(user_unfollow):
    query = """
        DELETE FROM users_follow_list
        WHERE user_id = :id
        AND follow_user_id = :unfollow
    """
    return current_app.database.execute(text(query), user_unfollow).rowcount


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
    timeline = current_app.database.execute(text(query), {"user_id": user_id}).fetchall()

    return [{"user_id": tweet["user_id"], "tweet": tweet["tweet"]} for tweet in timeline]


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("dbconfig.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config["DB_URL"], encoding="UTF-8", max_overflow=0)
    app.database = database

    @app.route("/sign-up", methods=["POST"])
    def sign_up():
        print(request.json)
        new_user = request.json
        new_user_id = insert_user(new_user)
        new_user = get_user(new_user_id)

        return jsonify(new_user)

    @app.route("/tweet", methods=["POST"])
    def tweet():
        user_tweet = request.json
        tweet = user_tweet["tweet"]

        if len(tweet) > 300:
            return "300자를 초과하였습니다.", 400

        insert_tweet(user_tweet)

        return "트윗이 등록되었습니다.", 200

    @app.route("/follow", methods=["POST"])
    def follow():
        payload = request.json
        insert_follow(payload)

        return "팔로워가 등록되었습니다.", 200

    @app.route("/unfollow", methods=["POST"])
    def unfollow():
        payload = request.json
        remove_follow(payload)

        return "팔로워가 삭제되었습니다.", 200

    @app.route("/timeline/<int:user_id>", methods=["GET"])
    def timeline(user_id):
        return jsonify({"user_id": user_id, "timeline": get_timeline(user_id)})

    return app


current_app = create_app()


if __name__ == "__main__":
    current_app.run(debug=True, host="0.0.0.0")
