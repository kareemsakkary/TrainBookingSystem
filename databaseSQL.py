#install pyodbc with "pip install pyodbc"
import pyodbc
import models
class database:
    def __init__(self):
        self.connection = pyodbc.connect('DRIVER={SQL Server};Server={TrainBooking.mssql.somee.com};Database=TrainBooking; UID=TrainBookingSys; PWD=123456789',autocommit=True)
        
    def addRecord(self,data):
        cursor = self.connection.cursor()
        sql = f"""
        INSERT INTO {data.add()}
        """
        cursor.execute(sql)

    def deleteRecord(self,tableName,where):
        cursor = self.connection.cursor()
        sql = f"""
        DELETE FROM {tableName} WHERE {where};
        """
        cursor.execute(sql)
        
    def selectAll(self,tablename,where=None ):
        cursor = self.connection.cursor()
        sql = ""
        if(where == None):
            sql = f"""select * from {tablename}"""
        else:
            sql = f"""select * from {tablename} WHERE {where}"""
        cursor.execute(sql)
        row = cursor.fetchone()
        li = []
        while row:
            if(tablename == "Account"):
                if(row[3] == "Customer"):
                    li.append(models.Customer(row))
                else :
                    li.append(models.Admin(row))
            elif(tablename == "Train"):
                li.append(models.Train(row))
            elif(tablename=="Trip"):
                trip = models.Trip(row)
                trip.train = selectAll("Train",f"train_id = {row[1]};")[0]
                trip.seats = selectAll("Seat",f"trip_id = {row[0]};")
                li.append(trip)
            elif(tablename=="seat"):
                li.append(models.Seat)
            row=cursor.fetchone()   
        return li