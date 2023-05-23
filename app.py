# install Pyqt5 & Qt designer by "pip install pyqt5" , "pip install pyqt5-tools"

import sys
import time
import databaseSQL
import models
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime

db = databaseSQL.database()

loggedInUser = models.Account()
selectedTrain = models.Train()
selected = False
selectedTrip = models.Trip()
selectedBooking = models.Booking()
matchingTrips = []

class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("ui/splash.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        pixMap = QPixmap("img/splash.png")
        self.setPixmap(pixMap)
        self.show()
        self.progress()

    def progress(self):
        for i in range(100):
            time.sleep(0.01)
            self.progressBar.setValue(i)


class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("ui/main.ui", self)
        self.login.clicked.connect(self.gotologin)
        self.signup.clicked.connect(self.gotosignup)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotosignup(self):
        signup = SignupScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("ui/Login.ui", self)
        self.inputPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.loginfunction)
        self.returnButton.clicked.connect(self.returnPrevScreen)

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def validateLogin(self):
        email = self.inputEmail.text()
        password = self.inputPassword.text()
        if len(email) == 0 or len(password) == 0:
            self.error.setText("Please input email and password!")
            return False
        else:
            self.error.setText("")
            for row in db.selectAll("Account", f"email ='{email}' and password ='{password}'"):
                loggedInUser.account_id = row.account_id
                loggedInUser.name = row.name
                loggedInUser.email = row.email
                loggedInUser.password = row.password
                loggedInUser.phone_num = row.phone_num
                loggedInUser.address = row.address
                loggedInUser.date_of_birth = row.date_of_birth
                loggedInUser.role = row.role
                return True
            return False

    def loginfunction(self):
        if self.validateLogin():
            self.inputEmail.setText("")
            self.inputPassword.setText("")
            if loggedInUser.role == "admin":
                admin = AdminOptionsScreen()
                widget.addWidget(admin)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif loggedInUser.role == "customer":
                customer = UserOptionsScreen()
                widget.addWidget(customer)
                widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            if self.error.text() == "":
                self.error.setText("Invalid email and password!")


