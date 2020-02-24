from flask import Flask, jsonify, request
from flask.json import JSONEncoder

app = Flask(__name__)

app.users = {}
app.id_count = 1
app.tweets = []


@app.route("/sign-up", methods=["POST"])
def sign_up():
    """ 회원 가입
        {
            "email": "sheyon.kang@gmail.com",
            "name": "Seonghyeon Kang",
            "password": "pass1234",
            "profile": "Christian, Data Scientist & Enginner(maybe?)"
        }
    
    Returns:
        json -- 회원 정보
            {
                "email": "sheyon.kang@gmail.com",
                "id": 1
                "name": "Seonghyeon Kang",
                "password": "pass1234",
                "profile": "Christian, Data Scientist & Enginner(maybe?)"
            }
    """
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count + 1

    return jsonify(new_user)


@app.route("/tweet", methods=["POST"])
def tweet():
    """ 트윗 등록
        {
            "id": 1,
            "tweet": "the first tweet"
        }

    Returns:
        string -- tweet contents
    """
    payload = request.json
    user_id = int(payload["id"])
    tweet = payload["tweet"]

    if user_id not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    if len(tweet) > 300:
        return "300자를 초과했습니다.", 400

    app.tweets.append({"user_id": user_id, "tweet": tweet})

    return f"{tweet} is appended", 200


@app.route("/follow", methods=["POST"])
def follow():
    """ 팔로워 등록
        {
            "id": 1,
            "follow": 2
        }

    Returns:
        json -- 팔로워에 추가된 후 사용자 정보
    """
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_follow = int(payload["follow"])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    user = app.users[user_id]
    user.setdefault("follow", set()).add(user_id_to_follow)

    app.users[user_id].update(user)

    return jsonify(app.users[user_id])


@app.route("/unfollow", methods=["POST"])
def unfollow():
    """ 팔로워 해제
        {
            "id": 1,
            "follow": 2
        }

    Returns:
        json -- 팔로워가 해제된 후 사용자 정보
    """
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_unfollow = int(payload["unfollow"])

    if user_id not in app.users or user_id_to_unfollow not in app.users:
        return "사용자가 존재하지 않습니다.", 400
    elif user_id_to_unfollow not in app.users[user_id]["follow"]:
        return "팔로워가 아닙니다.", 400

    user = app.users[user_id]
    user.setdefault("follow", set()).discard(user_id_to_unfollow)  # 키가 없을 땐 무시됨

    app.users[user_id].update(user)

    return jsonify(app.users[user_id])


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


app.json_encoder = CustomJSONEncoder


@app.route("/timeline/<int:user_id>", methods=["GET"])
def timeline(user_id):
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    follow_list = app.users[user_id].get("follow", set())
    follow_list.add(user_id)

    timeline = [
        tweet for tweet in app.tweets if tweet["user_id"] in follow_list
    ]  # 자신과 팔로워 들의 트윗 내용을 출력

    return jsonify({"user_id": user_id, "timeline": timeline})

