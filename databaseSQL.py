#install pyodbc with "pip install pyodbc"
import pyodbc
import models
class database:
    def __init__(self):
        self.connection = pyodbc.connect('DRIVER={SQL Server};Server={TrainBooking.mssql.somee.com};Database=TrainBooking; UID=TrainBookingSys; PWD=123456789',autocommit=True)
        
    def addRecord(self,data):
        cursor = self.connection.cursor()
        sql = f""""""
        if(data.table =="Trip" and len(data.seats) > 0):
            for seat in data.seats:
                sql = f"""
                INSERT INTO Seat(seat_id,trip_id,status) VALUES {seat.add()};     
                """
                cursor.execute(sql)

        else:
            cursor = self.connection.cursor()
            sql = f"""
            INSERT INTO {data.add()}
            """
            cursor.execute(sql)
            if(data.table == "Trip"):
                trip = self.getLastRecord("Trip","Trip_id")
                trip.setTrain()
                self.addRecord(trip)
            if(data.table == "Booking"):
                cursor = self.connection.cursor()
                sql = f"""
                    UPDATE TOP({data.no_of_seats}) Seat SET status = 'booked' WHERE trip_id = {data.trip.trip_id} AND status = 'available';
                """
                cursor.execute(sql)
                data.trip = self.selectAll("Trip",f"trip_id = {data.trip.trip_id}")

    def getLastRecord(self,table_name,column):
        cursor = self.connection.cursor()
        sql =f"""
        SELECT MAX({column})
        FROM {table_name};
        """
        cursor.execute(sql)
        id = cursor.fetchone()[0]
        cursor = self.connection.cursor()
        sql =f"""
        SELECT *
        FROM {table_name} WHERE {column} = {id};
        """
        cursor.execute(sql)
        trip=None
        row = cursor.fetchall()[0]
        if(table_name == "Trip"):
            trip = models.Trip(row)
            trip.train= self.selectAll("Train",f"train_id = {row[1]};")[0]
        return trip

    def deleteRecord(self,tableName,where):
        cursor = self.connection.cursor()
        sql = f"""
        DELETE FROM {tableName} WHERE {where};
        """
        cursor.execute(sql)
        
    def selectAll(self,tablename,where=None):
        cursor = self.connection.cursor()
        sql = ""
        if(where == None):
            sql = f"""select * from {tablename}"""
        else:
            sql = f"""select * from {tablename} WHERE {where}"""
        cursor.execute(sql)
        rows = cursor.fetchall()
        li = []
        for row in rows: 
            if(tablename == "Account"):
                if(row[3] == "Customer"):
                    li.append(models.Customer(row))
                else :
                    li.append(models.Admin(row))
            elif(tablename == "Train"):
                li.append(models.Train(row))
            elif(tablename=="Trip"):
                trip = models.Trip(row)
                trip.train = self.selectAll("Train",f"train_id = {row[1]};")[0]
                trip.seats = self.selectAll("Seat",f"trip_id = {row[0]};")
                trip.ETA = trip.end_date-trip.start_date
                li.append(trip)
            elif(tablename=="Seat"):
                li.append(models.Seat(row))
            elif(tablename=="Booking"):
                booking = models.Booking(row)
                booking.trip = self.selectAll("Trip",f"trip = {row[2]};")[0]
                booking.account = self.selectAll("Account",f"account = {row[1]};")[0]
                li.append(booking)
        return li
    
    def count(self,tablename,where=None):
        return len(self.selectAll(tablename,where))
    
    def update(self,data):
        cursor = self.connection.cursor()
        sql = f"""
            UPDATE {data.table} SET {data.update()};
        """
        cursor.execute(sql)
