import sys
import mysql.connector

import shutil

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='chatbot'
)
# prepare a cursor object using cursor() method
cursor = mydb.cursor()


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.submit.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createacc.clicked.connect(self.gotocreate)

    def loginfunction(self):
        usera = self.username.text()
        pad = self.password.text()
        cmd = "SELECT * FROM signup WHERE username = '%s' AND password = '%s'" % (usera, pad)

        try:

            re = cursor.execute(cmd)
            res = cursor.fetchall()

            if res != 0:
                createadmin = CreateAdmin()
                widget.addWidget(createadmin)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            else:
                print("hello")


        except:
            # Rollback in case there is any error
            mydb.rollback()

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("signup.ui", self)

        self.signsubmit.clicked.connect(self.createaccfunction)

    def createaccfunction(self):
        user = self.signuser.text()
        ema = self.signemail.text()
        passw = self.sign.text()

        # Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO signup(username,email, password) VALUES ('%s', '%s','%s')" % \
              (user, ema, passw)

        try:

            cursor.execute(sql)
            # Commit your changes in the database
            mydb.commit()
        except:
            # Rollback in case there is any error
            mydb.rollback()

        # disconnect from server
        mydb.close()
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAdmin(QDialog):
    def __init__(self):
        super(CreateAdmin, self).__init__()
        loadUi("admin.ui", self)

        self.browse.clicked.connect(self.browfun)
        self.upload.clicked.connect(self.uploads)

    def browfun(self):
        global fname
        fname = QFileDialog.getOpenFileName(self, 'Open file', r"C:\Users\muham\Desktop\version 2\version 2")



    def uploads(self):
     print(fname)

app = QApplication(sys.argv)
mainwindow = CreateAdmin()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()
