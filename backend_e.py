from flask import Flask, jsonify, request
import datetime
import jwt
import backend_a as aadeesh

PRIVATE_KEY = "esharkyisthecoolestherointhiswholeworld"

def validate_token(token):
    try:
        return jwt.decode(token, PRIVATE_KEY,verify=True, algorithms=["HS256"])['username']
    except Exception as e:
        return None

app = Flask("coco")

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/add", methods=["POST"])
def add_question():
    data = request.get_json()
    # Handle Authentication and get User
    token = data.get("token")
    user = validate_token(token)
    if user is None:
        return jsonify({"status": "error", "message": "invalid token"})

    question = data.get("question")
    # Add Question to Database
    aadeesh.addQuestion(question)
    if question is None:
        return jsonify({"status": "error", "message": "no question"})
    return jsonify({"status": "success"})

@app.route("/list", methods=["GET"])
def list_questions():
    data = request.get_json()
    # Handle Authentication and get User
    token = data.get("token")
    user = validate_token(token)
    if user is None:
        return jsonify({"status": "error", "message": "invalid token"})

    # Get Questions from Database
    questions = aadeesh.listAllQuestions()
    return jsonify({"status": "success", "questions": questions})

@app.route("/mark", methods=["POST"])
def mark_question():
    data = request.get_json()
    # Handle Authentication and get User
    token = data.get("token")
    user = validate_token(token)
    if user is None:
        return jsonify({"status": "error", "message": "invalid token"})
    data = request.get_json()
    question = data.get("question")
    if question is None:
        return jsonify({"status": "error", "message": "no question_id"})
    # Mark Question in Database
    # aadeesh.addQuestion(question)
    aadeesh.markQuestionAsSolved(user,question)
    return jsonify({"status": "success"})

@app.route("/unmark", methods=["POST"])
def unmark_question():
    data = request.get_json()
    # Handle Authentication and get User
    token = data.get("token")
    user = validate_token(token)
    if user is None:
        return jsonify({"status": "error", "message": "invalid token"})
    data = request.get_json()
    question = data.get("question")
    if question is None:
        return jsonify({"status": "error", "message": "no question_id"})
    # UnMark Question in Database
    #
    return jsonify({"status": "success"})

@app.route("/leaderboard")
def leaderboard():
    data = request.get_json()
    # Handle Authentication and get User
    token = data.get("token")
    user = validate_token(token)
    if user is None:
        return jsonify({"status": "error", "message": "invalid token"})

    # Get Leaderboard from Database
    leaderboard = aadeesh.listAllUsers(sort=True)
    return jsonify({"status": "success", "leaderboard": leaderboard})

@app.route("/stats/user",methods=["GET"])
def user_stats():
    data = request.get_json()
    # Handle Authentication and Get User
    token = data.get("token")
    user_token = validate_token("token")
    if user_token is None:
        return jsonify({"status":"error","message":"invalid token"})
    # Get User Stats
    user = data.get("username")
    user_stat = aadeesh.listUserStats(user)
    return jsonify({"status":"success","user":user_stat})

@app.route("/stats/question",methods=["GET"])
def question_stats():
    data = request.get_json()
    # Handle Authentication and Get User
    token = data.get("token")
    user = validate_token("token")
    if user is None:
        return jsonify({"status":"error","message":"invalid token"})
    # Get Question Stats
    question = data.get("question")
    if question is None:
        return jsonify({"status":"error", "message":"no question provided"})
    question_stat = aadeesh.listQuestionStats(question)
    return jsonify({"status":"success",})

@app.route("/top/solved",methods=["GET"])
def top_solved():
    data = request.get_json()
    # Handle Authentication and Get User
    token = data.get("token")
    user = validate_token("token")
    if user is None:
        return jsonify({"status":"error","message":"invalid token"})
    # Get Top Solved Question
    #
    return jsonify({"status":"success",})

@app.route("/top/unsolved",methods=["GET"])
def top_unsolved():
    data = request.get_json()
    # Handle Authentication and Get User
    token = data.get("token")
    user = validate_token("token")
    if user is None:
        return jsonify({"status":"error","message":"invalid token"})
    # Get Top UnSolved Question
    #
    return jsonify({"status":"success",})

@app.route("/top/rated",methods=["GET"])
def top_rated():
    data = request.get_json()
    # Handle Authentication and Get User
    token = data.get("token")
    user = validate_token("token")
    if user is None:
        return jsonify({"status":"error","message":"invalid token"})
    # Get Top Rated Question
    #
    return jsonify({"status":"success",})

@app.route("/top/user",methods=["GET"])
def top_user():
    data = request.get_json()
    # Handle Authentication and Get User
    token = data.get("token")
    user = validate_token("token")
    if user is None:
        return jsonify({"status":"error","message":"invalid token"})
    # Get Top Rated User
    #
    return jsonify({"status":"success",})

@app.route("/register",methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    invite = data.get("invite")
    if username is None or password is None:
        return jsonify({"status": "error", "message": "no username or password"})
    # Check Invite Add User to Database
    new_invite = aadeesh.checkInviteCode(username,password,invite)
    if new_invite == 0:
        return jsonify({"status": "error", "message": "invalid invite"})
    if new_invite == 1:
        return jsonify({"status": "error", "message": "username already exists"})
    return jsonify({"status": "success", "invite": new_invite})

@app.route("/login",methods=["POST"])
def login():
    data =request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username is None or password is None:
        return jsonify({"status": "error", "message": "no username or password"})
    # Check Password
    res = aadeesh.login(username,password) 
    if res == 0:
        return jsonify({"status": "error", "message": "invalid username or password"})
    # Generate Token
    token = jwt.encode({"username": username,"exp":datetime.datetime.utcnow()+datetime.timedelta(hours=24)}, PRIVATE_KEY, algorithm="HS256")
    return jsonify({"status": "success", "token": token})
