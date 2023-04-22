from flask import Flask, render_template, redirect, url_for, session, request, send_file
from flask_session import Session

import requests
import json
import math
import random
import string

app = Flask(__name__)
app.secret_key = "thisisasecretkeydonttellanyone"

def getItinerary():

	url = "https://gpt-chatbotapi.p.rapidapi.com/ask"

	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "1245c0d08cmsh6048f1f2b40e429p1f824ejsnda64bb5ace07",
		"X-RapidAPI-Host": "gpt-chatbotapi.p.rapidapi.com"
	}

	promptInput = input("Where do you want to visit? ")
	prompt = "Things you must do at " + promptInput
	payload = {"query": prompt}

	dataCity = requests.request("POST", url, json=payload, headers=headers)

	json_txt_city = dataCity.text

	data = json.loads(json_txt_city)
	response = data['response']

	promptIt = "Given these locations, make a detailed day by day itinerary for a $500 budget per day while including resturants and hotel: \n" + response
	payload = {"query": promptIt}

	dataPlan = requests.request("POST", url, json=payload, headers=headers)

	json_txt = dataPlan.text

	dataIt = json.loads(json_txt)
	response = dataIt['response']

	print(response)

users = []

user1 = {
	"email": "user1@gmail.com",
    "name": "User1",
    "prefs": ["cityhustler", "socialmediacrazy", "lovebirds", "naturelover"],
	"password": "test123",
    "group": ""
}

user2 = {
	"email": "user2@gmail.com",
    "name": "User2",
    "prefs": ["cityhustler", "socialmediacrazy"],
	"password": "test123",
    "group": ""
}

user3 = {
	"email": "user3@gmail.com",
    "name": "User3",
    "prefs": ["cityhustler", "socialmediacrazy"],
	"password": "test123",
    "group": ""
}

users.append(user1)
users.append(user2)
users.append(user3)

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
            "group": request.form["gr"]
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

@app.route("/logout")
def logout():
    session.pop("currentUser", None)
    return redirect(url_for("index"), code=302)

@app.route('/mini_logo.png')
def mini_logo():
    filename = 'mini_logo.png'
    return send_file(filename, mimetype='image/png')

@app.context_processor
def context_processor():
    global users

    session.modified = True

    isLoggedIn = False
    currentUser = None

    if "currentUser" in session:
        isLoggedIn = True
        currentUser = session["currentUser"]

    return dict(isLoggedIn=isLoggedIn, users=users, currentUser=currentUser)

if __name__ == "__main__":
    app.run(debug=True)

# personality = {
#         "Thrillers": False,
#         "InvisibleHopper" : False,
#         "CityHustler" : False,
#         "LoneWolf" : False,
#         "TypicalTraveller" : False,
#         "SocialMediaCrazy" : False,
#         "LoveBirds" : False,
#         "NatureLover" : False,
#         "Foodie" : False,
#         "NightOwl" : False
#     }

description = {
        "Thrillers": "adrenaline activities",
        "InvisibleHopper" : "relaxing",
        "CityHustler" : "city activities",
        "LoneWolf" : "secluded areas",
        "TypicalTraveller" : "tourist spot",
        "SocialMediaCrazy" : "picture places",
        "LoveBirds" : "romantic activities",
        "NatureLover" : "natural places",
        "Foodie" : "good local food",
        "NightOwl" : "night life"
    }

# users = {}
# userGroups = {}
groups = {}

def createGroup(self):
    group_name = input("Enter group name: ")

     # generate random 5-letter alphanumeric code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        # check if the generated code already exists
    while code in self.groups:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        # add the new group to the dictionary
    currUser = session["currentUser"]
    currUser["group"] = code
    
    groups[code] = group_name

    print(f"Group '{group_name}' has been created with code '{code}'.")

def joinGroup():
    code = input("Enter 5-letter alphanumeric code to join group: ")

    if code in groups:
        group_name = groups[code]
        currUser = session["currentUser"]
        currUser["group"] = code
        print(f"You have joined {group_name}!")
    else:
        print("Invalid code. Please try again.")

def getGroup(str):
    usersInGroup = []
    for user in users:
        if user["group"] == str:
            usersInGroup.append(user)
    return usersInGroup



# def toggleType(typeName) -> bool:
#     personality[typeName] = not personality[typeName]