class SignupScreen(QDialog):
    def __init__(self):
        super(SignupScreen, self).__init__()
        loadUi("ui/Signup.ui", self)
        self.inputPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signupButton.clicked.connect(self.signupfunction)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        # restrictions for input fields
        txtRegex = QRegExp("[a-zA-Z]+")
        stringValidator = QRegExpValidator(txtRegex)
        intValidator = QtGui.QIntValidator()
        self.inputName.setValidator(stringValidator)
        self.inputNumber.setValidator(intValidator)

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def showMessageBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success registration!")
        msg.setText("Signed up successfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def uniqueEmail(self, mail):
        unique = True
        if db.count("Account", f"email ='{mail}'") == 1:
            unique = False
        return unique

    def signupfunction(self):
        # reset error msg
        self.error.setText("")
        self.emailError.setText("")

        name = self.inputName.text()
        email = self.inputEmail.text()
        password = self.inputPassword.text()
        phoneNum = self.inputNumber.text()
        dob = self.inputDob.text()
        address = self.inputAddress.text()

        if not self.uniqueEmail(email):
            self.error.setText("")
            self.errorMsg.setText("")
            self.emailError.setText("An account is already registered with your email!")
        elif len(name) == 0 or len(email) == 0 or len(password) == 0 or len(phoneNum) == 0 or len(address) == 0:
            self.error.setText("")
            self.emailError.setText("")
            self.errorMsg.setText("Please input all the required fields!")
        # see which is checked, then add it
        elif self.adminRadioButton.isChecked():
            self.showMessageBox()
            acc = models.Admin()
            acc.name = name
            acc.email = email
            acc.password = password
            acc.phone_num = phoneNum
            acc.date_of_birth = dob
            acc.address = address
            db.addRecord(acc)
            self.returnPrevScreen()
        elif self.customerRadioButton.isChecked():
            self.showMessageBox()
            acc = models.Customer()
            acc.name = name
            acc.email = email
            acc.password = password
            acc.phone_num = phoneNum
            acc.date_of_birth = dob
            acc.address = address
            db.addRecord(acc)
            self.returnPrevScreen()
        else:
            self.errorMsg.setText("")
            self.error.setText("Please choose a role!")


class UpdateUserScreen(QDialog):
    def __init__(self):
        super(UpdateUserScreen, self).__init__()
        loadUi("ui/UpdateUser.ui", self)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.updateUserButton.clicked.connect(self.updateuserfunction)
        self.loadUserInfo()
        # restrictions for input fields
        txtRegex = QRegExp("[a-zA-Z]+")
        stringValidator = QRegExpValidator(txtRegex)
        intValidator = QtGui.QIntValidator()
        self.inputName.setValidator(stringValidator)
        self.inputNumber.setValidator(intValidator)
        self.inputDob.setReadOnly(True)
        self.inputEmail.setReadOnly(True)

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def showMessageBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success changes!")
        msg.setText("Profile updated successfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def loadUserInfo(self):
        # extract the date
        year = int(loggedInUser.date_of_birth[0:4])
        month = int(loggedInUser.date_of_birth[5:7])
        day = int(loggedInUser.date_of_birth[8:10])

        self.inputDob.setDate(QDate(year, month, day))
        self.inputName.setText(loggedInUser.name)
        self.inputEmail.setText(loggedInUser.email)
        self.inputPassword.setText(loggedInUser.password)
        self.inputNumber.setText(loggedInUser.phone_num)
        self.inputAddress.setText(loggedInUser.address)
        if loggedInUser.role == "admin":
            self.adminRadioButton.setChecked(True)
        elif loggedInUser.role == "customer":
            self.customerRadioButton.setChecked(True)

        self.adminRadioButton.setEnabled(False)
        self.customerRadioButton.setEnabled(False)

    def updateuserfunction(self):
        self.showMessageBox()
        acc = models.Account()
        acc.account_id = loggedInUser.account_id
        acc.name = self.inputName.text()
        acc.email = self.inputEmail.text()
        acc.password = self.inputPassword.text()
        acc.phone_num = self.inputNumber.text()
        acc.date_of_birth = loggedInUser.date_of_birth
        acc.address = self.inputAddress.text()
        db.update(acc)
        # update the current info of logged in user if updated
        loggedInUser.name = acc.name
        loggedInUser.email = acc.email
        loggedInUser.password = acc.password
        loggedInUser.phone_num = acc.phone_num
        loggedInUser.address = acc.address
        self.returnPrevScreen()


class AddTrainScreen(QDialog):
    def __init__(self):
        super(AddTrainScreen, self).__init__()
        loadUi("ui/AddTrain.ui", self)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.addTrainButton.clicked.connect(self.addtrainfunction)

        intValidator = QtGui.QIntValidator()
        txtRegex = QRegExp("[a-zA-Z]+")
        stringValidator = QRegExpValidator(txtRegex)
        self.inputCapacity.setValidator(intValidator)
        self.inputNumofcart.setValidator(intValidator)
        self.inputManufacturer.setValidator(stringValidator)

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def showMessageBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success addition!")
        msg.setText("Train added successfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def addtrainfunction(self):
        cap = self.inputCapacity.text()
        numOfCart = self.inputNumofcart.text()
        manufacture = self.inputManufacturer.text()
        if len(cap) == 0 or len(numOfCart) == 0 or len(
                manufacture) == 0 or (
                not self.activeRadioButton.isChecked() and not self.inactiveRadioButton.isChecked()):
            self.error.setText("Please input all the required fields!")
        else:
            self.showMessageBox()
            train = models.Train()
            train.capacity = int(cap)
            train.no_of_cart = int(numOfCart)
            train.manufacture = manufacture
            if self.activeRadioButton.isChecked():
                train.status = "active"
            elif self.inactiveRadioButton.isChecked():
                train.status = "inactive"
            db.addRecord(train)
            self.returnPrevScreen()


class ShowAllTrains(QDialog):
    def __init__(self):
        super(ShowAllTrains, self).__init__()
        loadUi("ui/ShowTrains.ui", self)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 200)
        self.tableWidget.setHorizontalHeaderLabels(["Train ID", "Capacity", "Status", "Number of cart", "Manufacturer"])
        self.tableWidget.horizontalHeader().setFixedHeight(20)
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.loadTrains()
        self.selectTrainButton.clicked.connect(self.gotoupdatetrain)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.tableWidget.cellClicked.connect(self.getClickedCell)

    def clearSelected(self):
        global selected
        selected = False
        # reset the selected train data to none
        selectedTrain.train_id = ""
        selectedTrain.status = ""
        selectedTrain.capacity = ""
        selectedTrain.manufacture = ""
        selectedTrain.no_of_cart = ""

    def getClickedCell(self, row):
        global selected
        selected = True
        # move the clicked row data to update train screen
        selectedTrain.train_id = self.tableWidget.item(row, 0).text()
        selectedTrain.capacity = self.tableWidget.item(row, 1).text()
        selectedTrain.status = self.tableWidget.item(row, 2).text()
        selectedTrain.no_of_cart = self.tableWidget.item(row, 3).text()
        selectedTrain.manufacture = self.tableWidget.item(row, 4).text()

    def returnPrevScreen(self):
        self.clearSelected()
        widget.removeWidget(self)

    def loadTrains(self):
        self.tableWidget.setRowCount(db.count("Train"))
        tableRow = 0
        for row in db.selectAll("Train"):
            self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row.train_id)))
            self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(str(row.capacity)))
            self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(row.status))
            self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(row.no_of_cart)))
            self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(row.manufacture))
            tableRow += 1

    def gotoupdatetrain(self):
        if selected:
            self.error.setText("")
            updateTrain = UpdateTrainScreen()
            widget.addWidget(updateTrain)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            self.error.setText("Please select a train to update!")


