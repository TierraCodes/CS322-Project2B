# Front End Full-Stack App
from flask import Flask, render_template, request, flash
import requests
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
        # TODO: validate the form information before making the backend request

        # build json with requested data
        new_dest = {
            "destination": dest_name,
            "notes": dest_notes,
            "cost": dest_cost
        }
        # send a POST request to the backend to create a new entry
        response = requests.post(backend_url + "/api/new", json=new_dest)
        # Give the user a message
        return f'<h1>Your form was submitted to add {dest_name}. <a href="/home">Continue</a></h1>'

if __name__ == "__main__":
    # We use port 5001 so it doesn't clash with your frontend on 5000
    # debug=True ensures you see errors in the terminal
    frontend_app.run(port=5000, debug=True)
