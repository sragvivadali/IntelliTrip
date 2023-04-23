from flask import Flask, render_template, redirect, url_for, session, request, send_file
from flask_session import Session

import cohere

import requests
import json
import math
import random
import string

app = Flask(__name__)
app.secret_key = "thisisasecretkeydonttellanyone"

users = []

user1 = {
	"email": "john@gmail.com",
    "name": "John Doe",
    "prefs": ["cityhustler", "socialmediacrazy", "lovebirds"],
    "trips": ["Lisbon", "New York City", "Tokyo"],
	"password": "test123",
    "group": ""
}

user2 = {
	"email": "jane@gmail.com",
    "name": "Jane Doe",
    "prefs": ["cityhustler", "socialmediacrazy"],
    "trips": ["Chicago", "Seoul"],
	"password": "test123",
    "group": "YWQTL"
}

user3 = {
	"email": "john@gmail.com",
    "name": "John Smith",
    "prefs": ["socialmediacrazy"],
    "trips": [],
	"password": "test123",
    "group": ""
}

user4 = {
	"email": "brady@gmail.com",
    "name": "Tom Brady",
    "prefs": ["cityhustler", "socialmediacrazy", "naturelover"],
    "trips": [],
	"password": "test123",
    "group": "YWQTL"
}

user5 = {
	"email": "jim@gmail.com",
    "name": "Jim Carrey",
    "prefs": ["typicaltraveller", "foodie"],
    "trips": [],
	"password": "test123",
    "group": ""
}

user6 = {
	"email": "britney@gmail.com",
    "name": "Britney Spears",
    "prefs": ["nightowl", "lovebirds"],
    "trips": [],
	"password": "test123",
    "group": "YWQTL"
}

user7 = {
	"email": "oprah@gmail.com",
    "name": "Oprah Winfrey",
    "prefs": [],
    "trips": [],
	"password": "test123",
    "group": ""
}

user8 = {
	"email": "joe@gmail.com",
    "name": "Joe Biden",
    "prefs": ["thrillers", "lonewolf", "foodie"],
    "trips": [],
	"password": "test123",
    "group": "YWQTL"
}

user9 = {
	"email": "bill@gmail.com",
    "name": "Bill Gates",
    "prefs": ["nightowl", "lonewolf"],
    "trips": [],
	"password": "test123",
    "group": ""
}

user10 = {
	"email": "brad@gmail.com",
    "name": "Brad Pitt",
    "prefs": ["cityhustler", "thrillers"],
    "trips": [],
	"password": "test123",
    "group": ""
}

users.append(user1)
users.append(user2)
users.append(user3)
users.append(user4)
users.append(user5)
users.append(user6)
users.append(user7)
users.append(user8)
users.append(user9)
users.append(user10)

groups = {"YWQTL": "Vacationers"}

@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def index():
    # getItinerary()
	global users

	if "currentUser" not in session:
		return redirect(url_for('login'))
    
	return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    
    global users

    if request.method == "POST":
        # Get login form data

        newUser = {
            "email": request.form["em"],
            "password": request.form["pw"]
        }

        accountMatch = False

        for user in users:
            if newUser.get("email") == user.get("email") and newUser.get("password") == user.get("password"):
                session["currentUser"] = user
                accountMatch = True

        if accountMatch:
            return redirect(url_for('index'))
        else:
            print("Incorrect email or password!")
            return render_template("login.html")
        
    elif "currentUser" in session:
        return redirect(url_for('index'))
    elif request.method == "GET" or "currentUser" not in session:
        return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    global users

    if request.method == "POST":
        # Get register form data

        newUser = {
            "email": request.form["em"],
            "name": request.form["nm"],
            "password": request.form["pw"],
            "trips": [],
            "group": ""
        }

        accountExists = False

        for user in users:
            if newUser.get("email") == user.get("email"):
                accountExists = True
        
        if not accountExists:
            print("Registration successful!")
            newUserPrefs = []
            if request.form.get("thriller") != None:
                newUserPrefs.append("thriller")
            if request.form.get("invisiblehopper") != None:
                newUserPrefs.append("invisiblehopper")
            if request.form.get("cityhustler") != None:
                newUserPrefs.append("cityhustler")
            if request.form.get("lonewolf") != None:
                newUserPrefs.append("lonewolf")
            if request.form.get("typicaltraveller") != None:
                newUserPrefs.append("typicaltraveller")
            if request.form.get("socialmediacrazy") != None:
                newUserPrefs.append("socialmediacrazy")
            if request.form.get("lovebirds") != None:
                newUserPrefs.append("lovebirds")
            if request.form.get("naturelover") != None:
                newUserPrefs.append("naturelover")
            if request.form.get("foodie") != None:
                newUserPrefs.append("foodie")
            if request.form.get("nightowl") != None:
                newUserPrefs.append("nightowl")
            newUser["prefs"] = newUserPrefs
            users.append(newUser)
            session["currentUser"] = newUser
            return redirect(url_for('index'))
        else:
            print("Account with that email already exists!")
            return render_template("signup.html")
    
    elif "currentUser" in session:
        return redirect(url_for('index'))
    elif request.method == "GET" or "currentUser" not in session:
        return render_template("signup.html")

