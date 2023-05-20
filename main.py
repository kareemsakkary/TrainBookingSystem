import databaseSQL
import models
import datetime
db = databaseSQL.database()



cus = db.selectAll("Account","account_id = 1")[0]
cus.name = "kareem"
cus.email = "sakkary@gmail.com"
db.update(cus)
