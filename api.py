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

user_table_headers = ["user_id", "user_name", "diet_default", "car_travel_default", "train_travel_default",
        "bus_travel_default", "food_disposal_default", "plastic_disposal_default", "paper_disposal_default",
        "glass_disposal_default", "tin_disposal_default", "mobile_screentime_default", "computer_screetime_default",
        "tv_screentime_default"]

@app.route("/users/<string:user_id>/", methods=["GET", "PUT", "POST", "DELETE"])
def users(user_id):
    if request.method == "POST":
        user = request.json
        print(user)
        print(type(user))
        # Make sure the user doesn't already exist before creatin one.
        get_user_query = "SELECT * FROM Users WHERE user_id = '{}';"
        cursor = db.cursor(dictionary=True)
        cursor.execute(get_user_query.format(user_id))
        results = cursor.fetchall()

        if len(results) == 0:
            # No user with user_id so create new user.
            # Extract the user features from the request body.
            user_features = []
            for header in user_table_headers:
                if type(user[header]) == str:
                    # Wrap strings with quotes
                    user_features.append("'{}'".format(user[header]))
                else:
                    user_features.append(str(user[header]))
            # Insert the new user.
            insert_user_query = "INSERT INTO Users ({}) VALUES ({});".format(", ".join(user_table_headers), ", ".join(user_features))
            # print(insert_user_query)
            cursor.execute(insert_user_query)

            # Insert the user into Organisations.
            for organisation_name in user["organisations"]:
                insert_organisations_query = "INSERT INTO Organisations (user_id, organisation_name) VALUES ('{}', '{}');".format(user_id, organisation_name)
                print(insert_organisations_query)
                cursor.execute(insert_organisations_query)

            # Commit changes to mysql.
            db.commit()
            return "Done."
        else: # len(results) == 1
            return "User already exists."

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
        # Not implemented as updating the user in frontend uses post.
        return ""
    else: # request.method == "DELETE":
        # Query to delete from users.
        query = "DELETE FROM {0} WHERE user_id = '{1}';"
        # Delete from all tables.
        for table in ("Users", "Organisations", "Reports"):
            formatted_query = query.format(table, user_id)
            cursor.execute(formatted_query)
        db.commit()
        return "Done."

@app.route("/users/<string:user_id>/report/<string:date>/", methods=["GET", "PUT", "POST", "DELETE"])
def user_reports(user_id, date):
    if request.method == "POST":
        return ""
    elif request.method == "GET":
        get_report_query = "SELECT * FROM Reports WHERE user_id = '{}' and date = '{}';"
        get_report_query = get_report_query.format(user_id, date)
        cursor = db.cursor(dictionary=True)
        cursor.execute(get_report_query)
        results = cursor.fetchall()
        if len(results) == 0:
            return "No reports with date and user_id."
        else:
            report = results[0]
            # Format date
            report["date"] = report["date"].isoformat()
            return report
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
    # print(os.environ)
    app.run(debug=True, host='0.0.0.0', port=port)