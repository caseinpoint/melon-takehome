from flask import Flask, render_template, request, flash, session, redirect, jsonify
from datetime import datetime, timedelta
from dateutil.parser import parse
from model import Reservation, db, connect_to_db
from os import environ

app = Flask(__name__)

app.secret_key = environ["APP_SECRET_KEY"]


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("index.html")

@app.route("/logout")
def logout():
    """Logout and redirect homepage."""

    session.clear()

    return redirect("/")


@app.route("/reservations", methods=["POST", "GET"])
def get_user_reservations():
    """ Retrieve reservations the user has made."""
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
    else:
        # assign a value to username is user is in session
        if 'username' in session:
            username = session["username"]
        # if the user is not in session, redirect them to the homepage
        else:
            return redirect("/")
    existing_reservations = Reservation.retrieve_reservations(username)

    return render_template("reservations.html", reservations=existing_reservations)

@app.route("/schedule")
def render_schedule():
    """ View scheduling page."""
    return render_template("schedule.html")

@app.route("/reservations/delete", methods=["POST"])
def delete_reservation():
    """ Delete reservations the user has made."""
    reservation_start = parse(request.json.get("startTime"))
    username = session["username"]

    reservation_to_delete = Reservation.find_reservation_by_start_and_user(
        reservation_start, username
    )
    db.session.delete(reservation_to_delete)
    db.session.commit()
    return "Success"

@app.route("/reservations/book", methods=["POST"])
def make_reservation():
    """ Create a reservation with the specified user and time."""
    reservation_start = parse(request.form.get("start_time"))
    # reservation_start = parse(request.form.get("start_time"), ignoretz=True)
    username = session["username"]

    new_reservation = Reservation.create_reservation(username, reservation_start)
    db.session.add(new_reservation)
    db.session.commit()
    return redirect("/reservations")

@app.route("/search_reservations", methods=["GET"])
def search_reservation():
    start_time = parse(request.args.get("startTime"))
    end_time = parse(request.args.get("endTime"))

    available_times = Reservation.available_reservations(start_time, end_time, session["username"])
    return jsonify(available_times)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)