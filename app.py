from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Hardcoded username and password for demonstration purposes
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# code here in website
@app.route('/')
def home_page():
    return render_template('index.html')

# code here in login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password."})

if __name__ == '__main__':
    app.run(debug=True)
