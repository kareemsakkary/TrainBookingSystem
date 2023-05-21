# install Pyqt5 & Qt designer by "pip install pyqt5" , "pip install pyqt5-tools"

import sys
import time
import databaseSQL
import models

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRegExp, QDate
from PyQt5.QtGui import *

db = databaseSQL.database()

loggedInUser = models.Account()
selectedTrain = models.Train()


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
        widget.setCurrentIndex(widget.currentIndex()+1)

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
            for row in db.selectAll("Account",f"email ='{email}' and password ='{password}'"):
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
        x = msg.exec_()

    def signupfunction(self):
        name = self.inputName.text()
        email = self.inputEmail.text()
        password = self.inputPassword.text()
        phoneNum = self.inputNumber.text()
        dob = self.inputDob.text()
        address = self.inputAddress.text()
        if len(name) == 0 or len(email) == 0 or len(password) == 0 or len(phoneNum) == 0 or len(address) == 0:
            self.error.setText("")
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

    def returnPrevScreen(self):
        widget.removeWidget(self)

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
        x = msg.exec_()

    def addtrainfunction(self):
        cap = self.inputCapacity.text()
        numOfCart = self.inputNumofcart.text()
        manufacture = self.inputManufacturer.text()
        if len(cap) == 0 or len(numOfCart) == 0 or len(
                manufacture) == 0 or (not self.activeRadioButton.isChecked() and not self.inactiveRadioButton.isChecked()):
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
        # reset the selected train data to none
        selectedTrain.train_id = ""
        selectedTrain.status = ""
        selectedTrain.capacity = ""
        selectedTrain.manufacture = ""
        selectedTrain.no_of_cart = ""

    def getClickedCell(self, row):
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
        updateTrain = UpdateTrainScreen()
        widget.addWidget(updateTrain)
        widget.setCurrentIndex(widget.currentIndex() + 1)


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
        x = msg.exec_()

    def clearSelected(self):
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
                manufacture) == 0 or (not self.activeRadioButton.isChecked() and not self.inactiveRadioButton.isChecked()):
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


class ShowAllTrips(QDialog):
    def __init__(self):
        super(ShowAllTrips, self).__init__()
        # load UI


class UpdateTripScreen(QDialog):
    def __init__(self):
        super(UpdateTripScreen, self).__init__()
        # load UI


class BookTripScreen(QDialog):
    def __init__(self):
        super(BookTripScreen, self).__init__()
        # load UI


class CancelTripScreen(QDialog):
    def __init__(self):
        super(CancelTripScreen, self).__init__()
        # load UI


class FindTripScreen(QDialog):
    def __init__(self):
        super(FindTripScreen, self).__init__()
        # load UI


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
        # self.bookButton.clicked.connect(self.gotobooktrip)
        # self.cancelButton.clicked.connect(self.gotocanceltrip)
        # self.findTripButton.clicked.connect(self.gotofindtrip)
        self.returnButton.clicked.connect(self.returnPrevScreen)

    def returnPrevScreen(self):
        widget.removeWidget(self)

    def gotobooktrip(self):
        bookTrip = BookTripScreen()
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
    main = MainScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main)
    widget.setFixedWidth(800)
    widget.setFixedHeight(840)
    widget.show()
    splash.finish(widget)
    # run app
    app.exec_()