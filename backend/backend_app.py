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
    try:
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM destinations').fetchall()
        conn.close()
        result_list = []
        for row in rows:
            d = dict(row)
            try:
                d['cost'] = float(d['cost'])
            except (TypeError, ValueError):
                d['cost'] = 0.00  # Default if data is corrupt
            result_list.append(d)

        return jsonify(result_list), 200
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        return jsonify({"error": "Could not retrieve data"}), 500

# create a new destination
@backend_app.route("/api/new", methods=["POST"])
def create_dest():
    # get info from POST request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    dest_name = data.get("destination", "").strip()
    dest_note = data.get("notes", "").strip()
    raw_cost = data.get("cost")

    # 2. BACKEND VALIDATION (The "Firewall")
    if not dest_name or len(dest_name) > 20:
        return jsonify({"error": "Invalid destination name (1-20 chars)"}), 400

    if len(dest_note) > 20:
        return jsonify({"error": "Notes must be 20 chars or less"}), 400

    try:
        cost_val = float(raw_cost)
        if cost_val < 0 or cost_val > 1000000:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Cost must be a number between 0 and 1,000,000"}), 400

    # 3. Secure Database Insertion
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO destinations (destination, notes, cost) VALUES (?, ?, ?)',
                     (dest_name, dest_note, cost_val))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"Added {dest_name}"}), 201
    except sqlite3.Error as e:
        print(f"SQL ERROR: {e}")
        return jsonify({"error": "Database write failed"}), 500

if __name__ == "__main__":
    # We use port 5001 so it doesn't clash with your frontend on 5000
    # debug=True ensures you see errors in the terminal
    backend_app.run(port=5001, debug=True)