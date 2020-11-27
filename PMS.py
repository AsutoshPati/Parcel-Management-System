"""
    Project Name:       Parcel Management
    Author:             Asutosh Pati (https://in.linkedin.com/in/asutoshpati)
    Date of Creation:   21 Nov. 2020
    Purpose:            for training of MCCAI - batch2 of CTTC, Bhuabneswar
    Description:
        This project simulates a real life example of Parcel Management system
        which will help the students to understand about the python and GUI
        integration with the data base. In this project we have 4 types of
        users (Admin, Agent, Customer, Manager), so that students can
        understand how diffrent roles work in programming environment; As this
        project provides certain functionalities that differ with the roles.
        Every user can have access to their own profile data which can be
        modified by the user itself. Every user can order a parcel and can
        track the ordered parcel. Where as an agent can pickup a pracel and
        can deliver to an user. An Manager is the incharge of a depot and can
        manage the shipment of parcel in depot of their supervision. An admin
        has access of creating a new depot, manage user privileges like
        appointing managers, angents and new admins along with this admin has
        full accesss over the database. With all this functionality the
        students can also learn about the versioning and the modification works
         that can be done during development of any project is required.

        ADVISORY:
             As this program is created by Asutosh Pati for educational purpose
              so use of this project with out authors consent is strictly
             prohibited. This project can only be used for teaching purpose
             with authors consent and other uses of this program is completely
              banned.

    Version:
        V 0.0.1: Released with beta version
        V 0.0.2: Database architecture modified(Parcel Table - add datetime
                 field)
"""

################################   Libraries   ################################

from functools import partial
from datetime import datetime
import sqlite3 as sql
from PyQt5 import QtWidgets, uic


#############################   Global variables   ############################

currentId = "" # store userid to know which user is currently logged in
currentRole = "" # store current users role


########################   Function to open UI pages   ########################

def openHomePage():
    home.show()

def openSignupPage():
    signup.show()

def openProfilePage():
    conn = sql.connect(r'Database\PMS.db')
    query = """SELECT UserDetail.id, name, phno, address,
desgType, password, role
FROM UserDetail JOIN Designation JOIN Authentication JOIN UserRole
ON (UserDetail.desgId = Designation.id
AND UserDetail.id = Authentication.userId
AND Authentication.userType = UserRole.id)
WHERE UserDetail.id = {}""".format(currentId)
    ret = conn.execute(query)
    data = ret.fetchall()[0]
    profile.label_8.setText(str(data[0]))
    profile.lineEdit.setText(str(data[1]))
    profile.lineEdit_2.setText(str(data[2]))
    profile.lineEdit_3.setText(str(data[5]))

    desg = str(data[4])
    if desg == "Mr.":
        profile.comboBox.setCurrentIndex(0)
    elif desg == "Mrs.":
        profile.comboBox.setCurrentIndex(1)
    elif desg == "Ms.":
        profile.comboBox.setCurrentIndex(2)
    else:
        profile.comboBox.setCurrentIndex(3)

    profile.textEdit.setPlainText(str(data[3]))
    profile.label_11.setText(str(data[6]))

    profile.label_3.setText(desg+" "+str(data[1]))

    conn.close()
    profile.show()

def openNewParcelPage():
    conn = sql.connect(r'Database\PMS.db')
    query = """SELECT name, address, desgType FROM UserDetail JOIN Designation
ON UserDetail.desgId = Designation.id
WHERE UserDetail.id = {}""".format(currentId)
    ret = conn.execute(query)
    data = ret.fetchall()[0]
    new_parcel.textBrowser.setText("To: " + data[2] + " " + data[0] +
                                   "\n\n" + data[1])
    new_parcel.show()

def openMyParcelPage():
    my_parcel.show()
    conn = sql.connect(r'Database\PMS.db')
    query = """SELECT id FROM Parcel WHERE deliverTo = {}
    ORDER BY datetime DESC""".format(currentId)
    ret = conn.execute(query)
    data = ret.fetchall()
    if len(data) == 0:
        failure.label_2.setText("No order has been placed yet")
        failure.show()
    else:
        for row in data:
            my_parcel.comboBox.addItem(str(row[0]))
    conn.close()

