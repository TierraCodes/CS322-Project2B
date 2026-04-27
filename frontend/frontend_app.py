# Front End Full-Stack App
from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from requests import RequestException

# Note the two libraries:
#
# flask.request processes incoming requests to the frontend server
# (in other words, form submissions)
#
# the python requests library (plural!) sends requests to
# a different server:  the backend server
# need to execute in Terminal:    pip install requests

# create the frontend app, which talks to the user, receives
# user requests, and then approves them to be sent to the backend
frontend_app = Flask(__name__)
backend_url = "http://127.0.0.1:5001"
frontend_app.secret_key = "security_key"

# ROUTES

# view all destinations on homepage
@frontend_app.route("/")
@frontend_app.route("/home")
def home():
    # send a request to the backend for all the destinations
    # NOTE: the response variable includes the entire HTTP response
    # NOTE: can use print(dest_list.json()) # can use for debugging
    try:
        # 1. Ask the backend for the data
        response = requests.get(f"{backend_url}/api")
        response.raise_for_status()
        # 2. Parse the JSON text into a Python list
        destinations = response.json()
    except Exception as e:
        destinations = []
        flash(f"Error connecting to backend: {e}")

    # now, pass the data returned from the backend to the template and
    # render it (send it to the client computer as an HTML file)
    return render_template('bucketlist.html', places=destinations)

# add a new destination
@frontend_app.route("/new_destination", methods=["GET", "POST"])
def new_destination():
    # if GET request, display the form
    if request.method == "GET":
        return render_template('new_destination.html')
    # process the submitted form on a POST request
    if request.method == "POST":
        # Retrieve data from the form using the 'name' attribute
        dest_name = request.form.get('dest_name')
        dest_notes = request.form.get('dest_notes')
        dest_cost = request.form.get('dest_cost')

        if not dest_name or len(dest_name) > 20:
            flash("Invalid destination name.")
            return redirect(url_for('new_destination'))
        if len(dest_notes) > 20:
            flash("Notes must be 20 characters or less.")
            return redirect(url_for('new_destination'))
        try:
            cost_val = float(dest_cost)
            if cost_val < 0 or cost_val > 1000000:
                raise ValueError
        except (ValueError, TypeError):
            flash("Please enter a valid cost between 0 and 1,000,000.")
            return redirect(url_for('new_destination'))

        # build json with requested data
        new_dest = {
            "destination": dest_name,
            "notes": dest_notes,
            "cost": dest_cost
        }

        try:
            # SECURITY: Always use timeouts on POST requests to prevent hanging connections.
            response = requests.post(f"{backend_url}/api/new", json=new_dest, timeout=5)
            response.raise_for_status()
            flash(f"Successfully added {dest_name}!")
        except RequestException:
            flash("Failed to save destination. The server might be busy.")
        # send a POST request to the backend to create a new entry
        # Give the user a message
        return redirect(url_for('home'))

if __name__ == "__main__":
    # We use port 5001 so it doesn't clash with your frontend on 5000
    # debug=True ensures you see errors in the terminal
    frontend_app.run(port=5000, debug=True)
