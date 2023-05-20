import databaseSQL
import models
import datetime
db = databaseSQL.database()



# for i in db.selectAll("Trip"):
#     print("trip id :",i.trip_id)
#     print("train id :",i.train.train_id)
#     print("Seats :")
#     for j in i.seats :
#         print(j.seat_id)
for i in db.selectAll("Seat"):
    print(i.seat_id," ",i.trip_id)