def openPickupPage():
    if currentRole == "Agent":
        pickup.show()
        return True
    else:
        failure.label_2.setText("Only agent can open this page")
        failure.show()
        return False


########################   Function to close UI pages   #######################

def closeHomePage():
    home.close()
    home.lineEdit.setText("")
    home.lineEdit_2.setText("")

def closeSignupPage():
    signup.close()
    signup.lineEdit.setText("")
    signup.lineEdit_2.setText("")
    signup.lineEdit_3.setText("")
    signup.textEdit.setPlainText("")
    signup.comboBox.setCurrentIndex(0)

def closeFailurePage():
    failure.close()
    failure.label_2.setText("")

def closeSuccessPage():
    success.close()
    success.label_2.setText("")

def closeProfilePage():
    profile.close()
    profile.label_8.setText("")
    profile.lineEdit.setText("")
    profile.lineEdit_2.setText("")
    profile.lineEdit_3.setText("")
    profile.comboBox.setCurrentIndex(0)
    profile.textEdit.setPlainText("")
    profile.label_11.setText("")
    profile.label_3.setText("")

def closeNewParcelPage():
    new_parcel.close()
    new_parcel.comboBox.setCurrentIndex(0)
    new_parcel.comboBox_2.setCurrentIndex(0)
    new_parcel.textBrowser.setText("")

def closeMyParcelPage():
    my_parcel.close()

def closePickupPage():
    pickup.close()


#############################   Extra functions   #############################

def travel(openPage, closePage):
    isCloseNeeded = True
    if openPage == "home":
        openHomePage()
    elif openPage == "signup":
        openSignupPage()
    elif openPage == "profile":
        openProfilePage()
    elif openPage == "new_parcel":
        openNewParcelPage()
    elif openPage == "my_parcel":
        openMyParcelPage()
    elif openPage == "pickup":
        isCloseNeeded = openPickupPage()

    if isCloseNeeded:
        if closePage == "home":
            closeHomePage()
        elif closePage == "signup":
            closeSignupPage()
        elif closePage == "profile":
            closeProfilePage()
        elif closePage == "new_parcel":
            closeNewParcelPage()
        elif closePage == "my_parcel":
            closeMyParcelPage()
        elif closePage == "pickup":
            closePickupPage()

def isValidPassword(pwd):
    if len(pwd) > 6 and len(pwd) < 18:
        upper = 0
        lower = 0
        digit = 0
        symbol = 0

        for ltr in pwd:
            if ltr.isupper():
                upper += 1
            elif ltr.islower():
                lower += 1
            elif ltr.isdigit():
                digit += 1
            elif ltr in "@#$&*":
                symbol += 1
            else:
                return False
        if upper and lower and digit and symbol:
            return True
        else:
            return False
    else:
        return False

def doLogout(fromPage):
    global currentId, currentRole

    currentId = ""
    currentRole = ""
    travel("home", fromPage)


########################   Functions for in UI pages   ########################

