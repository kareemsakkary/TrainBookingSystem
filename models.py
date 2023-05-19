class Account:
    def __init__(self,row=[None,None,None,None,None,None,None,None]):
        self.table = "Users"
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
        values =f'VALUES({self.name},{self.password},admin,{self.email},{self.phone_num},{self.address},{self.date_of_birth})'
        return table+values

class Train:
    def __init__(self,row=[None,None]):
        self.table = "train"
        self.train_id = row[0]
        self.capacity = row[1]
        self.manufacture = row[2]

    def add(self) -> str:
        table= 'Train(capacity)'
        values =f'VALUES({self.capacity})'
        return table+values
    

class Trip:
    def __init__(self,row=[None,None,None,None,None,None,None,None]):
        self.table = "Trip"
        self.trip_id = row[0]
        self.price = row[1]
        self.start_date = row[2]
        self.start_time = row[3]
        self.end_date = row[4]
        self.end_time =row[5]
        self.departure_station = row[6]
        self.arrival_station = row[7]
    def add(self) -> str:
        table= 'Trip(capacity,departure_station,arrival_station,departure_time,arrival_time)'
        values =f'VALUES({self.capacity},{self.departure_station},{self.arrival_station},{self.departure_time},{self.arrival_time})'
        return table+values
    