class UpdateTrainScreen(QDialog):
    def __init__(self):
        super(UpdateTrainScreen, self).__init__()
        loadUi("ui/UpdateTrain.ui", self)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.updateTrainButton.clicked.connect(self.updatetrainfunction)
        self.loadTrainInfo()
        intValidator = QtGui.QIntValidator()
        txtRegex = QRegExp("[a-zA-Z]+")
        stringValidator = QRegExpValidator(txtRegex)
        self.inputCapacity.setValidator(intValidator)
        self.inputNumofcart.setValidator(intValidator)
        self.inputManufacturer.setValidator(stringValidator)

    def showMessageBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success changes!")
        msg.setText("Train updated successfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def clearSelected(self):
        global selected
        selected = False
        # reset the selected train data to none
        selectedTrain.train_id = ""
        selectedTrain.status = ""
        selectedTrain.capacity = ""
        selectedTrain.manufacture = ""
        selectedTrain.no_of_cart = ""

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def loadTrainInfo(self):
        self.inputCapacity.setText(selectedTrain.capacity)
        self.inputNumofcart.setText(selectedTrain.no_of_cart)
        self.inputManufacturer.setText(selectedTrain.manufacture)
        if selectedTrain.status == "active":
            self.activeRadioButton.setChecked(True)
        elif selectedTrain.status == "inactive":
            self.inactiveRadioButton.setChecked(True)

    def updatetrainfunction(self):
        cap = self.inputCapacity.text()
        numOfCart = self.inputNumofcart.text()
        manufacture = self.inputManufacturer.text()
        if len(cap) == 0 or len(numOfCart) == 0 or len(
                manufacture) == 0 or (
                not self.activeRadioButton.isChecked() and not self.inactiveRadioButton.isChecked()):
            self.error.setText("Cannot update without the required fields!")
        else:
            self.showMessageBox()
            selectedTrain.capacity = cap
            selectedTrain.no_of_cart = numOfCart
            selectedTrain.manufacture = manufacture
            if self.activeRadioButton.isChecked():
                selectedTrain.status = "active"
            elif self.inactiveRadioButton.isChecked():
                selectedTrain.status = "inactive"
            # update the selected train data
            db.update(selectedTrain)
            self.returnPrevScreen()
            self.clearSelected()
            widget.removeWidget(widget.currentWidget())


class AddTripScreen(QDialog):
    def __init__(self):
        super(AddTripScreen, self).__init__()
        # load UI
        loadUi("ui/AddTrip.ui", self)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.addTripButton.clicked.connect(self.addtripfunction)
        self.inputStartDate.setMinimumDateTime(QtCore.QDateTime.currentDateTime())
        self.inputEndDate.setMinimumDateTime(QtCore.QDateTime.currentDateTime())
        self.inputStartDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.inputEndDate.setDateTime(QtCore.QDateTime.currentDateTime())

        intValidator = QtGui.QIntValidator()
        floatValidator = QtGui.QDoubleValidator()
        txtRegex = QRegExp("[a-zA-Z]+")
        stringValidator = QRegExpValidator(txtRegex)
        self.inputPrice.setValidator(floatValidator)
        self.inputDepartureStation.setValidator(stringValidator)
        self.inputArrivalStation.setValidator(stringValidator)
        self.inputTrainID.setValidator(intValidator)
    def showMessageBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success changes!")
        msg.setText("Trip added successfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
    def returnPrevScreen(self):
        widget.removeWidget(self)
    def addtripfunction(self):
        price = self.inputPrice.text()
        departure = self.inputDepartureStation.text()
        arrival = self.inputArrivalStation.text()
        trainID =self.inputTrainID.text()
        startdate = self.inputStartDate.dateTime().toPyDateTime().replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
        enddate = self.inputEndDate.dateTime().toPyDateTime().replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
        if len(str(price)) == 0 or len(departure) == 0 or len(arrival) == 0 or len(trainID) == 0:
            self.error.setText("Cannot add without the required fields!")
        elif not db.count("Train", f"train_id ='{trainID}'") == 1:
            self.error.setText("Train ID doesn't exist!")
        elif startdate >= enddate:
            self.error.setText("Start date must be before end date!")
        else:
            train = db.selectAll("Train" , f"train_id = '{int(trainID)}'")[0]
            trip = models.Trip()
            trip.train = train
            trip.price = float(price)
            trip.departure_station = departure
            trip.arrival_station = arrival
            trip.start_date = startdate
            trip.end_date = enddate
            db.addRecord(trip)
            self.showMessageBox()
            widget.removeWidget(widget.currentWidget())


class UpdateTripScreen(QDialog):
    def __init__(self):
        super(UpdateTripScreen, self).__init__()
        loadUi("ui/UpdateTrip.ui", self)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.updateTripButton.clicked.connect(self.updatetripfunction)
        self.inputStartDate.setMinimumDateTime(datetime.now())
        self.inputEndDate.setMinimumDateTime(datetime.now())
        self.loadTripInfo()
        intValidator = QtGui.QIntValidator()
        floatValidator = QtGui.QDoubleValidator()
        txtRegex = QRegExp("[a-zA-Z]+")
        stringValidator = QRegExpValidator(txtRegex)
        self.inputPrice.setValidator(floatValidator)
        self.inputDepartureStation.setValidator(stringValidator)
        self.inputArrivalStation.setValidator(stringValidator)
        self.inputTrainID.setValidator(intValidator)

    def showMessageBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success changes!")
        msg.setText("Trip updated successfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def loadTripInfo(self):
        self.inputPrice.setText(str(selectedTrip.price))
        self.inputDepartureStation.setText(selectedTrip.departure_station)
        self.inputArrivalStation.setText(selectedTrip.arrival_station)
        self.inputTrainID.setText(str(selectedTrip.train.train_id))
        startDate = datetime.strptime(selectedTrip.start_date, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0)
        endDate = datetime.strptime(selectedTrip.end_date, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0)
        self.inputStartDate.setDateTime(startDate)
        self.inputEndDate.setDateTime(endDate)

    def updatetripfunction(self):
        price = self.inputPrice.text()
        departure = self.inputDepartureStation.text()
        arrival = self.inputArrivalStation.text()
        trainID = self.inputTrainID.text()
        startdate = self.inputStartDate.dateTime().toPyDateTime().replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
        enddate = self.inputEndDate.dateTime().toPyDateTime().replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
        if len(str(price)) == 0 or len(departure) == 0 or len(arrival) == 0 or len(trainID) == 0:
            self.error.setText("Cannot add without the required fields!")
        elif startdate >= enddate:
            self.error.setText("Start date must be before end date!")
        else:
            selectedTrip.price = price
            selectedTrip.departure_station = departure
            selectedTrip.arrival_station = arrival
            selectedTrip.train = db.selectAll("Train", f"train_id = '{int(trainID)}'")[0]
            selectedTrip.start_date = startdate
            selectedTrip.end_date = enddate
            db.update(selectedTrip)
            self.showMessageBox()
            self.returnPrevScreen()
            widget.removeWidget(widget.currentWidget())


class ShowAllTrips(QDialog):
    def __init__(self):
        super(ShowAllTrips, self).__init__()
        # load UI
        loadUi("ui/ShowTrips.ui", self)
        #make coulmn width fit the content
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setHorizontalHeaderLabels(["Trip Id","Departure Station", "Arrival Station", "Price", "Start Date", "End Date", "Train ID"])
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.loadTrips()
        self.tableWidget.horizontalHeader().setFixedHeight(20)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.tableWidget.doubleClicked.connect(self.getClickedCell)
        if loggedInUser.role == "admin":
            self.instructionLabel.setText("Please double click on the trip to update it :)")
        elif loggedInUser.role == "customer":
            self.instructionLabel.setText("Please double click on the trip to book it :)")

    def getClickedCell(self, index):
        row = index.row()
        column = index.column()

        if column >= 0:
            selectedTrip.trip_id = self.tableWidget.item(row, 0).text()
            selectedTrip.departure_station = self.tableWidget.item(row, 1).text()
            selectedTrip.arrival_station = self.tableWidget.item(row, 2).text()
            selectedTrip.price = float(self.tableWidget.item(row, 3).text())
            selectedTrip.start_date = self.tableWidget.item(row, 4).text()
            selectedTrip.end_date = self.tableWidget.item(row, 5).text()
            trainid = int(self.tableWidget.item(row, 6).text())
            selectedTrip.train = db.selectAll("Train", f"train_id = '{trainid}'")[0]
            self.action()

    def clearSelected(self):
        # reset the selected train data to none
        selectedTrip.departure_station = ""
        selectedTrip.arrival_station = ""
        selectedTrip.price = ""
        selectedTrip.start_date = ""
        selectedTrip.end_date = ""
        selectedTrip.train = None
    def returnPrevScreen(self):
        self.clearSelected()
        widget.removeWidget(self)

    def loadTrips(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.tableWidget.setRowCount(db.count("Trip",f"start_date >= '{current_datetime}'"))
        tableRow = 0
        for row in db.selectAll("Trip", f"start_date >= '{current_datetime}'"):
            self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row.trip_id)))
            self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(row.departure_station))
            self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(row.arrival_station))
            self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(row.price)))
            self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(str(row.start_date)))
            self.tableWidget.setItem(tableRow, 5, QtWidgets.QTableWidgetItem(str(row.end_date)))
            self.tableWidget.setItem(tableRow, 6, QtWidgets.QTableWidgetItem(str(row.train.train_id)))
            tableRow += 1

    def action(self):
        if loggedInUser.role == "admin":
            widget.addWidget(UpdateTripScreen())
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            widget.addWidget(BookTripScreen())
            widget.setCurrentIndex(widget.currentIndex() + 1)