def doSignup():
    global currentId, currentRole

    desg = signup.comboBox.currentText()
    name = signup.lineEdit.text()
    if len(name) < 3:
        failure.label_2.setText("Name should be atleast 3 characters long")
        failure.show()
        return
    for char in name:
        if char.isupper() or char.lower() or char.isspace():
            continue
        else:
            failure.label_2.setText("""Name should contain uppercase, lowercase
 and spaces only""")
            failure.show()
            return
    phno = signup.lineEdit_2.text()
    if not phno.isdigit() or len(phno) != 10:
        # check whether the input is a number and must be 10 digit long
        failure.label_2.setText("Phone number should be 10 digits long only")
        failure.show()
        return
    pwd = signup.lineEdit_3.text()
    if not isValidPassword(pwd):
        failure.label_2.setText("""Invalid Password
1. password should be 6 - 18 characters long
2. password should contain atleast 1 uppercase, 1 lowercase, 1 digit and
1 symbol from @#$&*""")
        failure.show()
        return
    address = signup.textEdit.toPlainText()
    if len(address) < 10:
        failure.label_2.setText("address should be atleast 10 characters long")
        failure.show()
        return

    # print the details if every input is correct
    # print(desg, name, phno, pwd, address)

    # insert the details in database if every input is correct
    conn = sql.connect(r'Database\PMS.db')
    query = """INSERT INTO UserDetail(name, phno, address, desgId)
VALUES('{}', {}, '{}', (SELECT id FROM Designation
WHERE desgType = '{}'))""".format(name, phno, address, desg)
    try:
        conn.execute(query)
    except sql.IntegrityError:
        failure.label_2.setText("Phone number already registered")
        failure.show()
        return
    except Exception as err:
        failure.label_2.setText(str(err))
        failure.show()
        return
    else:
        query = """SELECT last_insert_rowid()"""
        ret = conn.execute(query)
        userid = ret.fetchall()[0][0]

        query = """INSERT INTO Authentication VALUES((SELECT
        last_insert_rowid()), '{}', 3)""".format(pwd)
        try:
            conn.execute(query)
        except sql.IntegrityError:
            failure.label_2.setText("Phone number already registered")
            failure.show()
            return
        except Exception as err:
            failure.label_2.setText(str(err))
            failure.show()
            return
    conn.commit()
    conn.close()

    # if everything goes well... Account is created
    # set the userid as current id (login process)
    currentId = userid
    currentRole = "Customer"
    # open the profile page
    openProfilePage()

    # show the success message
    success.label_2.setText("Your account has been created")
    success.show()

    closeSignupPage()

def doLogin():
    global currentId, currentRole

    userid = home.lineEdit.text()
    pwd = home.lineEdit_2.text()

    conn = sql.connect(r'Database\PMS.db')
    query = """SELECT UserRole.role FROM Authentication JOIN UserRole
ON Authentication.userType = UserRole.id
WHERE userId = {} AND password = '{}'""".format(userid, pwd)
    ret = conn.execute(query)
    data = ret.fetchall()
    if len(data) == 0:
        # if no row returned then either userid or password
        # or both are incorrect.
        failure.label_2.setText("Invalid UserID or Password")
        failure.show()
        return
    else:
        # if correct userid and password entered
        # set the userid as current id (login process)
        currentId = userid
        currentRole = data[0][0]
        travel("profile", "home")
    conn.close()

def modifyProfile():
    name = profile.lineEdit.text()
    if len(name) < 3:
        failure.label_2.setText("Name should be atleast 3 characters long")
        failure.show()
        return
    for char in name:
        if char.isupper() or char.lower() or char.isspace():
            continue
        else:
            failure.label_2.setText("""Name should contain uppercase, lowercase
 and spaces only""")
            failure.show()
            return
    phone = profile.lineEdit_2.text()
    if not phone.isdigit() or len(phone) != 10:
        # check whether the input is a number and must be 10 digit long
        failure.label_2.setText("Phone number should be 10 digits long only")
        failure.show()
        return
    pwd = profile.lineEdit_3.text()
    if not isValidPassword(pwd):
        failure.label_2.setText("""Invalid Password
1. password should be 6 - 18 characters long
2. password should contain atleast 1 uppercase, 1 lowercase, 1 digit and
1 symbol from @#$&*""")
        failure.show()
        return
    desg = profile.comboBox.currentText()
    address = profile.textEdit.toPlainText()
    if len(address) < 10:
        failure.label_2.setText("address should be atleast 10 characters long")
        failure.show()
        return

    conn = sql.connect(r'Database\PMS.db')
    query = """UPDATE UserDetail SET name='{}', phno={}, address='{}',
desgId=(SELECT id FROM Designation WHERE desgType='{}') WHERE id={}""".format(
    name, phone, address, desg, currentId)
    try:
        conn.execute(query)
    except sql.IntegrityError:
        failure.label_2.setText("Phone number already exist")
        failure.show()
        return
    except Exception as err:
        failure.label_2.setText("Unable to modify because \n" + str(err))
        failure.show()
        return
    else:
        query = """UPDATE Authentication SET password='{}'
WHERE userId={}""".format(pwd, currentId)
        try:
            conn.execute(query)
        except Exception as err:
            failure.label_2.setText("Unable to modify because \n" + str(err))
            failure.show()
            return
    conn.commit()
    conn.close()

    closeProfilePage()
    openProfilePage()   # it will show the updated data
    success.label_2.setText("Your profile has been updated")
    success.show()

