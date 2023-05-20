import databaseSQL
import models
import datetime
db = databaseSQL.database()
print(db.count("Seat","status ='available'"))
