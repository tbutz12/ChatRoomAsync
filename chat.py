import json
from flask import Flask, request, abort, url_for, redirect, session, render_template, flash
from datetime import datetime

app = Flask(__name__)

users = {}
chatList = {}
items = []

@app.route("/")
def default():
    return redirect(url_for("login"))
    
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["user"]
        if session["username"] not in users:
            return redirect(url_for("registration"))
        return redirect(url_for("homepage", username=session["username"]))
    return render_template("login.html")

@app.route("/room/<username>", methods=["GET", "POST"])
def homepage(username = None):
    if not username:
        return redirect(url_for("login"))
    elif "username" in session:
        flag2 = False
        if not chatList:
            flag2 = True
        return render_template("homepage.html", list = chatList, name = session["username"], flag2 = flag2)

@app.route("/registration/", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        userName = request.form["user"]
        if(userName in users):
            usernameError = True
            return render_template("registration.html", usernameError = usernameError)
        users[userName] = request.form["pass"]
        passW = request.form["pass"]
        if(len(userName) == 0):
            return render_template("registration.html")
        passW = request.form["pass"]
        if(len(passW) == 0):
            return render_template("registration.html")
        session["username"] = userName
        return redirect(url_for("login"))
    return render_template("registration.html")

@app.route("/viewChatRoom/<name>", methods=["GET", "POST"])
def viewChatRoom(name = None):
    if not name:
        return render_template("homepage.html", list = chatList, name = session["username"], deleted = True)
    if(session.get("inChatRoom") == True):
        currentlyIn = session["inChatRoom"]
        if(currentlyIn):
            flag = True
            return render_template("homepage.html", list = chatList, flag = flag)
    session["inChatRoom"] = True
    forumName = name
    newItems = []
    for x in items:
        if x[1] == forumName:
            newItems.append(x[0])
    return render_template("viewChatRoom.html", name = name, items=newItems)

@app.route("/hostEnd/", methods=["GET", "POST"])
def hostEnd(name = None):
    session["inChatRoom"] = False
    if not chatList:
        flag2 = True
    else:
        flag2 = False
    return render_template("homepage.html", list = chatList, name = session["username"], flag2=flag2)

@app.route("/createChatRoom/", methods=["GET", "POST"])
def createChatRoom():
    if request.method == "POST":
        chatRoomName = request.form["name"]
        chatList[chatRoomName] = session["username"]
        return render_template("createChatRoom.html", list = chatList)
    return render_template("createChatRoom.html")

@app.route("/logout/")
def logout():
    if "username" in session:
        session.clear()
        return render_template("logoutPage.html")
    else:
        return redirect(url_for("login"))
@app.route("/messages", methods=["GET"])
def get_items():
    forumName = request.args.get("forumName")
    newItems = []
    for x in items:
        if x[1] == forumName:
            newItems.append(x[0])
    return json.dumps(newItems)

@app.route("/new_message", methods=["POST"])
def add():
    items.append([request.form["message"], request.form["forumName"]])
    return "Success!"

@app.route("/leaveChat", methods=["GET"])
def leaveChat():
    session["inChatRoom"] = False
    return redirect(url_for("homepage", username = session["username"]))

@app.route("/deleteChat<chatName>", methods=["POST"])
def deleteChat(chatName = None):
    global items
    if request.method == "POST":
        del chatList[chatName]
        items = [item for item in items if item[1] != chatName]
    return render_template("homepage.html", list = chatList, name = session["username"])

app.secret_key = "asdf;lkj"
            
if __name__ == "__main__":
    app.run()