def placeOrder():
    pay = new_parcel.comboBox.currentText()
    category = new_parcel.comboBox_2.currentText()
    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    conn = sql.connect(r'Database\PMS.db')
    query = """INSERT INTO Parcel(paymentType, productType, deliverTo,
datetime) VALUES((SELECT id FROM paymentType WHERE payType='{}'),
(SELECT id FROM ProductCategory WHERE productType='{}'), {}, '{}'
)""".format(pay, category, currentId, now)
    try:
        conn.execute(query)
        conn.commit()
    except Exception as err:
        failure.label_2.setText("Unable to place order because \n" + str(err))
        failure.show()
        return
    else:
        query = """SELECT last_insert_rowid()"""
        ret = conn.execute(query)
        orderid = ret.fetchall()[0][0]

        success.label_2.setText("Order placed \n Your order id is " +
                                str(orderid))
        success.show()
        return
    conn.close()

def checkParcelDetails():
    parcelid = my_parcel.comboBox.currentText()
    if not parcelid.isdigit():
        failure.label_2.setText("Please select a valid parcel ID")
        failure.show()
        return
    conn = sql.connect(r'Database\PMS.db')
    query = """SELECT Parcel.id, PaymentType.payType, weight, length, breadth,
height,ProductCategory.productType, Designation.desgType, UserDetail.name,
UserDetail.address, datetime
FROM Parcel JOIN PaymentType JOIN ProductCategory JOIN UserDetail
JOIN Designation
ON (Parcel.paymentType = PaymentType.id
AND Parcel.productType = ProductCategory.id
AND Parcel.deliverTo = UserDetail.id AND UserDetail.desgId = Designation.id)
WHERE Parcel.id = {} ORDER BY datetime DESC""".format(parcelid)
    ret = conn.execute(query)
    row = ret.fetchall()[0]
    my_parcel.label_6.setText(str(row[0]))
    my_parcel.label_21.setText(row[1])
    my_parcel.label_14.setText("Kgs - " + str(row[2]))
    my_parcel.label_15.setText("cm - " + str(row[3]))
    my_parcel.label_16.setText("cm - " + str(row[4]))
    my_parcel.label_17.setText("cm - " + str(row[5]))
    my_parcel.label_18.setText(row[6])
    my_parcel.label_20.setText(row[10][:10])
    my_parcel.textBrowser.setText("To: " + row[7] + " " + row[8] + "\n\n" +
                                  row[9])
    conn.close()

def completePickup():
    parcelid = pickup.lineEdit.text()
    weight = pickup.doubleSpinBox.text()
    length = pickup.doubleSpinBox_2.text()
    breadth = pickup.doubleSpinBox_3.text()
    height = pickup.doubleSpinBox_4.text()
    ret_loc = pickup.textEdit.toPlainText()
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    conn = sql.connect(r'Database\PMS.db')
    query = """SELECT * FROM ParcelActionTaken
WHERE parcelId = {}""".format(parcelid)
    ret = conn.execute(query)
    data = ret.fetchall()
    if len(data) != 0:
        failure.label_2.setText("""This parcel can't be picked up
due to the last status is """ + data[0][0] + " at " + str(data[0][1]))
        failure.show()
        return
    query = """UPDATE Parcel SET weight= {}, length= {}, breadth= {},
height= {} WHERE id={}""".format(weight, length, breadth, height, parcelid)
    try:
        conn.execute(query)
    except Exception as err:
        failure.label_2.setText("Unable to pickup order because \n" + str(err))
        failure.show()
        return
    else:
        query = """INSERT INTO ParcelActionTaken VALUES({},
(SELECT id FROM ParcelAction WHERE action = "Picked up"),
'{}')""".format(parcelid, now)
        try:
            conn.execute(query)
        except Exception as err:
            failure.label_2.setText("Unable to pickup order because \n" +
                                    str(err))
            failure.show()
            return
        else:
            query = """INSERT INTO Pickup VALUES({}, {}, '{}',
'{}')""".format(currentId, parcelid, ret_loc, now)
            try:
                conn.execute(query)
            except Exception as err:
                failure.label_2.setText("Unable to pickup order because \n" +
                                        str(err))
                failure.show()
                return
            else:
                conn.commit()
                success.label_2.setText("The order has been picked up")
                success.show()
    conn.close()


