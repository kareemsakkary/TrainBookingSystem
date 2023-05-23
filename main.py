import databaseSQL
import models
from datetime import datetime
db = databaseSQL.database()

# trip = db.selectAll("Trip")[0]
# acc = db.selectAll("Account")[3]
# booking = models.Booking()
# booking.account = acc
# booking.trip = trip
# booking.set_seats_num(1)
# db.addRecord(booking)
# db.deleteRecord("Trip","trip_id = 3")

# for i in db.getTrips(5):
#     print(i.departure_station,i.trip_id)
#add trip
# trip = models.Trip()
# trip.train = db.selectAll("Train")[0]
# trip.departure_station = "cairo"
# trip.arrival_station = "hurghada"
# trip.start_date = datetime(2023, 5, 25, 0, 0, 0, 0)
# trip.end_date = datetime(2023, 5, 25, 6, 0, 0, 0)
# trip.price = 400
# db.addRecord(trip)
# for i in db.selectAll("Trip"):
#     print(i.trip_id,i.departure_station,i.arrival_station)
# for i in db.getTrips(1,arrival_station="hurghada",departure_station="cairo"):
#     print("found")
#
# # for i in db.getTrips(1,arrival_station="dahab",departure_station="cairo"):
# #     print("found")
# print(db.count("Account"))
# print(db.count("Trip"))
# print(db.count("Train"))
# print(db.count("Booking"))
for i in db.tableSizes():
    print(i[1][0])