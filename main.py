import databaseSQL
import models
from datetime import datetime
db = databaseSQL.database()

trip = db.selectAll("Trip")[0]
acc = db.selectAll("Account")[0]
booking = models.Booking()
booking.account = acc
booking.trip = trip
booking.set_seats_num(1)
db.addRecord(booking)