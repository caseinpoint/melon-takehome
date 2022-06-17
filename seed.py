from subprocess import run
from server import app
from model import connect_to_db, db, Reservation
from datetime import date, datetime

run(['dropdb', 'melon_reservations'])
run(['createdb', 'melon_reservations'])

connect_to_db(app)
db.create_all()

# generate reservations for user0
today = date.today()
start_times = []
for i in range(10):
    start_times.append(datetime(today.year, today.month, today.day + i, 12))

username = 'user0'
for start_time in start_times:
    new_reservaton = Reservation(username=username, start_time=start_time)

    db.session.add(new_reservaton)

db.session.commit()
