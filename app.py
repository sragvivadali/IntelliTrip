from flask import Flask, render_template, redirect, url_for, session, request, send_file
from flask_session import Session

import requests
import json
import math

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
	"password": "test123"
}

user2 = {
	"email": "user2@gmail.com",
	"password": "test123"
}

user3 = {
	"email": "user3@gmail.com",
	"password": "test123"
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
            "password": request.form["pw"]
        }

        accountExists = False

        for user in users:
            if newUser.get("email") == user.get("email"):
                accountExists = True
        
        if not accountExists:
            print("Registration successful!")
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