###############################   Main Program   ##############################

try:
    # create the application
    app = QtWidgets.QApplication([])

    # load the ui pages
    home = uic.loadUi(r'pages\home.ui')
    signup = uic.loadUi(r'pages\signup.ui')
    failure = uic.loadUi(r'pages\failure.ui')
    success = uic.loadUi(r'pages\success.ui')
    profile = uic.loadUi(r'pages\profile.ui')
    new_parcel = uic.loadUi(r'pages\order parcel.ui')
    my_parcel = uic.loadUi(r'pages\my parcels.ui')
    pickup = uic.loadUi(r'pages\pickup.ui')

    # show the home page initially
    home.show()

    # create listeners
    ### home page buttons
    home.pushButton_3.clicked.connect(partial(travel, "signup", "home"))
    home.pushButton_2.clicked.connect(doLogin)
    ### sigup page buttons
    signup.pushButton.clicked.connect(partial(travel, "home", "signup"))
    signup.pushButton_2.clicked.connect(doSignup)
    ### failure page buttons
    failure.pushButton.clicked.connect(closeFailurePage)
    ### success page buttons
    success.pushButton.clicked.connect(closeSuccessPage)
    ### profile page buttons
    profile.pushButton_7.clicked.connect(partial(doLogout, "profile"))
    profile.pushButton_6.clicked.connect(modifyProfile)
    profile.pushButton_2.clicked.connect(partial(travel, "new_parcel",
                                                 "profile"))
    profile.pushButton_3.clicked.connect(partial(travel, "pickup", "profile"))
    ### new_parcel page buttons
    new_parcel.pushButton.clicked.connect(partial(travel, "profile",
                                                  "new_parcel"))
    new_parcel.pushButton_7.clicked.connect(partial(doLogout, "new_parcel"))
    new_parcel.pushButton_6.clicked.connect(placeOrder)
    new_parcel.pushButton_9.clicked.connect(partial(travel, "my_parcel",
                                                    "new_parcel"))
    new_parcel.pushButton_3.clicked.connect(partial(travel, "pickup",
                                                    "new_parcel"))
    ### my_parcel page buttons
    my_parcel.pushButton.clicked.connect(partial(travel, "profile",
                                                 "my_parcel"))
    my_parcel.pushButton_7.clicked.connect(partial(doLogout, "my_parcel"))
    my_parcel.pushButton_8.clicked.connect(partial(travel, "new_parcel",
                                                   "my_parcel"))
    my_parcel.pushButton_6.clicked.connect(checkParcelDetails)
    my_parcel.pushButton_3.clicked.connect(partial(travel, "pickup",
                                                   "my_parcel"))
    ### pickup page buttons
    pickup.pushButton.clicked.connect(partial(travel, "profile", "pickup"))
    pickup.pushButton_2.clicked.connect(partial(travel, "new_parcel",
                                                "pickup"))
    pickup.pushButton_7.clicked.connect(partial(doLogout, "pickup"))
    pickup.pushButton_6.clicked.connect(completePickup)

    # execute the application
    app.exec()

    # delete the application
    del app
except Exception as err:
    print(err)
