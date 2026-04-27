# Back End Full_Stack App
from flask import Flask, request, jsonify
import sqlite3
import json
import os

# create the backend application, which only works with the database
backend_app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(basedir, 'database.db')

# function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ENDPOINTS
@backend_app.route("/api", methods=["GET"])
def get_all():
    # retrieve list from the database
    # connect to DB, run the SQL statement, close the connection
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM destinations').fetchall()
    conn.close()
    # the variable rows now contains a list of sqlite Row objects,
    # which needs to be converted to a list of dictionaries (i.e. json)
    result_list = [dict(row) for row in rows]
    # now we can send it to the json library to convert it to a string
    json_output = json.dumps(result_list, indent=4)
    return(json_output), 200  # creates response json, returns HTTP response 200

# create a new destination
@backend_app.route("/api/new", methods=["POST"])
def create_dest():
    # get info from POST request
    data = request.get_json()  # parses incoming json
    dest_name = data[0].get("destination")
    dest_note = data[1].get("notes")
    dest_cost = data[2].get("cost")
    # TODO: Input validation on all fields prior to database insertion!

    # Connect to DB and insert information
    conn = get_db_connection()
    conn.execute('INSERT INTO destinations (destination, notes, cost) VALUES (?, ?, ?)',
                 (dest_name, dest_note, dest_cost ))
    conn.commit()
    conn.close()
    return jsonify({"destination": dest_name}), 201  # creates response json, returns HTTP response 201

if __name__ == "__main__":
    # We use port 5001 so it doesn't clash with your frontend on 5000
    # debug=True ensures you see errors in the terminal
    backend_app.run(port=5001, debug=True)