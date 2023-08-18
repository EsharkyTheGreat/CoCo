from flask import Flask, jsonify, request
import jwt
import backend_a as aadeesh

PRIVATE_KEY = "esharkyisthecoolestherointhiswholeworld"

def validate_token(token):
    try:
        return jwt.decode(token, PRIVATE_KEY, algorithms=["HS256"])['username']
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
    aadeesh.addQuestion(user, question)
    if question is None:
        return jsonify({"status": "error", "message": "no question"})
    return jsonify({"status": "ok"})

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
    return jsonify({"status": "ok", "questions": questions})

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
    aadeesh.addQuestion(user, question)
    return jsonify({"status": "ok"})

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
    return jsonify({"status": "ok", "leaderboard": leaderboard})

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
    return jsonify({"status": "ok", "invite": new_invite})

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
    token = jwt.encode({"username": username}, PRIVATE_KEY, algorithm="HS256")
    return jsonify({"status": "ok", "token": token})