@app.route("/visit:<place>,<days>")
def visit(place, days):
    global users, groups

    if "currentUser" not in session:
        return redirect(url_for('login'))

    actualPlace = place

    for i in range(len(place)):
        if place[i] == "%":
            actualPlace = actualPlace[0:i] + " " + actualPlace[i + 4:]

    dayPlans = callAPI(actualPlace, days)

    session["currentUser"]["trips"].insert(0, actualPlace)
    
    for user in users:
        if user["email"] == session["currentUser"]["email"]:
            user["trips"] = session["currentUser"]["trips"]

    return render_template("visit.html", place=actualPlace, dayPlans=dayPlans, days=days)

@app.route("/group", methods=["POST", "GET"])
def group():
    global users, groups

    if "currentUser" not in session:
        return redirect(url_for('login'))
    # if request.method == "POST":
    #     session["currentUser"]["group"] = request.form["group_code"]
    return render_template("group.html")

@app.route("/createGroup", methods=["POST", "GET"])
def createGroup():
    global users, groups

    if "currentUser" not in session or request.method == "GET":
        return redirect(url_for('login'))
    
    createAGroup(request.form["group_name"])
    session.modified = True

    return redirect(url_for('group'))

@app.route("/joinGroup", methods=["POST", "GET"])
def joinGroup():
    global users, groups

    if "currentUser" not in session or request.method == "GET":
        return redirect(url_for('login'))
    
    joinAGroup(request.form["group_code"])
    session.modified = True 

    return redirect(url_for('group'))

@app.route("/leaveGroup", methods=["POST", "GET"])
def leaveGroup():
    global users, groups

    if "currentUser" not in session:
        return redirect(url_for('login'))
    
    session["currentUser"]["group"] = ""
    session.modified = True

    return redirect(url_for('group'))

@app.route("/logout")
def logout():
    global users, groups

    session.pop("currentUser", None)
    return redirect(url_for("index"), code=302)

@app.route('/mini_logo.png')
def mini_logo():
    filename = 'mini_logo.png'
    return send_file(filename, mimetype='image/png')

description = {
	"thrillers": "adrenaline activities",
	"invisiblehopper" : "relaxing",
	"cityhustler" : "city activities",
	"lonewolf" : "secluded areas",
	"typicaltraveller" : "tourist spot",
	"socialmediacrazy" : "picture places",
	"lovebirds" : "romantic activities",
	"naturelover" : "natural places",
	"foodie" : "good local food",
	"nightowl" : "night life"
}

def createAGroup(group_name):
    global users, groups

     # generate random 5-letter alphanumeric code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        # check if the generated code already exists
    while code in groups:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        # add the new group to the dictionary
    session["currentUser"]["group"] = code
    
    for user in users:
        if user["email"] == session["currentUser"]["email"]:
            user["group"] = code
            break

    groups[code] = group_name

    print(f"Group '{group_name}' has been created with code '{code}'.")
    session.modified = True

def joinAGroup(code):
    global users, groups

    if code in groups:
        group_name = groups[code]
        session["currentUser"]["group"] = code
        for user in users:
            if user["email"] == session["currentUser"]["email"]:
                user["group"] = code
                break
        print(f"You have joined {group_name}!")
    else:
        print("Invalid code. Please try again.")
    
    session.modified = True

