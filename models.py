class Account:
    def __init__(self,row=[None,None,None,None,None,None,None,None]):
        self.table = "Account"
        self.user_id = row[0]
        self.email = row[1]
        self.password = row[2]
        self.name = row[4]
        self.phone_num = row[5]
        self.address =row[6]
        self.date_of_birth =row[7]   

class Customer(Account):
    def __init__(self,row=None):
        if(row == None):
            super().__init__()
        else:
            super().__init__(row)
    def add(self) -> str:
        table= 'Account(name,password,role,email,phone_num,address,date_of_birth) '
        values =f"VALUES('{self.name}','{self.password}','customer','{self.email}','{self.phone_num}','{self.address}','{self.date_of_birth}');"
        return table+values

class Admin(Account):
    def __init__(self,row=None):
        if(row == None):
            super().__init__()
        else:
            super().__init__(row)
    def add(self) -> str:
        table= 'Account(name,password,role,email,phone_num,address,date_of_birth)'
        values =f"VALUES('{self.name}','{self.password}',admin,'{self.email}','{self.phone_num}','{self.address}','{self.date_of_birth}');"
        return table+values

class Train:
    def __init__(self,row=[None,None,None,None,None]):
        self.table = "Train"
        self.train_id = row[0]
        self.capacity = row[1]
        self.status = row[2]
        self.no_of_cart = row[3]
        self.manufacture = row[4]
        
    def add(self) -> str:
        table= 'Train(capacity,status,no_of_carts,manufacturer)'
        values =f"VALUES('{self.capacity}','{self.status}','{self.no_of_cart}','{self.manufacture}');"
        return table+values
    

class Trip:
    def __init__(self,row=[None,None,None,None,None,None,None,None,None]):
        self.table = "Trip"
        self.trip_id = row[0]
        self.train_id= row[1]
        self.price = row[2]
        self.start_date = row[3]
        self.start_time = row[4]
        self.end_date = row[5]
        self.end_time =row[6]
        self.departure_station = row[7]
        self.arrival_station = row[8]
        self.seats=[]
        self.train = None
    def add(self) -> str:
        table= 'Trip(train_id,price,start_date,end_date,start_time,end_time,departure_station,arrival_station) '
        values =f"VALUES('{self.train_id}','{self.price}','{self.start_date}','{self.end_date}','{self.start_time}','{self.end_time}','{self.departure_station}','{self.arrival_station}');"
        return table+values
class seat:
    def __init__(self,row=[None,None,None]) -> None:
        self.seat_id = row[0]
        self.trip_id = row[1]
        self.statues = row[2]
    def add(self) ->str:
        table = 'Seat(trip_id,status) '
        values = f"VALUES('{self.trip_id}','{self.statues}')'"