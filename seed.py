from subprocess import run
from server import app
from model import connect_to_db, db, Reservation
from datetime import date, datetime

run(['dropdb', 'melon_reservations'])
run(['createdb', 'melon_reservations'])

connect_to_db(app)
db.create_all()

# generate reservations for users 0 - 9 (user0, user1, user2 ... user9)
today = date.today()
usernames = []
start_times = []

for i in range(10):
    usernames.append("user" + str(i))

    start_times.append(datetime(today.year, today.month, today.day + i, 12))

for username in usernames:
    for start_time in start_times:
        new_reservaton = Reservation(username=username, start_time=start_time)

    db.session.add(new_reservaton)

db.session.commit()

