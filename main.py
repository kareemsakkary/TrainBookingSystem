import databaseSQL
import models
import datetime
db = databaseSQL.database()
for i in db.selectAll("Train"):
    print(i.train_id , i.status)
train = db.selectAll("Train")[0]
train.status = 'active'
db.update(train)
for i in db.selectAll("Train"):
    print(i.train_id , i.status)