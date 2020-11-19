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
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

user_table_headers = ["user_id", "user_name", "diet_default", "car_travel_default", "train_travel_default",
    "bus_travel_default", "food_disposal_default", "plastic_disposal_default", "paper_disposal_default",
    "glass_disposal_default", "tin_disposal_default", "mobile_screentime_default", "computer_screetime_default",
    "tv_screentime_default"]

report_table_headers = ["date", "user_id", "use_defaults", "diet", "car_travel", "train_travel", "bus_travel", "food_disposal",
    "plastic_disposal", "paper_disposal", "glass_disposal", "tin_disposal", "mobile_screentime", "computer_screentime", "tv_screentime"]

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
        # Check this user doesn't already have a report today.
        get_report_query = "SELECT * FROM Reports WHERE user_id = '{}' and date = '{}';"
        get_report_query = get_report_query.format(user_id, date)
        cursor = db.cursor(dictionary=True)
        cursor.execute(get_report_query)
        results = cursor.fetchall()
        if len(results) != 0:
            return "This user has already reported for date."
        # Add the report to the database.
        report = request.json
        # Extract the report features from the request body.
        report_features = []
        for header in report_table_headers:
            if type(report[header]) == str:
                # Wrap strings with quotes
                report_features.append("'{}'".format(report[header]))
            else:
                report_features.append(str(report[header]))
        # Insert the new user.
        insert_report_query = "INSERT INTO Reports ({}) VALUES ({});".format(", ".join(report_table_headers), ", ".join(report_features))
        print(insert_report_query)
        cursor.execute(insert_report_query)
        db.commit()
        return "Done."
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
    # Get all the reports for the past week.
    get_reports_from_past_week_query = "SELECT * FROM Reports WHERE date >= curdate()-7 AND date < curdate()+1;"
    cursor = db.cursor(dictionary=True)
    cursor.execute(get_reports_from_past_week_query)
    results = cursor.fetchall()
    # Compute scores for each user.
    all_users_scores_1w = {}
    for report in results:
        # print(report)
        user_id = report["user_id"]
        # Add new dict if its the frst report for this user.
        if user_id not in all_users_scores_1w:
            # Get user_name for this user_id.
            get_user_name = "SELECT user_name FROM Users WHERE user_id = '{}';".format(user_id)
            cursor = db.cursor(dictionary=True)
            cursor.execute(get_user_name)
            user_name = cursor.fetchall()[0]["user_name"]
            all_users_scores_1w[user_id] = {
                "user_id": user_id,
                "user_name": user_name,
                "diet_score": 0,
                "car_travel_score": 0,
                "bus_travel_score": 0,
                "train_travel_score": 0,
                "food_disposal_score": 0,
                "plastic_disposal_score": 0,
                "paper_disposal_score": 0,
                "glass_disposal_score": 0,
                "tin_disposal_score": 0,
                "mobile_screentime_score": 0,
                "computer_screentime_score": 0,
                "tv_screentime_score": 0,
                "total_score": 0
            }
        # Increment scores for each area and total
        # diet
        diet_score = diet_to_score(report["diet"])
        all_users_scores_1w[user_id]["diet_score"] += diet_score
        all_users_scores_1w[user_id]["total_score"] += diet_score
        # car_travel
        car_travel_score = car_travel_to_score(report["car_travel"])
        all_users_scores_1w[user_id]["car_travel_score"] += car_travel_score
        all_users_scores_1w[user_id]["total_score"] += car_travel_score
        # bus_travel
        bus_travel_score = bus_travel_to_score(report["bus_travel"])
        all_users_scores_1w[user_id]["bus_travel_score"] += bus_travel_score
        all_users_scores_1w[user_id]["total_score"] += bus_travel_score
        # train_travel
        train_travel_score = train_travel_to_score(report["train_travel"])
        all_users_scores_1w[user_id]["train_travel_score"] += train_travel_score
        all_users_scores_1w[user_id]["total_score"] += train_travel_score
        # food_disposal
        food_disposal_score = disposal_to_score(report["food_disposal"])
        all_users_scores_1w[user_id]["food_disposal_score"] += food_disposal_score
        all_users_scores_1w[user_id]["total_score"] += food_disposal_score
        # plastic_disposal
        plastic_disposal_score = disposal_to_score(report["plastic_disposal"])
        all_users_scores_1w[user_id]["plastic_disposal_score"] += plastic_disposal_score
        all_users_scores_1w[user_id]["total_score"] += plastic_disposal_score
        # paper_disposal
        paper_disposal_score = disposal_to_score(report["paper_disposal"])
        all_users_scores_1w[user_id]["paper_disposal_score"] += paper_disposal_score
        all_users_scores_1w[user_id]["total_score"] += paper_disposal_score
        # glass_disposal
        glass_disposal_score = disposal_to_score(report["glass_disposal"])
        all_users_scores_1w[user_id]["glass_disposal_score"] += glass_disposal_score
        all_users_scores_1w[user_id]["total_score"] += glass_disposal_score
        # tin_disposal
        tin_disposal_score = disposal_to_score(report["tin_disposal"])
        all_users_scores_1w[user_id]["tin_disposal_score"] += tin_disposal_score
        all_users_scores_1w[user_id]["total_score"] += tin_disposal_score
        # mobile_screentime
        mobile_screentime_score = mobile_screentime_to_score(report["mobile_screentime"])
        all_users_scores_1w[user_id]["mobile_screentime_score"] += mobile_screentime_score
        all_users_scores_1w[user_id]["total_score"] += mobile_screentime_score
        # computer_screentime
        computer_screentime_score = computer_screentime_to_score(report["computer_screentime"])
        all_users_scores_1w[user_id]["computer_screentime_score"] += computer_screentime_score
        all_users_scores_1w[user_id]["total_score"] += computer_screentime_score
        # tv_screentime
        tv_screentime_score = tv_screentime_to_score(report["tv_screentime"])
        all_users_scores_1w[user_id]["tv_screentime_score"] += tv_screentime_score
        all_users_scores_1w[user_id]["total_score"] += tv_screentime_score
    return all_users_scores_1w

def diet_to_score(diet):
    if diet == "meat":
        return 4
    elif diet == "vegeterian":
        return 3
    elif diet == "pescetarian":
        return 2
    elif diet == "vegan":
        return 1
    else:
        return 0

def car_travel_to_score(car_travel):
    return car_travel*3

def bus_travel_to_score(bus_travel):
    return bus_travel*2

def train_travel_to_score(train_travel):
    return train_travel*1

def disposal_to_score(disposal):
    if disposal == 1:
        # Did dispose properly, not penalty score.
        return 0
    else:
        # Penalty score for not disposing properly.
        return 1

def mobile_screentime_to_score(mobile_screentime):
    return mobile_screentime*1

def computer_screentime_to_score(computer_screentime):
    return computer_screentime*2

def tv_screentime_to_score(tv_screentime):
    return tv_screentime*3

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)