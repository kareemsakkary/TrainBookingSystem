# install Pyqt5 & Qt designer by "pip install pyqt5" , "pip install pyqt5-tools"

import sys
import time
import databaseSQL
import models
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRegExp, QDate, QDateTime
from PyQt5.QtGui import *
from datetime import datetime

db = databaseSQL.database()

loggedInUser = models.Account()
selectedTrain = models.Train()
selected = False
selectedTrip = models.Trip()

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


# -------------------------------------------------------
# Shahd - Screens
class AddTripScreen(QDialog):
    def __init__(self):
        super(AddTripScreen, self).__init__()
        # load UI
        loadUi("ui/AddTrip.ui", self)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.addTripButton.clicked.connect(self.addtripfunction)

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
        trainID = self.inputTrainID.text()
        startdate = self.inputStartDate.dateTime().toPyDateTime()
        enddate = self.inputEndDate.dateTime().toPyDateTime()
        train = db.selectAll("Train" , f"train_id = '{trainID}'")[0]

        if len(price) == 0 or len(departure) == 0 or len(arrival) == 0 or len(trainID) == 0:
            self.error.setText("")
            self.errorMsg.setText("")
            self.errorMsg.setText("Cannot add without the required fields!")
        #check train id exist
        elif train is None:
            self.error.setText("")
            self.errorMsg.setText("")
            self.errorMsg.setText("Train ID doesn't exist!")
        elif startdate >= enddate:
            self.error.setText("")
            self.errorMsg.setText("")
            self.errorMsg.setText("Start date must be before end date!")
        else:
            trip = models.Trip()
            trip.train = train
            trip.price = price
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
        # load UI

class ShowAllTrips(QDialog):
    def __init__(self):
        super(ShowAllTrips, self).__init__()
        # load UI
        loadUi("ui/ShowTrips.ui", self)
        #make coulmn width fit the content
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setHorizontalHeaderLabels(["Trip Id","Departure Station", "Arrival Station", "Price", "StartDate", "End Date"])
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.loadTrips()
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.tableWidget.doubleClicked.connect(self.getClickedCell)

    def getClickedCell(self, index):
        row = index.row()
        column = index.column()

        if column >= 0:
            selectedTrip.trip_id = self.tableWidget.item(row, 0).text()
            selectedTrip.departure_station = self.tableWidget.item(row, 1).text()
            selectedTrip.arrival_station = self.tableWidget.item(row, 2).text()
            # print(self.tableWidget.item(row, 3).text())
            selectedTrip.price = float(self.tableWidget.item(row, 3).text())
            selectedTrip.start_date = self.tableWidget.item(row, 4).text()
            selectedTrip.end_date = self.tableWidget.item(row, 5).text()
            self.gotobooktrip()

    def clearSelected(self):
        # reset the selected train data to none
        selectedTrip.departure_station = ""
        selectedTrip.arrival_station = ""
        selectedTrip.price = ""
        selectedTrip.start_date = ""
        selectedTrip.end_date = ""
    def returnPrevScreen(self):
        self.clearSelected()
        widget.removeWidget(self)

    def loadTrips(self):
        self.tableWidget.setRowCount(db.count("Trip"))
        tableRow = 0
        for row in db.selectAll("Trip"):
            self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row.trip_id)))
            self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(row.departure_station))
            self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(row.arrival_station))
            self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(row.price)))
            self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(str(row.start_date)))
            self.tableWidget.setItem(tableRow, 5, QtWidgets.QTableWidgetItem(str(row.end_date)))
            tableRow += 1

    def gotobooktrip(self):
        #check if the user selected a trip
        if selectedTrip.departure_station == "" or selectedTrip.arrival_station == "" or selectedTrip.price == "" or selectedTrip.start_date == "" or selectedTrip.end_date == "":
            self.error.setText("Please select a trip!")
        else:
            widget.removeWidget(self)
            widget.addWidget(BookTripScreen())
            widget.setCurrentIndex(widget.currentIndex() + 1)
            self.clearSelected()