def getUsersInGroup(code):
        global users, groups

        usersInGroup = []
        for user in users:
            print(user["group"] + " == " + code)
            if user["group"] == code:
                usersInGroup.append(user)
        return usersInGroup

def callAPI(place, time):
  global description

  currUser = session["currentUser"]
  firstChoice = ""
  secondChoice = ""
  thirdChoice = ""
  if currUser["group"] == "":
    i=0
    for choice in currUser["prefs"]:
      if i == 0:
        firstChoice = choice
        i = i+1
      elif i == 1:
        secondChoice = choice
        i = i + 1
      else:
        thirdChoice = choice
  else:
    code = currUser["group"]
    users = getUsersInGroup(code)
    groupPrefs = {
        "thrillers": 0,
        "invisiblehopper" : 0,
        "cityhustler" : 0,
        "lonewolf" : 0,
        "typicaltraveller" : 0,
        "socialmediacrazy" : 0,
        "lovebirds" : 0,
        "naturelover" : 0,
        "foodie" : 0,
        "nightowl" : 0
    }
    for user in users:
      for pref in user["prefs"]:
        groupPrefs[pref] = groupPrefs[pref] + 1
    

    firstChoice = "thrillers"
    for key in groupPrefs:
      if groupPrefs[key] > groupPrefs[firstChoice]:
        firstChoice = key

    if firstChoice == "thrillers":
      secondChoice = "invisiblehopper"
    else:
      secondChoice = "thrillers"
    for key in groupPrefs:
      if groupPrefs[key] > groupPrefs[secondChoice]:
        if key != firstChoice:
          secondChoice = key
    

    if firstChoice == "thrillers" or secondChoice == "thrillers":
      if firstChoice == "invisiblehopper" or secondChoice == "invisiblehopper":
        thirdChoice = "cityhustler"
      else:
        thirdChoice = "invisiblehopper"
    else:
      thirdChoice = "thrillers"

    for key in groupPrefs:
      if groupPrefs[key] > groupPrefs[thirdChoice]:
        if key != firstChoice and key != secondChoice:
          thirdChoice = key


  co = cohere.Client('D5xfH4vJcpMK3guiHwsGJ1KuutLhaNRbU3JsJb0x') # This is your trial API key
  print('KEY ', firstChoice)
  firstChoice1 = description[firstChoice]
  secondChoice1 = description[secondChoice]
  thirdChoice1 = description[thirdChoice]
  prompt = ("make a detailed %s day itinerary with five things to do per day including specific restaurants in %s for a user interested in %s, %s, %s" %(time,place,firstChoice1,secondChoice1,thirdChoice1))
  # prompt = ("make a %s day itinerary with specific restaurants for %s" % (time,place))

  response = co.generate(
    model='da0398d8-9a0f-4b8b-b670-6e6bbc304e41-ft',
    prompt= prompt,
    max_tokens=2000, #944
    temperature=0.9,
    k=0,
    stop_sequences=[],
    return_likelihoods='NONE')

  plan = response.generations[0].text

  dayPlans = []
  start = 0

  for i in range(len(plan)):
      if plan[i:i+5] == '\nDay ':
          dayPlans.append(plan[start:i-1])
          start = i

  dayPlans.append(plan[start:])
  dayPlans.pop(0)
  print(dayPlans)
  return dayPlans

@app.context_processor
def context_processor():
    global users, groups

    session.modified = True

    isLoggedIn = False
    currentUser = None

    if "currentUser" in session:
        isLoggedIn = True
        currentUser = session["currentUser"]

    def getGroupName(code):
        print(groups)
        if code in groups:
            group_name = groups[code]
            return group_name
        return "no group found"
    
    def getUsersInGroup(code):
        global users, groups

        usersInGroup = []
        for user in users:
            print(user["group"] + " == " + code)
            if user["group"] == code:
                usersInGroup.append(user)
        return usersInGroup

    return dict(isLoggedIn=isLoggedIn, users=users, groups=groups, currentUser=currentUser, getGroupName=getGroupName, getUsersInGroup=getUsersInGroup)

if __name__ == "__main__":
    app.run(debug=True)
    
    
    


