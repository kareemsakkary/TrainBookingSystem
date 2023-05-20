import databaseSQL
import models
import datetime
db = databaseSQL.database()
cus = models.Customer()
cus.name ="kareem"
cus.address="helwan"
cus.date_of_birth = datetime.date(2002,4,25)
cus.email="kareem@gmail.com"
cus.password="123456789"
cus.phone_num="01222222"
db.addRecord(cus)