class BookTripScreen(QDialog):
    def __init__(self):
        super(BookTripScreen, self).__init__()
        loadUi("ui/BookTrip.ui", self)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.bookTripButton.clicked.connect(self.booktripfunction)
        self.loadTripInfo()
        intValidator = QtGui.QIntValidator()
        txtRegex = QRegExp("[a-zA-Z]+")
        stringValidator = QRegExpValidator(txtRegex)

    def clearSelected(self):
        # reset the selected train data to none
        selectedTrip.departure_station = ""
        selectedTrip.arrival_station = ""
        selectedTrip.price = ""
        selectedTrip.start_date = ""
        selectedTrip.end_date = ""
    def returnPrevScreen(self):
        self.clearSelected()
        widget.removeWidget(self)
    def loadTripInfo(self):
        self.departureStationLabel.setText(selectedTrip.departure_station)
        self.arrivalStationLabel.setText(selectedTrip.arrival_station)
        self.startDateLabel.setText(selectedTrip.start_date)
        self.endDateLabel.setText(selectedTrip.end_date)
        self.totalPriceLabel.setText(str(selectedTrip.price))
    #     self.seatCountInput.textChanged.connect(self.updateTotalPrice)
    # def updateTotalPrice(self):
    #     numofseats = self.seatCountInput.text()
    #     if len(numofseats) == 0:
    #         self.totalPriceLabel.setText("0")
    #     else:
    #         self.totalPriceLabel.setText(str(int(numofseats) * int(selectedTrip.price)))
    def showMessageBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success Booking!")
        msg.setText("Successfully booked the trip!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
    def booktripfunction(self):
        numofseats = self.seatCountInput.text()
        # if int(numofseats) > db.count("Seat",f"status = 'available' and trip_id = '{selectedTrip.trip_id}';"):
        #     self.error.setText("")
        #     self.errorMsg.setText("")
        #     self.errorMsg.setText("Not enough seats!")
        # else:
        book = models.Booking()
        book.trip = selectedTrip
        book.account = loggedInUser
        book.set_seats_num(int(numofseats))
        db.addRecord(book)
        self.showMessageBox()
        self.returnPrevScreen()
        self.clearSelected()

class CancelTripScreen(QDialog):
    def __init__(self):
        super(CancelTripScreen, self).__init__()
        # load UI

class ShowMatchingTripsScreen(QDialog):
    def __init__(self):
        super(ShowMatchingTripsScreen, self).__init__()
        # load UI
        loadUi("ui/ShowTrips.ui", self)
        model = QStandardItemModel(0, 5)
        model.setHorizontalHeaderLabels(
            ["Departure Station", "Arrival Station", "Price", "Start Date", "End Date"])
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.loadTrips()
        self.selectTripButton.clicked.connect(self.gotobooktrip)
        self.tableWidget.cellClicked.connect(self.getClickedCell)

    def clearSelected(self):
        # reset the selected trip data to none
        selectedTrip.departure_station = ""
        selectedTrip.arrival_station = ""
        selectedTrip.price = ""
        selectedTrip.start_date = ""
        selectedTrip.end_date = ""

    def returnPrevScreen(self):
        self.clearSelected()
        widget.removeWidget(self)

    def loadTrips(self, departure_station, arrival_station, departure_date, seats_count):
        model = QStandardItemModel(0, 5)
        model.setHorizontalHeaderLabels(
            ["Departure Station", "Arrival Station", "Price", "Start Date", "End Date"])
        for i in db.selectAll("Trip",where="departure_station = ? AND arrival_station = ? AND start_date = ? AND capacity >= ?",where_values=[departure_station,arrival_station,departure_date,seats_count]):
            departure_station = QStandardItem(str(i.departure_station))
            arrival_station = QStandardItem(str(i.arrival_station))
            price = QStandardItem(str(i.price))
            start_date = QStandardItem(str(i.start_date))
            end_date = QStandardItem(str(i.end_date))

            model.appendRow([departure_station, arrival_station, price, start_date, end_date])

    def getClickedCell(self, row, column):
        # Retrieve the data from the clicked cell
        trip_id = self.tableWidget.item(row, 0).text()
        departure_station = self.tableWidget.item(row, 1).text()
        arrival_station = self.tableWidget.item(row, 2).text()
        price = self.tableWidget.item(row, 3).text()
        start_date = self.tableWidget.item(row, 4).text()
        end_date = self.tableWidget.item(row, 5).text()

        # Set the selected trip data
        selectedTrip.departure_station = departure_station
        selectedTrip.arrival_station = arrival_station
        selectedTrip.price = price
        selectedTrip.start_date = start_date
        selectedTrip.end_date = end_date

    def gotobooktrip(self):
        # Check if a trip is selected
        if (
            selectedTrip.departure_station
            and selectedTrip.arrival_station
            and selectedTrip.price
            and selectedTrip.start_date
            and selectedTrip.end_date
        ):
            # Open the BookSeatsScreen and pass the selected trip data
            book_seats_screen = BookTripScreen()
            book_seats_screen.departure_station_label.setText(selectedTrip.departure_station)
            book_seats_screen.arrival_station_label.setText(selectedTrip.arrival_station)
            book_seats_screen.price_label.setText(selectedTrip.price)
            book_seats_screen.start_date_label.setText(selectedTrip.start_date)
            book_seats_screen.end_date_label.setText(selectedTrip.end_date)
            widget.addWidget(book_seats_screen)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            QMessageBox.warning(self, "Warning", "Please select a trip.")

class FindTripScreen(QDialog):
    def __init__(self):
        super(FindTripScreen, self).__init__()
        # load UI
        loadUi("ui/FindTrip.ui", self)
        self.returnButton.clicked.connect(self.returnPrevScreen)
        self.findTripButton.clicked.connect(self.findtripfunction)
        self.loadTripInfo()
        intValidator = QtGui.QIntValidator()
        txtRegex = QRegExp("[a-zA-Z]+")
        dateTimeRegex = QRegExp("[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]")
        stringValidator = QRegExpValidator(txtRegex)
        self.inputDepartureStation.setValidator(stringValidator)
        self.inputArrivalStation.setValidator(stringValidator)


    def clearSelected(self):
        # reset the selected trip data to none
        selectedTrip.departure_station = ""
        selectedTrip.arrival_station = ""
        selectedTrip.price = ""
        selectedTrip.start_date = ""
        selectedTrip.end_date = ""

    def returnPrevScreen(self):
        self.clearSelected()
        widget.removeWidget(self)

    def loadTripInfo(self):
        self.inputDepartureStation.setText(selectedTrip.departure_station)
        self.inputArrivalStation.setText(selectedTrip.arrival_station)
        self.inputDateTime.setDateTime(QDateTime.fromString(selectedTrip.start_date, "yyyy-MM-dd HH:mm"))

    def findtripfunction(self):
        departure_station = self.inputDepartureStation.text()
        arrival_station = self.inputArrivalStation.text()
        departure_date = self.inputDateTime.text()
        seats_count = self.inputSeatsCount.text()
        # if len(departure_station) == 0 or len(arrival_station) == 0 or len(departure_date) == 0 or len(seats_count) == 0:
        #     QMessageBox.warning(self, "Warning", "Please fill in all the fields.")
        # else:
        show_matching_trips_screen = ShowMatchingTripsScreen()
        show_matching_trips_screen.loadTrips(
            departure_station, arrival_station, departure_date, seats_count)
        ShowMatchingTripsScreen.loadTrips(departure_station, arrival_station, departure_date, seats_count)
        widget.addWidget(ShowMatchingTripsScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)





class AdminOptionsScreen(QDialog):
    def __init__(self):
        super(AdminOptionsScreen, self).__init__()
        loadUi("ui/adminOptions.ui", self)
        self.addTrainButton.clicked.connect(self.gotoaddtrain)
        self.updateTrainButton.clicked.connect(self.gotoshowtrains)
        # self.addTripButton.clicked.connect(self.gotoaddtrip)
        # self.updateTripButton.clicked.connect(self.gotoupdatetrip)
        self.returnButton.clicked.connect(self.returnPrevScreen)

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def gotoaddtrain(self):
        addTrain = AddTrainScreen()
        widget.addWidget(addTrain)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoaddtrip(self):
        addTrip = AddTripScreen()
        widget.addWidget(addTrip)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoupdatetrip(self):
        updateTrip = UpdateTripScreen()
        widget.addWidget(updateTrip)
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
        # self.cancelButton.clicked.connect(self.gotocanceltrip)
        self.findTripButton.clicked.connect(self.gotofindtrip)
        self.returnButton.clicked.connect(self.returnPrevScreen)

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def gotobooktrip(self):
        bookTrip = ShowAllTrips()
        widget.addWidget(bookTrip)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocanceltrip(self):
        cancelTrip = CancelTripScreen()
        widget.addWidget(cancelTrip)
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
    main = ShowAllTrips()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main)
    widget.setFixedWidth(800)
    widget.setFixedHeight(840)
    widget.show()
    splash.finish(widget)
    # run app
    app.exec_()