class BookTripScreen(QDialog):
    def __init__(self):
        super(BookTripScreen, self).__init__()
        loadUi("ui/BookTrip.ui", self)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.bookTripButton.clicked.connect(self.booktripfunction)
        self.loadTripInfo()
        self.seatCountInput.textChanged.connect(self.updateTotalPrice)

    def clearSelected(self):
        # reset the selected train data to none
        selectedTrip.trip_id = ""
        selectedTrip.departure_station = ""
        selectedTrip.arrival_station = ""
        selectedTrip.price = ""
        selectedTrip.start_date = ""
        selectedTrip.end_date = ""
        matchingTrips.clear()
    def returnPrevScreen(self):
        self.clearSelected()
        widget.removeWidget(self)

    def gotoallbookings(self):
        allBooking = ShowBookings()
        widget.addWidget(allBooking)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loadTripInfo(self):
        self.departureStationLabel.setText(selectedTrip.departure_station)
        self.arrivalStationLabel.setText(selectedTrip.arrival_station)
        self.startDateLabel.setText(selectedTrip.start_date)
        self.endDateLabel.setText(selectedTrip.end_date)
        self.totalPriceLabel.setText(str(selectedTrip.price))

    def updateTotalPrice(self):
        numofseats = self.seatCountInput.text()
        if len(numofseats) == 0:
            self.totalPriceLabel.setText("0")
        else:
            self.totalPriceLabel.setText(str(int(numofseats) * int(selectedTrip.price)))
    def showMessageBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success Booking!")
        msg.setText("Successfully booked the trip!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
    def booktripfunction(self):
        numofseats = self.seatCountInput.text()

        if int(numofseats) > db.count("Seat",f"status = 'available' and trip_id = '{selectedTrip.trip_id}';"):
            self.error.setText("Not enough seats!")
        elif db.selectAll("Booking", f"account.account_id = '{loggedInUser.account_id}' and trip.trip_id = '{selectedTrip.trip_id}'"):
            booking = db.selectAll("Booking", f"account.account_id = '{loggedInUser.account_id}' and trip.trip_id = '{selectedTrip.trip_id}'")[0]
            booking.set_seats_num(booking.no_of_seats + int(numofseats))
            db.update(booking)
            self.showMessageBox()
            self.clearSelected()
            self.returnPrevScreen()
            self.clearSelected()
            widget.removeWidget(widget.currentWidget())
            self.gotoallbookings()
        else:
            book = models.Booking()
            book.trip = selectedTrip
            book.account = loggedInUser
            book.set_seats_num(int(numofseats))
            db.addRecord(book)
            self.showMessageBox()
            self.clearSelected()
            self.returnPrevScreen()
            widget.removeWidget(widget.currentWidget())
            self.gotoallbookings()


class ShowBookings(QDialog):
    def __init__(self):
        super(ShowBookings, self).__init__()
        # load UI
        loadUi("ui/ShowBookings.ui", self)
        #make coulmn width fit the content
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setHorizontalHeaderLabels(["Booking ID", "Departure Station", "Arrival Station", "Departure Date", "Arrival Date","Seat Count" , "Price","Train ID", "Trip ID"])
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.horizontalHeader().setFixedHeight(20)
        self.loadBookings()
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.tableWidget.doubleClicked.connect(self.getClickedCell)
        self.instructionLabel.setText("Please double click on the trip to cancel it :(")

    def returnPrevScreen(self):
        widget.removeWidget(self)
    def loadBookings(self):
        self.tableWidget.setRowCount(db.count("Booking",f"account.account_id = '{loggedInUser.account_id}'"))
        tableRow = 0
        for row in db.selectAll("Booking",f"account.account_id = '{loggedInUser.account_id}'"):
            self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row.booking_id)))
            self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(row.trip.departure_station))
            self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(row.trip.arrival_station))
            self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(row.trip.start_date)))
            self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(str(row.trip.end_date)))
            self.tableWidget.setItem(tableRow, 5, QtWidgets.QTableWidgetItem(str(row.no_of_seats)))
            self.tableWidget.setItem(tableRow, 6, QtWidgets.QTableWidgetItem(str(row.price)))
            self.tableWidget.setItem(tableRow, 7, QtWidgets.QTableWidgetItem(str(row.trip.train.train_id)))
            self.tableWidget.setItem(tableRow, 8, QtWidgets.QTableWidgetItem(str(row.trip.trip_id)))
            tableRow += 1

    def getClickedCell(self):
        selectedRow = self.tableWidget.currentRow()
        selectedBooking.booking_id = self.tableWidget.item(selectedRow, 0).text()
        selectedTrip.trip_id = self.tableWidget.item(selectedRow, 8).text()
        selectedTrip.departure_station = self.tableWidget.item(selectedRow, 1).text()
        selectedTrip.arrival_station = self.tableWidget.item(selectedRow, 2).text()
        selectedTrip.start_date = self.tableWidget.item(selectedRow, 3).text()
        selectedTrip.end_date = self.tableWidget.item(selectedRow, 4).text()
        selectedBooking.no_of_seats = self.tableWidget.item(selectedRow, 5).text()
        selectedBooking.price = self.tableWidget.item(selectedRow, 6).text()
        selectedTrip.train_id = self.tableWidget.item(selectedRow, 7).text()
        selectedTrip.price = db.selectAll("Trip",f"Trip.trip_id = '{selectedTrip.trip_id}'")[0].price
        self.gotocanceltrip()
    def gotocanceltrip(self):
        if datetime.strptime(selectedTrip.start_date, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0) < datetime.now().replace(second=0, microsecond=0):
            self.error.setText("You can't cancel a trip that already started!")
        else:
            widget.removeWidget(self)
            widget.addWidget(CancelTripScreen())
            widget.setCurrentIndex(widget.currentIndex() + 1)


