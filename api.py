from flask import Flask, request
from flask_cors import CORS
import mysql.connector
import csv
import os

try:
    # Heroku, use Config vars
    host = os.getenv('host')
    port = os.getenv('port')
    user = os.getenv('user')
    password = os.getenv('password')
except:
    # Local environment, use credentials.csv
    with open('credentials.csv') as file:
        reader = csv.reader(file, delimiter=',')
        credentials = next(reader)
    host = credentials[0]
    port = credentials[1]
    user = credentials[2]
    password = credentials[3]


# Connect to mysql instance.
db = mysql.connector.connect(
  host=host,
  port=port,
  user=user,
  password=password,
  database="azhack"
)

@app.route("/users/<string:user_id>/", methods=["GET", "PUT", "POST", "DELETE"])
def users(user_id):
    print(request.args)
    if request.method == "POST":
        #request.form
        return ""
    elif request.method == "GET":
        return ""
    elif request.method == "PUT":
        return ""
    else: # request.method == "DELETE":
        return ""

@app.route("/users/<string:user_id>/report/<string:date>/", methods=["GET", "PUT", "POST", "DELETE"])
def user_reports(user_id, date):
    if request.method == "POST":
        return ""
    elif request.method == "GET":
        return ""
    elif request.method == "PUT":
        return ""
    else: # request.method == "DELETE":
        return ""

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    return ""

@app.route("/leaderboard/<string:organisation_name>", methods=["GET"])
def leaderboard_organisation():
    return ""

if __name__ == "__main__":
    app = Flask(__name__)
    CORS(app)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)