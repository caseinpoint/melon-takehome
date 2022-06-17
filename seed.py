from subprocess import run
import model
import server
import datetime

run(['dropdb', 'melon_reservations'])
run(['createdb', 'melon_reservations'])

model.connect_to_db(server.app)
model.db.create_all()

# generate reservations for users 0 - 9 (user0, user1, user2 ... user9)
# on dates corresponding to their user number (October 1 - 10) at 9am
for i in range(10):
    username = "user" + str(i)
    reservation_start = datetime.datetime(2022, 5, i + 1, 9)
    new_reservaton = model.Reservation(username=username, start_time=reservation_start)
    model.db.session.add(new_reservaton)
    model.db.session.commit()