class CancelTripScreen(QDialog):
    def __init__(self):
        super(CancelTripScreen, self).__init__()
        loadUi("ui/CancelBooking.ui", self)
        self.cancelButton.clicked.connect(self.cancelBooking)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.loadBookingInfo()
    def returnPrevScreen(self):
        widget.removeWidget(self)
    def loadBookingInfo(self):
        self.departureStationLabel.setText(selectedTrip.departure_station)
        self.arrivalStationLabel.setText(selectedTrip.arrival_station)
        self.startDateLabel.setText(str(selectedTrip.start_date))
        self.endDateLabel.setText(str(selectedTrip.end_date))
        self.seatsCountLabel.setText(str(selectedBooking.no_of_seats))
        self.totalPriceLabel.setText(str(selectedBooking.price))
        self.inputSeatsCount.setMaximum(int(selectedBooking.no_of_seats))
    def cancelBooking(self):
        seatsToCancel = int(self.inputSeatsCount.text())
        if seatsToCancel > int(selectedBooking.no_of_seats):
            self.error.setText("Not enough seats!")
        elif seatsToCancel == int(selectedBooking.no_of_seats):
            db.deleteRecord(selectedBooking)
            self.MsgBox()
            self.returnPrevScreen()

        else:
            selectedBooking.account = loggedInUser
            selectedBooking.trip = selectedTrip
            selectedBooking.no_of_seats = int(selectedBooking.no_of_seats) - seatsToCancel
            selectedBooking.price = float(selectedBooking.price) - (seatsToCancel * int(selectedBooking.trip.price))
            db.update(selectedBooking)
            self.MsgBox()
            self.returnPrevScreen()
    def MsgBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success cancellation!")
        msg.setText("Booking canceled successfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()


class ShowMatchingTripsScreen(QDialog):
    def __init__(self):
        super(ShowMatchingTripsScreen, self).__init__()
        # load UI
        loadUi("ui/ShowTrips.ui", self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Trip Id", "Departure Station", "Arrival Station", "Price", "Start Date", "End Date", "Train ID"])
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.loadTrips()
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.tableWidget.doubleClicked.connect(self.getClickedCell)
        self.instructionLabel.setText("Please double click on the trip to book it :)")

    def getClickedCell(self, index):
        row = index.row()
        column = index.column()
        if column >= 0:
            selectedTrip.trip_id = self.tableWidget.item(row, 0).text()
            selectedTrip.departure_station = self.tableWidget.item(row, 1).text()
            selectedTrip.arrival_station = self.tableWidget.item(row, 2).text()
            selectedTrip.price = float(self.tableWidget.item(row, 3).text())
            selectedTrip.start_date = self.tableWidget.item(row, 4).text()
            selectedTrip.end_date = self.tableWidget.item(row, 5).text()
            trainid = int(self.tableWidget.item(row, 6).text())
            selectedTrip.train = db.selectAll("Train", f"train_id = '{trainid}'")[0]
            self.action()

    def clearSelected(self):
        # reset the selected train data to none
        selectedTrip.departure_station = ""
        selectedTrip.arrival_station = ""
        selectedTrip.price = ""
        selectedTrip.start_date = ""
        selectedTrip.end_date = ""
        selectedTrip.train = None
        matchingTrips.clear()

    def returnPrevScreen(self):
        self.clearSelected()
        widget.removeWidget(self)

    def loadTrips(self):
        self.tableWidget.setRowCount(len(matchingTrips))
        tableRow = 0
        for row in matchingTrips:
            self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row.trip_id)))
            self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(row.departure_station))
            self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(row.arrival_station))
            self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(row.price)))
            self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(str(row.start_date)))
            self.tableWidget.setItem(tableRow, 5, QtWidgets.QTableWidgetItem(str(row.end_date)))
            self.tableWidget.setItem(tableRow, 6, QtWidgets.QTableWidgetItem(str(row.train.train_id)))
            tableRow += 1

    def action(self):
        if loggedInUser.role == "admin":
            widget.addWidget(UpdateTripScreen())
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            widget.addWidget(BookTripScreen())
            widget.setCurrentIndex(widget.currentIndex() + 1)


