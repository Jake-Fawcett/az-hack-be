from flask import Flask, request
from flask_cors import CORS
import mysql.connector
import csv
import os

if os.getenv('host'):
    # Heroku, use Config vars
    host = os.getenv('host')
    port = os.getenv('port')
    user = os.getenv('user')
    password = os.getenv('password')
else:
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

app = Flask(__name__)
CORS(app)

@app.route("/users/<string:user_id>/", methods=["GET", "PUT", "POST", "DELETE"])
def users(user_id):
    if request.method == "POST":
        #request.form
        return ""
    elif request.method == "GET":
        # Get the user with user_id.
        get_user_query = "SELECT * FROM Users WHERE user_id = '{}';"
        cursor = db.cursor(dictionary=True)
        cursor.execute(get_user_query.format(user_id))
        results = cursor.fetchall()
        # Return error message if no user.
        if len(results) == 0:
            return "No user with user_id={}.".format(user_id)
        # Otherwise get user data.
        user = results[0]
        # Get the user's organisations.
        get_users_organisations_query = "SELECT organisation_name FROM Organisations WHERE user_id = '{}';"
        cursor.execute(get_users_organisations_query.format(user_id))
        # Extract organisations into a list of strings.
        organisations = []
        for result in cursor.fetchall():
            organisations.append(result["organisation_name"])
        # Add the organisations to user.
        user["organisations"] = organisations
        # return the user.
        return user
    elif request.method == "PUT":
        return ""
    else: # request.method == "DELETE":
        # Query to delete from users.
        query = "DELETE FROM {0} WHERE user_id = '{1}';"
        # Delete from all tables.
        for table in ("Users", "Organisations", "Reports"):
            cursor = db.cursor(dictionary=True)
            formatted_query = query.format(table, user_id)
            cursor.execute(formatted_query)
        db.commit()
        return "Done."

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
    return "Hello World"

@app.route("/leaderboard/<string:organisation_name>", methods=["GET"])
def leaderboard_organisation():
    return ""

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(os.environ)
    app.run(debug=True, host='0.0.0.0', port=port)