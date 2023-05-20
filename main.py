import databaseSQL
import models
import datetime
db = databaseSQL.database()
print(db.count("Seat","status ='available'"))
name = 'kareem'
acc = db.selectAll("Account",f"name = '{name}'")[0]
print(acc.email)