class Account:
    def __init__(self,row=[None,None,None,None,None,None,None,None]):
        self.table = "Account"
        self.account_id = row[0]
        self.email = row[1]
        self.password = row[2]
        self.role = row[3]
        self.name = row[4]
        self.phone_num = row[5]
        self.address =row[6]
        self.date_of_birth =row[7]   
    def update(self) -> str:
        st = f"""
        email = '{self.email}',
        password = '{self.password}',
        name = '{self.name}',
        phone_num = '{self.phone_num}',
        address = '{self.address}',
        date_of_birth = '{self.date_of_birth}'
         where account_id = {self.account_id}
        """
        return st
    def key(self) ->str:
        return f'account_id = {self.account_id}'
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
        values =f"VALUES('{self.name}','{self.password}','admin','{self.email}','{self.phone_num}','{self.address}','{self.date_of_birth}');"
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
        values =f"VALUES({self.capacity},'{self.status}','{self.no_of_cart}','{self.manufacture}');"
        return table+values
    def update(self) -> str:
        st = f"""
        capacity = {self.capacity},
        status = '{self.status}',
        no_of_carts = '{self.no_of_cart}',
        manufacturer = '{self.manufacture}'
         where train_id = '{self.train_id}'
        """
        return st
    def key(self) ->str:
        return f'train_id = {self.train_id}'
class Trip:
    def __init__(self,row=[None,None,None,None,None,None,None,None]):
        self.table = "Trip"
        self.trip_id = row[0]
        self.train_id= row[1]
        self.price = row[2]
        self.start_date = row[3]
        self.end_date = row[4]
        self.departure_station = row[5]
        self.arrival_station = row[6]
        if(len(row) > 7):
            self.available_seat = row[7]     
        self.seats=[]
        self.ETA = None
        self.train = None
    def add(self) -> str:
        table= 'Trip(train_id,price,start_date,end_date,departure_station,arrival_station) '
        values =f"VALUES('{self.train.train_id}','{self.price}','{self.start_date}','{self.end_date}','{self.departure_station}','{self.arrival_station}');"
        return table+values
    def setTrain(self):
        for i in range(self.train.capacity):
            seat = Seat()
            seat.seat_id = i+1
            seat.trip_id = self.trip_id
            seat.status = "available"
            self.seats.append(seat)
    def update(self) -> str:
        st = f"""
        train_id = '{self.train.train_id}',
        price = '{self.price}',
        start_date = '{self.start_date}',
        end_date = '{self.end_date}',
        departure_station = '{self.departure_station}',
        arrival_station = '{self.arrival_station}'
         where trip_id = '{self.trip_id}'
        """
        return st
    def setDates(self,start , end):
        self.start_date = start
        self.end_date = end
        return end-start
    def key(self) ->str:
        return f'Trip.trip_id = {self.trip_id}'

class Seat:
    def __init__(self,row=[None,None,None]) -> None:
        self.table = "Seat"
        self.seat_id = row[0]
        self.trip_id = row[1]
        self.status = row[2]
    def add(self) ->str:
        values = f"('{self.seat_id}','{self.trip_id}','{self.status}')"
        return values
    def update(self) ->str:
        st = f"""
        status = '{self.status}'
         where seat_id = {self.seat_id} and trip_id = {self.trip_id}
        """
        return st
    def key(self) ->str:
        return f'Seat.seat_id = {self.seat_id}'

class Booking:
    def __init__(self, row = [None,None,None,None]) -> None:
        self.table = "Booking"
        self.booking_id = row[0]
        self.no_of_seats = row[3]
        self.trip = None
        self.account = None
        self.price = None
    def add(self) -> str:
        table= 'Booking(account_id,trip_id,no_of_seats) '
        values =f"VALUES('{self.account.account_id}','{self.trip.trip_id}','{self.no_of_seats}');"
        return table+values
    def set_seats_num(self,num):
        self.no_of_seats = num
        self.price = self.trip.price * self.no_of_seats
    def update(self) -> str:
        st = f"""
        no_of_seats = '{self.no_of_seats}';
        """
        return st
    def key(self) ->str:
        return f'booking_id = {self.booking_id}'