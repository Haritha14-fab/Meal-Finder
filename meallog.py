from flask import Flask, render_template, request, redirect, url_for
import re
import json
import os

log = Flask(__name__)

USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# In-memory user storage: {email: password}
users = load_users()

def valid_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

def valid_password(password):
    return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password)

@log.route('/')
def home():
    return redirect(url_for('login'))

@log.route("/meal")
def meal():
    return render_template("meal.html")

@log.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    users = load_users()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        if not valid_email(email):
            error = "Invalid email format."
        elif not valid_password(password):
            error = "Password must be at least 8 characters, include uppercase, lowercase, number, and special character."
        elif email not in users:
            error = "You are not registered. Please register first."
        elif users[email] != password:
            error = "Incorrect password."
        else:
            return redirect(url_for('meal'))
    return render_template("login.html", error=error)

@log.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    users = load_users()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if not valid_email(email):
            error = "Invalid email format."
        elif not valid_password(password):
            error = "Password must be at least 8 characters, include uppercase, lowercase, number, and special character."
        elif email in users:
            error = "You already have an account. Please login."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            users[email] = password
            save_users(users)
            return redirect(url_for('login'))
    return render_template("register.html", error=error)

if __name__ == "__main__":
    log.run(debug=True, port=5001)
# This file is used to handle user login, registration, and meal management 
# To run this file, use the command: python log.py
# Ensure you have Flask installed in your environment
