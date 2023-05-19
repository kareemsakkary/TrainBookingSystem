import databaseSQL
import models
import datetime
db = databaseSQL.database()
cus = models.Customer()
cus.name="waleed"
cus.email="waleed@gmail.com"
cus.address="address"
cus.password="123456789"
cus.phone_num="0111"
cus.date_of_birth = datetime.date(2002,4,25)
db.addRecord(cus)
# db.deleteRecord("Users","name = 'waleed 3l2'")
for i in db.selectAll("Users"):
    print(i.name)
