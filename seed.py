from subprocess import run
from server import app
from model import connect_to_db, db, Reservation
from datetime import date, datetime, timedelta

run(['dropdb', 'melon_reservations'])
run(['createdb', 'melon_reservations'])

connect_to_db(app)
db.create_all()

# generate reservations for users 0 - 9 (user0, user1, user2 ... user9)
now = datetime.now()
for i in range(10):
    username = "user" + str(i)

    reservation_start = datetime.datetime(2022, 5, i + 1, 9)

    new_reservaton = Reservation(username=username, start_time=reservation_start)

    db.session.add(new_reservaton)
    db.session.commit()