class FindTripScreen(QDialog):
    def __init__(self):
        super(FindTripScreen, self).__init__()
        # load UI
        loadUi("ui/FindTrip.ui", self)
        txtRegex = QRegExp("[a-zA-Z]+")
        stringValidator = QRegExpValidator(txtRegex)
        self.inputDepartureStation.setValidator(stringValidator)
        self.inputArrivalStation.setValidator(stringValidator)
        self.inputStartDate.setMinimumDateTime(datetime.now())
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.findTripButton.clicked.connect(self.findTrip)

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def showMessageBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Not found!")
        msg.setText("No available seats found that satisfy these criteria!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def findTrip(self):
        departure_station = self.inputDepartureStation.text()
        arrival_station = self.inputArrivalStation.text()
        start_date = self.inputStartDate.dateTime().toPyDateTime().replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
        no_of_seats = int(self.inputSeatsCount.text())
        if len(str(no_of_seats)) == 0 or len(departure_station) == 0 or len(arrival_station) == 0:
            self.error.setText("Cannot search without the required fields!")
        else:
            matchingTrips.extend(db.getTrips(no_of_seats, arrival_station, departure_station, start_date))
            if (len(matchingTrips)) == 0:
                self.showMessageBox()
            else:
                widget.addWidget(ShowMatchingTripsScreen())
                widget.setCurrentIndex(widget.currentIndex() + 1)
class ShowReportScreen(QDialog):
    def __init__(self):
        super(ShowReportScreen, self).__init__()
        loadUi("ui/Report.ui", self)
        self.loadInfo()
        self.tableWidget.setTextAlignment(4)
        self.tableWidget.horizontalHeader().setFixedHeight(40)
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.returnButton.clicked.connect(self.returnPrevScreen)

    def returnPrevScreen(self):
        self.clearSelected()
        widget.removeWidget(self)

    def loadInfo(self):
        self.tableWidget.setRowCount(len(db.reportTrips()))
        tableRow = 0
        self.accountsNum.setText(str(db.count("Account")))
        self.tripsNum.setText(str(db.count("Trip")))
        self.trainsNum.setText(str(db.count("Train")))
        self.bookingsNum.setText(str(db.count("Booking")))
        for row in db.reportTrips():
            item =QtWidgets.QTableWidgetItem(str(row[0]))
            item.setTextAlignment(4)
            self.tableWidget.setItem(tableRow, 0, item)

            item =QtWidgets.QTableWidgetItem(str(row[1]))
            item.setTextAlignment(4)
            self.tableWidget.setItem(tableRow, 1, item)

            item =QtWidgets.QTableWidgetItem(str(row[2]))
            item.setTextAlignment(4)
            self.tableWidget.setItem(tableRow, 2, item)

            item =QtWidgets.QTableWidgetItem(str(row[4]))
            item.setTextAlignment(4)
            self.tableWidget.setItem(tableRow, 3, item)

            item =QtWidgets.QTableWidgetItem(str(row[3]))
            item.setTextAlignment(4)
            self.tableWidget.setItem(tableRow, 4, item)
            tableRow += 1

class AdminOptionsScreen(QDialog):
    def __init__(self):
        super(AdminOptionsScreen, self).__init__()
        loadUi("ui/adminOptions.ui", self)
        self.addTrainButton.clicked.connect(self.gotoaddtrain)
        self.updateTrainButton.clicked.connect(self.gotoshowtrains)
        self.addTripButton.clicked.connect(self.gotoaddtrip)
        self.updateTripButton.clicked.connect(self.gotoshowtrips)
        self.showReportButton.clicked.connect(self.gotoshowreport)
        self.returnButton.clicked.connect(self.returnPrevScreen)

    def returnPrevScreen(self):
        widget.removeWidget(self)
    def gotoshowreport(self):
        showReport = ShowReportScreen()
        widget.addWidget(showReport)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoaddtrain(self):
        addTrain = AddTrainScreen()
        widget.addWidget(addTrain)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoaddtrip(self):
        addTrip = AddTripScreen()
        widget.addWidget(addTrip)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoshowtrips(self):
        showTrips = ShowAllTrips()
        widget.addWidget(showTrips)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoshowtrains(self):
        showTrains = ShowAllTrains()
        widget.addWidget(showTrains)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class UserOptionsScreen(QDialog):
    def __init__(self):
        super(UserOptionsScreen, self).__init__()
        loadUi("ui/userOptions.ui", self)
        self.updateInfoButton.clicked.connect(self.gotoupdateInfo)
        self.bookButton.clicked.connect(self.gotobooktrip)
        self.tripsButton.clicked.connect(self.gototrips)
        self.findTripButton.clicked.connect(self.gotofindtrip)
        self.returnButton.clicked.connect(self.returnPrevScreen)

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def gototrips(self):
        cancelTrip = ShowBookings()
        widget.addWidget(cancelTrip)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotobooktrip(self):
        bookTrip = ShowAllTrips()
        widget.addWidget(bookTrip)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoupdateInfo(self):
        updateInfo = UpdateUserScreen()
        widget.addWidget(updateInfo)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotofindtrip(self):
        findTrip = FindTripScreen()
        widget.addWidget(findTrip)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Ticket Trackr")
    app.setWindowIcon(QIcon("img/icon.png"))
    # splash screen
    splash = SplashScreen()
    # main window
    main = MainScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main)
    widget.setFixedWidth(800)
    widget.setFixedHeight(840)
    widget.show()
    splash.finish(widget)
    # run app
    app.exec_()