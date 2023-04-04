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
        V 0.1.0: structure optimised
"""

################################   Libraries   ################################

import ctypes
from datetime import datetime
from functools import partial
import os
import sqlite3 as sql
import sys

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QWidget,
)

#############################   Helper functions   ############################
def create_or_ignore_db():
    sql_file = open(SQL_FILE, "rt")
    sql_cmd = sql_file.read()
    conn = sql.connect(DB_FILE)
    conn.executescript(sql_cmd)
    conn.commit()
    conn.close()
    sql_file.close()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#############################   Global variables   ############################

current_id = None  # store userid to know which user is currently logged in
current_role = None  # store current users role

DB_FILE = resource_path("assets/database/PMS.db")
SQL_FILE = resource_path("assets/database/PMS.sql")

# window resizing variables
last_win_size = dict()  # store the last window size before resizing
display_frame_width = 1000  # default width of app window
display_frame_height = 600  # default height of app window


##############################   Load UI pages   ##############################


class Home(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/home_widget.ui"), self)


class Signup(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/signup_widget.ui"), self)


# class Failure(QWidget):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         uic.loadUi('assets/pages/failure.ui', self)

# class Success(QWidget):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         uic.loadUi('assets/pages/success.ui', self)


class ForgotPassword(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/forgot_password_widget.ui"), self)


class Profile(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/profile_widget.ui"), self)


class NewParcel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/order_parcel_widget.ui"), self)


class MyParcel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/my_parcels_widget.ui"), self)


class TrackParcel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/track_parcel_widget.ui"), self)


class Pickup(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/pickup_widget.ui"), self)


class Deliver(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/deliver_widget.ui"), self)


class ManageRole(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/manage_role_widget.ui"), self)


class NewCity(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/expand_city_widget.ui"), self)


class NewDepot(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/new_depot_widget.ui"), self)


class AssignManager(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/assign_manager_widget.ui"), self)


class Receive(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/receive_widget.ui"), self)


class Dispatch(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/dispatch_widget.ui"), self)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(resource_path("assets/pages/main_win.ui"), self)

        # Page 0
        self.home = Home()
        self.stackedWidget.addWidget(self.home)
        # Page 1
        self.signup = Signup()
        self.stackedWidget.addWidget(self.signup)
        # self.failure = Failure()
        # self.stackedWidget.addWidget(self.failure)
        # self.success = Success()
        # self.stackedWidget.addWidget(self.success)
        # Page 2
        self.forgot_password = ForgotPassword()
        self.stackedWidget.addWidget(self.forgot_password)
        # Page 3
        self.profile = Profile()
        self.stackedWidget.addWidget(self.profile)
        # Page 4
        self.new_parcel = NewParcel()
        self.stackedWidget.addWidget(self.new_parcel)
        # Page 5
        self.my_parcel = MyParcel()
        self.stackedWidget.addWidget(self.my_parcel)
        # Page 6
        self.pickup = Pickup()
        self.stackedWidget.addWidget(self.pickup)
        # Page 7
        self.deliver = Deliver()
        self.stackedWidget.addWidget(self.deliver)
        # Page 8
        self.manage_role = ManageRole()
        self.stackedWidget.addWidget(self.manage_role)
        # Page 9
        self.new_city = NewCity()
        self.stackedWidget.addWidget(self.new_city)
        # Page 10
        self.new_depot = NewDepot()
        self.stackedWidget.addWidget(self.new_depot)
        # Page 11
        self.assign_manager = AssignManager()
        self.stackedWidget.addWidget(self.assign_manager)
        # Page 12
        self.receive = Receive()
        self.stackedWidget.addWidget(self.receive)
        # Page 13
        self.dispatch = Dispatch()
        self.stackedWidget.addWidget(self.dispatch)
        # Page 14
        self.track_parcel = TrackParcel()
        self.stackedWidget.addWidget(self.track_parcel)


#######################   Function for responsiveness   #######################


def window_name(self):
    """
    Get the window name from the object when this method is being called.

    Returns
    -------
    str / None
        Return window name if found else None.

    """
    for name, module in sys.modules.items():
        try:
            for var_name, obj in module.__dict__.items():
                if obj is self:
                    return str(var_name)
        except AttributeError:
            return None


def resize_event(self, event) -> None:
    """
    Scale all the widgets as per window size whenever window is resized.

    Returns
    -------
    None.

    """
    global last_win_size, display_frame_width
    global display_frame_height

    try:
        win_width, win_height = self.size().width(), self.size().height()
        win = self.window_name()

        # print(win, '-->', last_win_size)

        # if it is the opening then just set the base size
        if win not in last_win_size:
            last_win_size.update({win: (win_width, win_height)})

        else:
            # ratio of change in width
            dw = (win_width - last_win_size[win][0]) / last_win_size[win][0]
            # ratio of change in height
            dh = (win_height - last_win_size[win][1]) / last_win_size[win][1]
            # change every widget as per the ratio

            # background image
            # self.label.resize(round(self.label.size().width() +
            #                         self.label.size().width() * dw),
            #                   round(self.label.size().height() +
            #                         self.label.size().height() * dh))
            # if win == 'login_page':
            #     """
            #     label_2 - air face logo
            #     label_3 - auth key label
            #     lineEdit - auth key input
            #     label_4 - host label
            #     lineEdit_2 - host input
            #     pushButton - login button
            #     """
            #     widgets_to_resize = [self.label_2, self.label_3,
            #                          self.lineEdit, self.label_4,
            #                          self.lineEdit_2, self.pushButton]
            #     for obj in widgets_to_resize:
            #         obj.move(round(obj.x() + obj.x() * dw),
            #                  round(obj.y() + obj.y() * dh))
            #         obj.resize(round(obj.size().width() +
            #                          obj.size().width() * dw),
            #                    round(obj.size().height() +
            #                          obj.size().height() * dh))

            # elif win == 'menu_page':
            #     """
            #     label_2 - side image
            #     pushButton - add employee button
            #     pushButton_2 - view employees button
            #     pushButton_3 - enroll employees button
            #     pushButton_4 - logout button
            #     """
            #     widgets_to_resize = [self.label_2, self.pushButton,
            #                          self.pushButton_2, self.pushButton_3,
            #                          self.pushButton_4]
            #     for obj in widgets_to_resize:
            #         obj.move(round(obj.x() + obj.x() * dw),
            #                  round(obj.y() + obj.y() * dh))
            #         obj.resize(round(obj.size().width() +
            #                          obj.size().width() * dw),
            #                    round(obj.size().height() +
            #                          obj.size().height() * dh))
            # elif win == 'add_page':
            #     """
            #     label_2 - page name label
            #     label_3 - page icon label
            #     pushButton - view employees button
            #     pushButton_2 - enroll employees button
            #     pushButton_3 - logout button
            #     label_4 - employee id label
            #     lineEdit - employee id input
            #     label_5 - employee name label
            #     lineEdit_2 - employee name input
            #     label_6 - mail id label
            #     lineEdit_3 - mail id input
            #     label_7 - mobile number label
            #     lineEdit_4 - mobile number input
            #     label_8 - location label
            #     comboBox - location input
            #     pushButton_4 - add button
            #     """
            #     widgets_to_resize = [self.label_2, self.label_3,
            #                          self.pushButton, self.pushButton_2,
            #                          self.pushButton_3, self.label_4,
            #                          self.lineEdit, self.label_5,
            #                          self.lineEdit_2, self.label_6,
            #                          self.lineEdit_3, self.label_7,
            #                          self.lineEdit_4, self.label_8,
            #                          self.comboBox, self.pushButton_4]
            #     for obj in widgets_to_resize:
            #         obj.move(round(obj.x() + obj.x() * dw),
            #                  round(obj.y() + obj.y() * dh))
            #         obj.resize(round(obj.size().width() +
            #                          obj.size().width() * dw),
            #                    round(obj.size().height() +
            #                          obj.size().height() * dh))
            # elif win == 'search_page':
            #     """
            #     label_2 - page name label
            #     label_3 - page icon label
            #     pushButton - add employees button
            #     pushButton_2 - enroll employees button
            #     pushButton_3 - logout button
            #     checkBox - employee id label
            #     lineEdit - employee id input
            #     checkBox_3 - employee name label
            #     lineEdit_2 - employee name input
            #     checkBox_4 - mail id label
            #     lineEdit_3 - mail id input
            #     checkBox_2 - mobile number label
            #     lineEdit_4 - mobile number input
            #     pushButton_4 - search button
            #     tableWidget - table
            #     """
            #     widgets_to_resize = [self.label_2, self.label_3,
            #                          self.pushButton, self.pushButton_2,
            #                          self.pushButton_3, self.checkBox,
            #                          self.lineEdit, self.checkBox_3,
            #                          self.lineEdit_2, self.checkBox_4,
            #                          self.lineEdit_3, self.checkBox_2,
            #                          self.lineEdit_4, self.pushButton_4,
            #                          self.tableWidget]
            #     for obj in widgets_to_resize:
            #         obj.move(round(obj.x() + obj.x() * dw),
            #                  round(obj.y() + obj.y() * dh))
            #         obj.resize(round(obj.size().width() +
            #                          obj.size().width() * dw),
            #                    round(obj.size().height() +
            #                          obj.size().height() * dh))
            # elif win == 'enroll_page':
            #     """
            #     label_2 - page name label
            #     label_3 - page icon label
            #     pushButton - add employees button
            #     pushButton_2 - search employees button
            #     pushButton_3 - logout button
            #     label_23 - employee id label
            #     comboBox - employee id input
            #     pushButton_4 - show button
            #     label_4 - employee name label
            #     label_5 - employee name display label
            #     pushButton_5 - start enroll button
            #     label_6 - frame label
            #     label_21 - movie label
            #     label_22 - message label
            #     label_7 - group label
            #     label_20 - face captured label
            #     pushButton_6 - proceed button
            #     label_8 to 19 - captured faces label
            #     pushButton_7 to 18 - delete button for captured faces
            #     """
            #     widgets_to_resize = [self.label_2, self.label_3,
            #                          self.pushButton, self.pushButton_2,
            #                          self.pushButton_3, self.label_23,
            #                          self.comboBox, self.pushButton_4,
            #                          self.label_4, self.label_5,
            #                          self.pushButton_5, self.label_6,
            #                          self.label_21, self.label_22,
            #                          self.label_7, self.label_20,
            #                          self.pushButton_6, self.label_8,
            #                          self.label_9, self.label_10,
            #                          self.label_11, self.label_12,
            #                          self.label_13, self.label_14,
            #                          self.label_15, self.label_16,
            #                          self.label_17, self.label_18,
            #                          self.label_19, self.pushButton_7,
            #                          self.pushButton_8, self.pushButton_9,
            #                           self.pushButton_10, self.pushButton_11,
            #                           self.pushButton_12, self.pushButton_13,
            #                           self.pushButton_14, self.pushButton_15,
            #                           self.pushButton_16, self.pushButton_17,
            #                           self.pushButton_18,
            #                           ]
            #     for obj in widgets_to_resize:
            #         obj.move(round(obj.x() + obj.x() * dw),
            #                   round(obj.y() + obj.y() * dh))
            #         obj.resize(round(obj.size().width() +
            #                           obj.size().width() * dw),
            #                     round(obj.size().height() +
            #                           obj.size().height() * dh))

        last_win_size.update({win: (win_width, win_height)})
    except Exception as err:
        print("Error in resize_event() --> ", err, type(err))


########################   Function to open UI pages   ########################


def show_message_box(msg_type: str = "info", msg: str = ""):
    """
    Show a message popup box with the information like success or error messages

    Parameters
    ----------
    msg_type : str, optional
        Type of message to be displayed (info|error). The default is "info".
    msg : str, optional
        Message to be displayed in the message box. The default is "".

    Returns
    -------
    None.

    """
    msg_box = QMessageBox()
    msg_box.setWindowTitle("PMS")
    msg_box.setWindowIcon(QIcon("assets/images/PMS logo.png"))
    if msg_type == "error":
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("OOPS!!")
    else:
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Information")
    msg_box.setInformativeText(msg)
    msg_box.setStandardButtons(QMessageBox.Close)
    msg_box.exec_()


def openHomePage():
    """
    Show home page

    Returns
    -------
    bool
        Whether to close the last opened page.

    """
    main_win.stackedWidget.setCurrentIndex(0)
    return True


def openSignupPage():
    """
    Show signup page

    Returns
    -------
    bool
        Whether to close the last opened page.

    """
    main_win.stackedWidget.setCurrentIndex(1)
    return True


def openForgotPassword():
    """
    Show forgot password page

    Returns
    -------
    bool
        Whether to close the last opened page.

    """
    main_win.stackedWidget.setCurrentIndex(2)
    return True


def openProfilePage():
    """
    Show profile page and display user details in it

    Returns
    -------
    bool
        Whether to close the last opened page.

    """
    conn = sql.connect(DB_FILE)
    query = (
        "SELECT UserDetail.id, name, phno, address, desgType, password, "
        "role FROM UserDetail JOIN Designation JOIN Authentication JOIN "
        "UserRole ON (UserDetail.desgId = Designation.id AND UserDetail.id = "
        "Authentication.userId AND Authentication.userType = UserRole.id) "
        f"WHERE UserDetail.id = {current_id}"
    )
    ret = conn.execute(query)
    data = ret.fetchall()[0]
    main_win.profile.label_8.setText(str(data[0]))
    main_win.profile.lineEdit.setText(str(data[1]))
    main_win.profile.lineEdit_2.setText(str(data[2]))
    main_win.profile.lineEdit_3.setText(str(data[5]))

    desg = str(data[4])
    if desg == "Mr.":
        main_win.profile.comboBox.setCurrentIndex(0)
    elif desg == "Mrs.":
        main_win.profile.comboBox.setCurrentIndex(1)
    elif desg == "Ms.":
        main_win.profile.comboBox.setCurrentIndex(2)
    else:
        main_win.profile.comboBox.setCurrentIndex(3)

    main_win.profile.textEdit.setPlainText(str(data[3]))
    main_win.profile.label_11.setText(str(data[6]))

    main_win.profile.label_3.setText(desg + " " + str(data[1]))

    conn.close()

    main_win.stackedWidget.setCurrentIndex(3)
    return True


def openNewParcelPage():
    """
    Show order parcel page and display the delivery address

    Returns
    -------
    bool
        Whether to close the last opened page.

    """
    conn = sql.connect(DB_FILE)
    query = (
        "SELECT name, address, desgType FROM UserDetail "
        "JOIN Designation ON UserDetail.desgId = Designation.id "
        f"WHERE UserDetail.id = {current_id}"
    )
    ret = conn.execute(query)
    data = ret.fetchall()[0]
    main_win.new_parcel.textBrowser.setText("To: " + data[2] + " " + data[0] + "\n\n" + data[1])
    conn.close()
    main_win.stackedWidget.setCurrentIndex(4)
    return True


def openMyParcelPage():
    """
    Show my parcel page and add all ordered parcel id to the combobox

    Returns
    -------
    bool
        Whether to close the last opened page.

    """
    main_win.stackedWidget.setCurrentIndex(5)
    conn = sql.connect(DB_FILE)
    query = f"SELECT id FROM Parcel WHERE deliverTo = {current_id} " "ORDER BY id DESC"
    ret = conn.execute(query)
    data = ret.fetchall()
    if len(data) == 0:
        show_message_box(msg_type="error", msg="No order has been placed yet")
    else:
        for row in data:
            main_win.my_parcel.comboBox.addItem(str(row[0]))
    conn.close()
    return True


def openPickupPage():
    """
    Show pickup page only to agents. if agent is logged in then only show the
    page otherwise display error message.

    Returns
    -------
    bool
        return True if previous page needs to be closed.

    """
    if current_role == "Agent":
        main_win.stackedWidget.setCurrentIndex(6)
        return True
    else:
        show_message_box(msg_type="error", msg="Only agents can open this page")
        return False


def openDeliverPage():
    """
    Show deliver page

    Returns
    -------
    None.

    """
    main_win.stackedWidget.setCurrentIndex(7)
    return True


def openManageRolePage():
    """
    Show manage role page only to admins. if admin is logged in then only show
    the page otherwise display error message.

    Returns
    -------
    bool
        return True if previous page needs to be closed.

    """
    if current_role == "Admin":
        main_win.stackedWidget.setCurrentIndex(8)
        return True
    else:
        show_message_box(msg_type="error", msg="Only admins can open this page")
        return False


def openNewCityPage():
    """
    Display the new city page

    Returns
    -------
    None.

    """
    main_win.new_city.comboBox.clear()
    conn = sql.connect(DB_FILE)
    query = "SELECT name FROM City ORDER BY name ASC"
    ret = conn.execute(query)
    data = ret.fetchall()
    for i in data:
        main_win.new_city.comboBox.addItem(i[0])
    conn.close()
    main_win.stackedWidget.setCurrentIndex(9)
    return True


def openNewDepotPage():
    """
    Display new depot page

    Returns
    -------
    None.

    """
    main_win.stackedWidget.setCurrentIndex(10)
    return True


def openAssignManagerPage():
    """
    Display assign manager page

    Returns
    -------
    None.

    """
    main_win.stackedWidget.setCurrentIndex(11)
    return True


def openReceivePage():
    """
    Show Receive page only to managers. if manager is logged in then only show
    the page otherwise display error message.

    Returns
    -------
    bool
        return True if previous page needs to be closed.

    """
    if current_role == "Manager":
        conn = sql.connect(DB_FILE)
        query = (
            "SELECT Depot.id FROM Depot JOIN City ON Depot.cityId=City.id "
            f"WHERE manager={current_id} ORDER BY Depot.id ASC"
        )
        ret = conn.execute(query)
        data = ret.fetchall()
        if data:
            for row in data:
                main_win.receive.comboBox.addItem(str(row[0]))
        conn.close()
        main_win.stackedWidget.setCurrentIndex(12)
        return True
    else:
        show_message_box(msg_type="error", msg="Only managers can open this page")
        return False


def openTrackParcelPage():
    main_win.stackedWidget.setCurrentIndex(14)

    conn = sql.connect(DB_FILE)
    query = f"SELECT id FROM Parcel WHERE deliverTo = {current_id} " "ORDER BY id DESC"
    ret = conn.execute(query)
    data = ret.fetchall()
    if len(data) == 0:
        show_message_box(msg_type="error", msg="No order has been placed yet")
    else:
        for row in data:
            main_win.track_parcel.comboBox.addItem(str(row[0]))
    conn.close()
    return True


def openDispatchPage():
    """
    Show dispatch page only to managers. if manager is logged in then only show
    the page otherwise display error message.

    Returns
    -------
    bool
        return True if previous page needs to be closed.

    """
    if current_role == "Manager":
        conn = sql.connect(DB_FILE)
        query = (
            "SELECT Depot.id FROM Depot JOIN City ON Depot.cityId=City.id "
            f"WHERE manager={current_id} ORDER BY Depot.id ASC"
        )
        ret = conn.execute(query)
        data = ret.fetchall()
        if data:
            for row in data:
                main_win.dispatch.comboBox.addItem(str(row[0]))
        conn.close()
        main_win.stackedWidget.setCurrentIndex(13)
        return True
    else:
        show_message_box(msg_type="error", msg="Only managers can open this page")
        return False


########################   Function to close UI pages   #######################


def closeHomePage():
    """
    Close home page and before closing remove all dynamic details present.

    Returns
    -------
    None.

    """
    # main_win.home.close()
    main_win.home.lineEdit.setText("")
    main_win.home.lineEdit_2.setText("")


def closeSignupPage():
    """
    Close signup page and before closing remove all dynamic details present.

    Returns
    -------
    None.

    """
    # main_win.signup.close()
    main_win.signup.lineEdit.setText("")
    main_win.signup.lineEdit_2.setText("")
    main_win.signup.lineEdit_3.setText("")
    main_win.signup.textEdit.setPlainText("")
    main_win.signup.comboBox.clear()


def closeForgotPassword():
    """
    Close forgot password page and before closing remove all dynamic details
    present.

    Returns
    -------
    None.

    """
    # main_win.forgot_password.close()
    main_win.forgot_password.lineEdit_2.setText("")
    main_win.forgot_password.lineEdit_3.setText("")
    main_win.forgot_password.lineEdit_4.setText("")


# def closeFailurePage():
#     """
#     Close failure page and before closing remove all dynamic details present.

#     Returns
#     -------
#     None.

#     """
#     failure.close()
#     failure.label_2.setText("")

# def closeSuccessPage():
#     """
#     Close success page and before closing remove all dynamic details present.

#     Returns
#     -------
#     None.

#     """
#     success.close()
#     success.label_2.setText("")


def closeProfilePage():
    """
    Close profile page and before closing remove all dynamic details present.

    Returns
    -------
    None.

    """
    # main_win.profile.close()
    main_win.profile.label_8.setText("")
    main_win.profile.lineEdit.setText("")
    main_win.profile.lineEdit_2.setText("")
    main_win.profile.lineEdit_3.setText("")
    main_win.profile.comboBox.setCurrentIndex(0)
    main_win.profile.textEdit.setPlainText("")
    main_win.profile.label_11.setText("")
    main_win.profile.label_3.setText("")


def closeNewParcelPage():
    """
    Close order parcel page and before closing remove all dynamic details
    present.

    Returns
    -------
    None.

    """
    # main_win.new_parcel.close()
    main_win.new_parcel.comboBox.setCurrentIndex(0)
    main_win.new_parcel.comboBox_2.setCurrentIndex(0)
    main_win.new_parcel.textBrowser.setText("")


def closeMyParcelPage():
    """
    Close my parcels page and before closing remove all dynamic details
    present.

    Returns
    -------
    None.

    """
    # main_win.my_parcel.close()
    main_win.my_parcel.comboBox.clear()
    main_win.my_parcel.label_6.setText("")
    main_win.my_parcel.label_21.setText("")
    main_win.my_parcel.label_20.setText("")
    main_win.my_parcel.textBrowser.setText("")
    main_win.my_parcel.label_18.setText("")
    main_win.my_parcel.label_17.setText("cm -")
    main_win.my_parcel.label_16.setText("cm -")
    main_win.my_parcel.label_15.setText("cm -")
    main_win.my_parcel.label_14.setText("kg -")


def closePickupPage():
    """
    Close pickup page and before closing remove all dynamic details present.

    Returns
    -------
    None.

    """
    # main_win.pickup.close()
    main_win.pickup.lineEdit.setText("")
    main_win.pickup.textEdit.setPlainText("")
    main_win.pickup.doubleSpinBox.setValue(0.00)
    main_win.pickup.doubleSpinBox_2.setValue(0.00)
    main_win.pickup.doubleSpinBox_3.setValue(0.00)
    main_win.pickup.doubleSpinBox_4.setValue(0.00)


def closeDeliverPage():
    """
    Close deliver page and before closing remove all dynamic details present.

    Returns
    -------
    None.

    """
    # main_win.deliver.close()
    main_win.deliver.lineEdit.setText("")
    main_win.deliver.textBrowser.setText("")
    main_win.deliver.textBrowser_2.setText("")
    main_win.deliver.label_9.setText("")
    main_win.deliver.label_10.setText("")
    main_win.deliver.label_11.setText("")
    main_win.deliver.label_12.setText("")
    main_win.deliver.label_15.setText("")


def closeManageRolePage():
    """
    Close manage role page and before closing remove all dynamic details
    present.

    Returns
    -------
    None.

    """
    # main_win.manage_role.close()
    main_win.manage_role.lineEdit.setText("")
    main_win.manage_role.label_3.setText("")
    main_win.manage_role.label_4.setText("")
    main_win.manage_role.label_6.setText("")
    main_win.manage_role.label_7.setText("")


def closeNewCityPage():
    """
    Close new city page and before closing remove all dynamic details
    present.

    Returns
    -------
    None.

    """
    # main_win.new_city.close()
    main_win.new_city.lineEdit.setText("")
    main_win.new_city.comboBox.clear()
    main_win.new_city.label_15.setText("")


def closeNewDepotPage():
    """
    Close new depot page and before closing remove all dynamic details
    present.

    Returns
    -------
    None.

    """
    # main_win.new_depot.close()
    main_win.new_depot.lineEdit.setText("")
    main_win.new_depot.lineEdit_2.setText("")
    main_win.new_depot.textEdit.setText("")
    main_win.new_depot.label_18.setText("")
    main_win.new_depot.label_19.setText("")


def closeAssignManagerPage():
    """
    Close assign manager page and before closing remove all dynamic details
    present.

    Returns
    -------
    None.

    """
    # main_win.assign_manager.close()
    main_win.assign_manager.lineEdit.setText("")
    main_win.assign_manager.lineEdit_2.setText("")
    main_win.assign_manager.label_15.setText("")
    main_win.assign_manager.textBrowser.setPlainText("")


def closeReceivePage():
    """
    Close receive page and before closing remove all dynamic details
    present.

    Returns
    -------
    None.

    """
    # main_win.receive.close()
    main_win.receive.comboBox.clear()
    main_win.receive.lineEdit.setText("")
    main_win.receive.textBrowser.setPlainText("")


def closeTrackParcelPage():
    # main_win.track_parcel.close()
    main_win.track_parcel.comboBox.clear()
    main_win.track_parcel.label_5.setText("")
    main_win.track_parcel.listWidget.clear()


def closeDispatchPage():
    # main_win.dispatch.close()
    main_win.dispatch.comboBox.clear()
    main_win.dispatch.lineEdit.setText("")
    main_win.dispatch.textBrowser.setPlainText("")


#############################   Extra functions   #############################


def travel(openPage, closePage):
    """
    This function helps to move from one page to another.

    Parameters
    ----------
    openPage : str,
        page name you want to open.
    closePage : str,
        page name you want to close.

    Returns
    -------
    None.

    """
    isCloseNeeded = True
    openFunctions = {
        "home": openHomePage,
        "signup": openSignupPage,
        "forgot_password": openForgotPassword,
        "profile": openProfilePage,
        "new_parcel": openNewParcelPage,
        "my_parcel": openMyParcelPage,
        "pickup": openPickupPage,
        "deliver": openDeliverPage,
        "manage_role": openManageRolePage,
        "new_city": openNewCityPage,
        "new_depot": openNewDepotPage,
        "assign_manager": openAssignManagerPage,
        "receive": openReceivePage,
        "track_parcel": openTrackParcelPage,
        "dispatch": openDispatchPage,
    }
    closeFunctions = {
        "home": closeHomePage,
        "signup": closeSignupPage,
        "forgot_password": closeForgotPassword,
        "profile": closeProfilePage,
        "new_parcel": closeNewParcelPage,
        "my_parcel": closeMyParcelPage,
        "pickup": closePickupPage,
        "deliver": closeDeliverPage,
        "manage_role": closeManageRolePage,
        "new_city": closeNewCityPage,
        "new_depot": closeNewDepotPage,
        "assign_manager": closeAssignManagerPage,
        "receive": closeReceivePage,
        "track_parcel": closeTrackParcelPage,
        "dispatch": closeDispatchPage,
    }

    isCloseNeeded = openFunctions[openPage]()
    if isCloseNeeded:
        closeFunctions[closePage]()


def isValidPassword(pwd):
    """
    Checks whether the password meets the following criteria or not
    1. should have 6 to 18 charecters long
    2. should contain atleast 1 uppercase letter
    3. should contain atleast 1 lowercase letter
    4. should contain atleast 1 digit
    5. should contain atleast 1 symbol from @#$&*

    Parameters
    ----------
    pwd : str,
        A string that contains password.

    Returns
    -------
    bool
        Returns True if all conditions are satisfied.

    """
    if len(pwd) >= 6 and len(pwd) <= 18:
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
    """
    Logout an user from the page currently in by setting the current_id and
    current_role to default.

    Parameters
    ----------
    fromPage : str,
        the page from which logout needs to be done.

    Returns
    -------
    None.

    """
    global current_id, current_role

    current_id = ""
    current_role = ""
    travel("home", fromPage)


########################   Functions used in UI pages   ########################


def doSignup():
    """
    Signup a new user by verifying all required data and store the information
    in database. And after completion take the user to profile page by setting
    the current_id and current_role to the required value.

    Returns
    -------
    None.

    """
    global current_id, current_role

    desg = main_win.signup.comboBox.currentText()
    name = main_win.signup.lineEdit.text()

    # verify name
    if len(name) < 3:
        show_message_box(msg_type="error", msg="Name should be atleast 3 characters long")
        return
    for char in name:
        if char.isupper() or char.lower() or char.isspace():
            continue
        else:
            show_message_box(
                msg_type="error",
                msg="Name should contain uppercase, lowercase and spaces only",
            )
            return

    # verify phone number
    phno = main_win.signup.lineEdit_2.text()
    if not phno.isdigit() or len(phno) != 10:
        # check whether the input is a number and must be 10 digit long
        show_message_box(msg_type="error", msg="Phone number should be 10 digits long only")
        return

    # verify password
    pwd = main_win.signup.lineEdit_3.text()
    if not isValidPassword(pwd):
        show_message_box(
            msg_type="error",
            msg=(
                "Invalid Password\n1. password should be 6 - 18 characters "
                "long\n2. password should contain atleast 1 uppercase, 1 "
                "lowercase, 1 digit and 1 symbol from @#$&*"
            ),
        )
        return
    ### --------- Password can be encrypted here

    # veriify address
    address = main_win.signup.textEdit.toPlainText()
    if len(address) < 10:
        show_message_box(msg_type="error", msg="Address should be atleast 10 characters long")
        return

    # print the details if every input is correct
    # print(desg, name, phno, pwd, address)

    # insert the details in database if every input is correct
    conn = sql.connect(DB_FILE)
    query = (
        f"INSERT INTO UserDetail(name, phno, address, desgId) VALUES('{name}', "
        f"{phno}, '{address}', (SELECT id FROM Designation WHERE "
        f"desgType = '{desg}'))"
    )
    try:
        conn.execute(query)
    except sql.IntegrityError:
        show_message_box(msg_type="error", msg="Phone number already registered")
    except Exception as err:
        show_message_box(msg_type="error", msg=str(err))
        return
    else:
        query = "SELECT last_insert_rowid()"
        ret = conn.execute(query)
        userid = ret.fetchall()[0][0]

        query = "INSERT INTO Authentication VALUES((SELECT " f"last_insert_rowid()), '{pwd}', 3)"
        try:
            conn.execute(query)
        except sql.IntegrityError:
            show_message_box(msg_type="error", msg="Phone number already registered")
        except Exception as err:
            show_message_box(msg_type="error", msg=str(err))
            return
        else:
            conn.commit()
    conn.close()

    # if everything goes well... Account is created
    # set the userid as current_id (login process)
    current_id = userid
    current_role = "Customer"
    # open the profile page
    openProfilePage()

    # show the success message
    show_message_box(msg_type="info", msg="Your account has been created")

    closeSignupPage()


def doLogin():
    """
    Verify the authentication details and if verified then set the current_id
    and current_role for further processes and take the user to profile page.

    Returns
    -------
    None.

    """
    global current_id, current_role

    userid = main_win.home.lineEdit.text()
    pwd = main_win.home.lineEdit_2.text()

    if not userid or not pwd:
        show_message_box(msg_type="error", msg="Please provide your credentials")
        return

    conn = sql.connect(DB_FILE)
    query = (
        "SELECT UserRole.role FROM Authentication JOIN UserRole ON "
        f"Authentication.userType = UserRole.id WHERE userId = '{userid}' AND "
        f"password = '{pwd}'"
    )
    ret = conn.execute(query)
    data = ret.fetchall()
    if len(data) == 0:
        # if no row returned then either userid or password
        # or both are incorrect.
        show_message_box(msg_type="error", msg="Invalid UserID or Password")
    else:
        # if correct userid and password entered
        # set the userid as current id (login process)
        current_id = userid
        current_role = data[0][0]
        travel("profile", "home")
    conn.close()


def changePassword():
    phno = main_win.forgot_password.lineEdit_2.text()
    new_pwd = main_win.forgot_password.lineEdit_3.text()
    confirm_pwd = main_win.forgot_password.lineEdit_4.text()

    if phno and new_pwd and confirm_pwd:
        if phno and (not phno.isdigit() or len(phno) != 10):
            # check whether the input is a number and must be 10 digit long
            show_message_box(
                msg_type="error",
                msg="Phone number should be 10 digits long only",
            )
            return

        if new_pwd == confirm_pwd:
            if isValidPassword(new_pwd):
                conn = sql.connect(DB_FILE)
                query = f"SELECT id FROM UserDetail WHERE phno = '{phno}'"
                ret = conn.execute(query)
                data = ret.fetchall()
                if data:
                    user_id = data[0][0]
                    query = f"UPDATE Authentication SET password = '{new_pwd}' " f"WHERE userId = '{user_id}'"
                    conn.execute(query)
                    conn.commit()

                    travel("home", "forgot_password")

                    show_message_box(msg_type="info", msg="Your password has been updated")
                else:
                    show_message_box(
                        msg_type="error",
                        msg="Sorry user not found; please try again",
                    )
                conn.close()
            else:
                show_message_box(
                    msg_type="error",
                    msg=(
                        "Invalid Password\n1. password should be 6 - 18 "
                        "characters long\n2. password should contain atleast 1 "
                        "uppercase, 1 lowercase, 1 digit and 1 symbol from "
                        "@#$&*"
                    ),
                )
        else:
            show_message_box(
                msg_type="error",
                msg="New password and Confirm password are not matching",
            )
    else:
        show_message_box(msg_type="error", msg="Please provide the proper informations")


def modifyProfile():
    """
    Update user's profile with the new data given by user. And complete the
    update by verifying all required data given by user.

    Returns
    -------
    None.

    """
    name = main_win.profile.lineEdit.text()
    if len(name) < 3:
        show_message_box(msg_type="error", msg="Name should be atleast 3 characters long")
        return

    for char in name:
        if char.isupper() or char.lower() or char.isspace():
            continue
        else:
            show_message_box(
                msg_type="error",
                msg="Name should contain uppercase, lowercase and spaces only",
            )
            return

    phone = main_win.profile.lineEdit_2.text()
    if not phone.isdigit() or len(phone) != 10:
        # check whether the input is a number and must be 10 digit long
        show_message_box(msg_type="error", msg="Phone number should be 10 digits long only")
        return

    pwd = main_win.profile.lineEdit_3.text()
    if not isValidPassword(pwd):
        show_message_box(
            msg_type="error",
            msg=(
                "Invalid Password\n1. password should be 6 - 18 characters long"
                "\n2. password should contain atleast 1 uppercase, 1 lowercase,"
                " 1 digit and 1 symbol from @#$&*"
            ),
        )
        return

    desg = main_win.profile.comboBox.currentText()
    address = main_win.profile.textEdit.toPlainText()
    if len(address) < 10:
        show_message_box(msg_type="error", msg="Address should be atleast 10 characters long")
        return

    conn = sql.connect(DB_FILE)
    query = (
        "SELECT UserDetail.id, name, phno, address, desgType, password, "
        "role FROM UserDetail JOIN Designation JOIN Authentication JOIN "
        "UserRole ON (UserDetail.desgId = Designation.id AND UserDetail.id = "
        "Authentication.userId AND Authentication.userType = UserRole.id) "
        f"WHERE UserDetail.id = {current_id}"
    )
    ret = conn.execute(query)
    data = ret.fetchall()[0]
    query = ["UPDATE UserDetail SET "]
    if data[1] != name:
        query.append(f"name='{name}'")
    if str(data[2]) != phone:
        query.append((", " if len(query) > 1 else "") + f"phno={phone}")
    if data[3] != address:
        query.append((", " if len(query) > 1 else "") + f"address='{address}'")
    if data[4] != desg:
        query.append((", " if len(query) > 1 else "") + f"desgId=(SELECT id FROM Designation WHERE desgType='{desg}')")
    query.append(f" WHERE id={current_id}")
    try:
        if len(query) > 2 or data[5] != pwd:
            # there is some thing to edit
            if len(query) > 2:
                query = "".join(query)
                conn.execute(query)
            if data[5] != pwd:
                pwd_query = f"UPDATE Authentication SET password='{pwd}' " f"WHERE userId={current_id}"
                conn.execute(pwd_query)
        else:
            show_message_box(msg_type="error", msg="No changes to save")
            conn.close()
            return
    except sql.IntegrityError as err:
        if "UserDetail.phno" in str(err):
            show_message_box(msg_type="error", msg="Phone number already exist")
        else:
            show_message_box(msg_type="error", msg=f"Unable to modify because \n{err}")
    except Exception as err:
        show_message_box(msg_type="error", msg=f"Unable to modify because \n{err}")
        return
    else:
        show_message_box(msg_type="info", msg="Your profile has been updated")
        conn.commit()
    conn.close()

    closeProfilePage()
    openProfilePage()  # it will show the updated data


def placeOrder():
    """
    Order a new parcel for the user.

    Returns
    -------
    None.

    """
    pay = main_win.new_parcel.comboBox.currentText()
    category = main_win.new_parcel.comboBox_2.currentText()

    if not pay and not category:
        show_message_box(msg_type="error", msg="Please provide all required informations")
        return

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    conn = sql.connect(DB_FILE)
    query = (
        "INSERT INTO Parcel(paymentType, productType, deliverTo, datetime) "
        f"VALUES((SELECT id FROM paymentType WHERE payType='{pay}'),"
        f"(SELECT id FROM ProductCategory WHERE productType='{category}'), "
        f"{current_id}, '{now}')"
    )
    try:
        conn.execute(query)
        conn.commit()
    except Exception as err:
        show_message_box(msg_type="error", msg=f"Unable to place order because \n{err}")
    else:
        query = """SELECT last_insert_rowid()"""
        ret = conn.execute(query)
        orderid = ret.fetchall()[0][0]
        show_message_box(msg_type="info", msg=f"Order placed \nYour order id is {orderid}")
    conn.close()


def checkParcelDetails():
    """
    Check the details for a given parcel id.

    Returns
    -------
    None.

    """
    parcelid = main_win.my_parcel.comboBox.currentText()
    if not parcelid.isdigit():
        show_message_box(msg_type="error", msg="Please select a valid parcel ID")
        return
    conn = sql.connect(DB_FILE)
    query = (
        "SELECT Parcel.id, PaymentType.payType, weight, length, breadth, "
        "height, ProductCategory.productType, Designation.desgType, "
        "UserDetail.name, UserDetail.address, datetime FROM Parcel "
        "JOIN PaymentType JOIN ProductCategory JOIN UserDetail "
        "JOIN Designation ON (Parcel.paymentType = PaymentType.id "
        "AND Parcel.productType = ProductCategory.id "
        "AND Parcel.deliverTo = UserDetail.id "
        f"AND UserDetail.desgId = Designation.id) WHERE Parcel.id = {parcelid} "
        "ORDER BY Parcel.id DESC"
    )
    ret = conn.execute(query)
    row = ret.fetchall()
    if row:
        row = row[0]
        main_win.my_parcel.label_6.setText(str(row[0]))
        main_win.my_parcel.label_21.setText(row[1])
        main_win.my_parcel.label_14.setText("Kgs - " + str(row[2]))
        main_win.my_parcel.label_15.setText("cm - " + str(row[3]))
        main_win.my_parcel.label_16.setText("cm - " + str(row[4]))
        main_win.my_parcel.label_17.setText("cm - " + str(row[5]))
        main_win.my_parcel.label_18.setText(row[6])
        main_win.my_parcel.label_20.setText(row[10][:10])
        main_win.my_parcel.textBrowser.setText("To: " + row[7] + " " + row[8] + "\n\n" + row[9])
    conn.close()


def completePickup():
    """
    Pickup can only be done by agents. Before picking up any order just verify
    its last status; if no last status found an order can be picked up. Also
    update the action in ParcelActionTaken table.

    Returns
    -------
    None.

    """
    parcelid = main_win.pickup.lineEdit.text()
    weight = main_win.pickup.doubleSpinBox.text()
    weight = "" if weight == "0.00" else weight
    length = main_win.pickup.doubleSpinBox_2.text()
    length = "" if length == "0.00" else length
    breadth = main_win.pickup.doubleSpinBox_3.text()
    breadth = "" if breadth == "0.00" else breadth
    height = main_win.pickup.doubleSpinBox_4.text()
    height = "" if height == "0.00" else height
    ret_loc = main_win.pickup.textEdit.toPlainText()
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    if not all(list(map(lambda x: bool(x), [parcelid, weight, length, breadth, ret_loc]))):
        show_message_box(
            msg_type="error",
            msg="Insufficient information; Please provide all informations",
        )
        return

    conn = sql.connect(DB_FILE)
    query = f"SELECT * FROM ParcelActionTaken WHERE parcelId = {parcelid}"
    ret = conn.execute(query)
    data = ret.fetchall()
    if data:
        show_message_box(msg_type="error", msg="Parcel is already pickedup")
        conn.close()
        return
    query = (
        f"UPDATE Parcel SET weight= {weight}, length= {length}, "
        f"breadth= {breadth}, height= {height} WHERE id={parcelid}"
    )
    try:
        conn.execute(query)
    except Exception as err:
        show_message_box(msg_type="error", msg=f"Unable to pickup order because \n{err}")
        return
    else:
        query = (
            "INSERT INTO ParcelActionTaken ('parcelId', 'actionId', "
            f"'datetime') VALUES({parcelid}, (SELECT id FROM ParcelAction "
            f"WHERE action = 'Picked up'), '{now}')"
        )
        try:
            conn.execute(query)
        except Exception as err:
            show_message_box(msg_type="error", msg=f"Unable to pickup order because \n{err}")
            return
        else:
            query = (
                f"INSERT INTO Pickup ('agentId', 'parcelId', 'location', "
                f"'datetime') VALUES({current_id}, {parcelid}, '{ret_loc}', "
                f"'{now}')"
            )
            try:
                conn.execute(query)
            except Exception as err:
                show_message_box(
                    msg_type="error",
                    msg=f"Unable to pickup order because \n{err}",
                )
                return
            else:
                conn.commit()
                show_message_box(msg_type="info", msg="The order has been picked up")
    conn.close()
    closePickupPage()


def checkBeforeDeliver():
    """
    Before delivery check the parcel details.

    Returns
    -------
    None.

    """
    parcelid = main_win.deliver.lineEdit.text()
    if not parcelid:
        show_message_box(msg_type="error", msg="Please provide the parcel Id")
        return

    conn = sql.connect(DB_FILE)
    query = f"SELECT * FROM ParcelActionTaken WHERE parcelId = {parcelid}"
    ret = conn.execute(query)
    data = ret.fetchall()
    if len(data) != 0:
        if data[0][2] != 1 and data[0][2] != 2:
            show_message_box(
                msg_type="error",
                msg="The parcel has already delivered or returned",
            )
            conn.close()
            return
    else:
        show_message_box(msg_type="error", msg="The parcel has not yet picked up")
        conn.close()
        return

    query = (
        "SELECT PaymentType.payType, weight, length, breadth, height, "
        "Designation.desgType, UserDetail.name, UserDetail.address, "
        "UserDetail.phno, Pickup.location FROM Parcel JOIN PaymentType "
        "JOIN UserDetail JOIN Designation JOIN Pickup ON ("
        "Parcel.paymentType = PaymentType.id "
        "AND Parcel.deliverTo = UserDetail.id "
        "AND UserDetail.desgId = Designation.id AND Parcel.id = Pickup.parcelId"
        f") WHERE Parcel.id = {parcelid}"
    )
    ret = conn.execute(query)
    data = ret.fetchall()[0]
    main_win.deliver.label_15.setText(data[0])
    main_win.deliver.label_9.setText(f"{data[1]} Kg")
    main_win.deliver.label_10.setText(f"{data[2]} cm")
    main_win.deliver.label_11.setText(f"{data[3]} cm")
    main_win.deliver.label_12.setText(f"{data[4]} cm")
    address = f"To: {data[5]} {data[6]}\n\n{data[7]}\n Phone: {data[8]}"
    main_win.deliver.textBrowser.setText(address)
    main_win.deliver.textBrowser_2.setText(data[9])
    conn.close()


def completeDeliver():
    """
    Deliver the parcel to user and update the action ParcelActionTaken table.

    Returns
    -------
    None.

    """
    parcelid = main_win.deliver.lineEdit.text()
    if not parcelid:
        show_message_box(msg_type="error", msg="Please provide the parcel Id")
        return

    conn = sql.connect(DB_FILE)
    query = f"SELECT * FROM ParcelActionTaken WHERE parcelId = {parcelid}"
    ret = conn.execute(query)
    data = ret.fetchall()
    if len(data) != 0:
        if data[0][2] != 1 and data[0][2] != 2:
            show_message_box(
                msg_type="error",
                msg="The parcel has already delivered or returned",
            )
            conn.close()
            return
    else:
        show_message_box(msg_type="error", msg="The parcel has not yet picked up")
        conn.close()
        return

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    query = (
        f"INSERT INTO Delivery VALUES({current_id}, (SELECT deliverTo "
        f"FROM Parcel WHERE id = {parcelid}), {parcelid}, '{now}')"
    )
    try:
        conn.execute(query)
    except Exception as err:
        show_message_box(msg_type="error", msg=f"Unable to deliver order because \n{err}")
        return
    else:
        query = (
            "UPDATE ParcelActionTaken SET actionId = (SELECT id "
            f"FROM ParcelAction WHERE action = 'Delivered'), datetime = '{now}' "
            f"WHERE parcelId = {parcelid}"
        )
        try:
            conn.execute(query)
        except Exception as err:
            show_message_box(msg_type="error", msg=f"Unable to deliver order because \n{err}")
            return
        else:
            conn.commit()
            conn.close()
            show_message_box(msg_type="info", msg="Parcel has been delivered")
            closeDeliverPage()


def completeReturn():
    """
    Agent can also return the package if can't be delivered to the customer

    Returns
    -------
    None.

    """
    parcelid = main_win.deliver.lineEdit.text()
    if not parcelid:
        show_message_box(msg_type="error", msg="Please provide the parcel Id")
        return

    conn = sql.connect(DB_FILE)
    query = f"SELECT * FROM ParcelActionTaken WHERE parcelId = {parcelid}"
    ret = conn.execute(query)
    data = ret.fetchall()
    if len(data) != 0:
        if data[0][2] != 1 and data[0][2] != 2:
            show_message_box(
                msg_type="error",
                msg="The parcel has already delivered or returned",
            )
            conn.close()
            return
    else:
        show_message_box(msg_type="error", msg="The parcel has not yet picked up")
        conn.close()
        return

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    query = (
        "UPDATE ParcelActionTaken SET actionId = (SELECT id FROM ParcelAction "
        f"WHERE action = 'Returned'), datetime = '{now}' "
        f"WHERE parcelId = {parcelid}"
    )
    try:
        conn.execute(query)
    except Exception as err:
        show_message_box(msg_type="error", msg=f"Unable to return order because \n{err}")
        return
    else:
        conn.commit()
        conn.close()
        show_message_box(msg_type="info", msg="Parcel has been returned")
        closeDeliverPage()


def findUserForMangeRole():
    """
    Check the user info before changing the role. This function will display
    some of the userdetails in manage role page.

    Returns
    -------
    None.

    """
    userid = main_win.manage_role.lineEdit.text()

    if not userid:
        show_message_box(msg_type="error", msg="Please provide user ID")
        return

    conn = sql.connect(DB_FILE)
    query = (
        "SELECT UserDetail.id, Designation.desgType, name, phno, role "
        "FROM UserDetail JOIN Designation JOIN Authentication JOIN UserRole "
        "ON (UserDetail.desgId = Designation.id "
        "AND UserDetail.id = Authentication.userId "
        "AND Authentication.userType = UserRole.id) "
        f"WHERE UserDetail.id = {userid}"
    )
    ret = conn.execute(query)
    data = ret.fetchall()
    if len(data) != 0:
        main_win.manage_role.label_3.setText(str(data[0][0]))
        main_win.manage_role.label_4.setText(data[0][1] + " " + data[0][2])
        main_win.manage_role.label_6.setText(str(data[0][3]))
        main_win.manage_role.label_7.setText(data[0][4])
    else:
        show_message_box(msg_type="error", msg="No User found for this user Id")
    conn.close()


def assignRole():
    """
    Assign the selected role to the selected user.

    Returns
    -------
    None.

    """
    userid = main_win.manage_role.label_3.text()
    role = main_win.manage_role.comboBox.currentText()
    if not userid.isdigit():
        show_message_box(msg_type="error", msg="Check the user details first")
        return

    if not userid and not role:
        show_message_box(msg_type="error", msg="Please provide all information")
        return

    conn = sql.connect(DB_FILE)
    query = (
        "UPDATE Authentication SET userType = (SELECT id FROM UserRole "
        f"WHERE role = '{role}') WHERE userId = {userid}"
    )
    try:
        conn.execute(query)
        conn.commit()
        show_message_box(msg_type="info", msg="New role has been assigned to the user")
    except Exception as err:
        show_message_box(msg_type="error", msg=f"Unable to assign role because \n{err}")
    else:
        closeManageRolePage()
    conn.close()


def expandCity():
    city_name = main_win.new_city.lineEdit.text()
    if len(city_name) < 3:
        show_message_box(
            msg_type="error",
            msg="City name should be atleast 3 characters long",
        )
        return
    else:
        conn = sql.connect(DB_FILE)
        query = f"INSERT INTO City(name) VALUES('{city_name}')"
        try:
            conn.execute(query)
        except sql.IntegrityError:
            show_message_box(msg_type="error", msg="City already exist")
        except Exception as err:
            show_message_box(msg_type="error", msg=f"Unable to assign role because \n{err}")
        else:
            conn.commit()
            closeNewCityPage()
            openNewCityPage()
            show_message_box(msg_type="info", msg="You have expanded to a new city")
        conn.close()


def searchCity():
    city_name = main_win.new_city.comboBox.currentText()
    if not city_name:
        show_message_box(msg_type="error", msg="Please select one city")
        return
    else:
        conn = sql.connect(DB_FILE)
        query = f"SELECT id FROM City WHERE name='{city_name}'"
        ret = conn.execute(query)
        cityid = ret.fetchall()[0][0]
        main_win.new_city.label_15.setText(str(cityid))
        show_message_box(msg_type="info", msg=f"City id for {city_name} is {cityid}")
        conn.close()


def findCity():
    cityid = main_win.new_depot.lineEdit.text()
    if len(cityid) != 3:
        show_message_box(msg_type="error", msg="3 digit cityid required")
        return
    else:
        conn = sql.connect(DB_FILE)
        query = f"SELECT name FROM City WHERE id={cityid}"
        ret = conn.execute(query)
        data = ret.fetchall()
        if len(data) == 0:
            show_message_box(msg_type="error", msg="No city found for given cityid")
            return
        else:
            main_win.new_depot.label_18.setText(data[0][0])
        conn.close()


def findManager():
    managerid = main_win.new_depot.lineEdit_2.text()
    if len(managerid) != 6:
        show_message_box(msg_type="error", msg="6 digit manager id required")
        return
    else:
        conn = sql.connect(DB_FILE)
        query = (
            "SELECT UserDetail.name FROM Authentication JOIN UserDetail "
            f"ON UserDetail.id = Authentication.userId "
            f"WHERE userId={managerid} AND userType=4"
        )
        ret = conn.execute(query)
        data = ret.fetchall()
        if len(data) == 0:
            show_message_box(msg_type="error", msg="No manager found for given manager ID")
            return
        else:
            main_win.new_depot.label_19.setText(data[0][0])
        conn.close()


def inaugurateDepot():
    cityid = main_win.new_depot.lineEdit.text()
    city_name = main_win.new_depot.label_18.text()
    if not city_name:
        show_message_box(msg_type="error", msg="Check the city name")
        return
    managerid = main_win.new_depot.lineEdit_2.text()
    manager_name = main_win.new_depot.label_19.text()
    if not manager_name:
        show_message_box(msg_type="error", msg="Check the manager name")
        return
    address = main_win.new_depot.textEdit.toPlainText()

    conn = sql.connect(DB_FILE)
    query = f"INSERT INTO Depot(cityId, manager, address) VALUES({cityid}, " f"{managerid}, '{address}')"
    try:
        conn.execute(query)
    except Exception as err:
        show_message_box(msg_type="error", msg=f"Unable to inaugurate because \n{err}")
    else:
        conn.commit()
        show_message_box(msg_type="info", msg="You have setup a new depot")
        closeNewCityPage()
    conn.close()


def getDepotDetails():
    depotid = main_win.assign_manager.lineEdit.text()
    if len(depotid) != 3 and not depotid.isdigit():
        show_message_box(msg_type="error", msg="Please provide a valid depot ID")
        return

    conn = sql.connect(DB_FILE)
    query = (
        "SELECT Depot.address, City.name, UserDetail.name FROM Depot "
        "JOIN City JOIN UserDetail ON (City.id = Depot.cityId "
        f"AND UserDetail.id = Depot.manager) WHERE Depot.id = {depotid}"
    )
    ret = conn.execute(query)
    data = ret.fetchall()[0]
    main_win.assign_manager.textBrowser.setText(data[0])
    main_win.assign_manager.label_16.setText(data[1])
    main_win.assign_manager.label_15.setText(data[2])
    conn.close()


def assignManager():
    depotid = main_win.assign_manager.lineEdit.text()
    managerid = main_win.assign_manager.lineEdit_2.text()

    if len(managerid) != 6:
        show_message_box(msg_type="error", msg="Manager ID required")
        return
    else:
        conn = sql.connect(DB_FILE)
        query = (
            "SELECT UserDetail.name FROM Authentication JOIN UserDetail "
            f"ON UserDetail.id = Authentication.userId WHERE userId={managerid}"
            " AND userType=4"
        )
        ret = conn.execute(query)
        data = ret.fetchall()
        if len(data) == 0:
            show_message_box(msg_type="error", msg="No manager found for given manager ID")
            conn.close()
            return
        else:
            query = f"UPDATE Depot SET manager = {managerid} " f"WHERE id = {depotid}"
            try:
                conn.execute(query)
            except Exception as err:
                show_message_box(
                    msg_type="error",
                    msg=f"Unable to inaugurate because \n{err}",
                )
            else:
                conn.commit()
                show_message_box(msg_type="info", msg="New manager has been assigned")
        conn.close()
        closeAssignManagerPage()


def getDepotDetailsForRecieve():
    depot_id = main_win.receive.comboBox.currentText()
    if len(depot_id) != 3 and not depot_id.isdigit():
        show_message_box(msg_type="error", msg="Please provide a valid depot ID")
        return

    conn = sql.connect(DB_FILE)
    query = (
        "SELECT Depot.address, City.name, UserDetail.name FROM Depot "
        "JOIN City JOIN UserDetail ON (City.id = Depot.cityId "
        f"AND UserDetail.id = Depot.manager) WHERE Depot.id = {depot_id}"
    )
    ret = conn.execute(query)
    data = ret.fetchall()[0]
    main_win.receive.textBrowser.setText(f"{data[0]}\n\n{data[1]}")
    conn.close()


def recieveParcel():
    parcel_id = main_win.receive.lineEdit.text()
    if not parcel_id:
        show_message_box(msg_type="error", msg="Please provide parcel ID")
        return

    depot_address = main_win.receive.textBrowser.toPlainText()
    if not depot_address:
        show_message_box(msg_type="error", msg="Please check the depot address first")
        return

    depot_id = main_win.receive.comboBox.currentText()
    if len(depot_id) != 3 and not depot_id.isdigit():
        show_message_box(msg_type="error", msg="Please provide a valid depot ID")
        return

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    conn = sql.connect(DB_FILE)
    query = f"SELECT parcelId FROM Delivery WHERE parcelId={parcel_id}"
    ret = conn.execute(query)
    data = ret.fetchall()
    if data:
        show_message_box(msg_type="error", msg="This parcel is already delivered")
        conn.close()
        return

    query = f"SELECT parcelId FROM Pickup WHERE parcelId={parcel_id}"
    ret = conn.execute(query)
    data = ret.fetchall()
    if not data:
        show_message_box(msg_type="error", msg="This parcel is not yet picked")
        conn.close()
        return

    query = (
        f"SELECT type, depotId FROM ParcelLocation JOIN ShipmentType "
        "ON ParcelLocation.shipType=ShipmentType.id "
        f"WHERE parcelId={parcel_id} ORDER BY ParcelLocation.id DESC"
    )
    ret = conn.execute(query)
    data = ret.fetchall()
    if data:
        # continue only if parcel is only picked up (no data returned from the
        # above query) or if parcel is already dispatched from last location
        data = data[0]
        if str(data[1]) == depot_id:
            show_message_box(msg_type="error", msg="This parcel is already received")
            conn.close()
            return
        elif data[0] == "Received":
            show_message_box(
                msg_type="error",
                msg="This parcel is not yet dispatched from last location",
            )
            conn.close()
            return

    # conn = sql.connect(DB_FILE)
    query = (
        "INSERT INTO ParcelLocation ('parcelId', 'depotId', 'shipType', "
        f"'datetime') VALUES({parcel_id}, {depot_id}, (SELECT id "
        f"FROM ShipmentType WHERE type='Received'), '{now}')"
    )
    try:
        conn.execute(query)
        conn.commit()
    except Exception as err:
        show_message_box(msg_type="error", msg=f"Unable to recieve parcel due to \n{err}")
    else:
        show_message_box(msg_type="info", msg="Parcel received at depot")
        closeReceivePage()
        openDispatchPage()
    conn.close()


def getDepotDetailsForDispatch():
    depot_id = main_win.dispatch.comboBox.currentText()
    if len(depot_id) != 3 and not depot_id.isdigit():
        show_message_box(msg_type="error", msg="Please provide a valid depot ID")
        return

    conn = sql.connect(DB_FILE)
    query = (
        "SELECT Depot.address, City.name, UserDetail.name FROM Depot "
        "JOIN City JOIN UserDetail ON (City.id = Depot.cityId "
        f"AND UserDetail.id = Depot.manager) WHERE Depot.id = {depot_id}"
    )
    ret = conn.execute(query)
    data = ret.fetchall()[0]
    main_win.dispatch.textBrowser.setText(f"{data[0]}\n\n{data[1]}")
    conn.close()


def dispatchParcel():
    parcel_id = main_win.dispatch.lineEdit.text()
    if not parcel_id:
        show_message_box(msg_type="error", msg="Please provide parcel ID")
        return

    depot_address = main_win.dispatch.textBrowser.toPlainText()
    if not depot_address:
        show_message_box(msg_type="error", msg="Please check the depot address first")
        return

    depot_id = main_win.dispatch.comboBox.currentText()
    if len(depot_id) != 3 and not depot_id.isdigit():
        show_message_box(msg_type="error", msg="Please provide a valid depot ID")
        return

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    conn = sql.connect(DB_FILE)
    query = (
        f"SELECT type, depotId FROM ParcelLocation JOIN ShipmentType "
        "ON ParcelLocation.shipType=ShipmentType.id "
        f"WHERE parcelId={parcel_id} AND depotId={depot_id} "
        "ORDER BY ParcelLocation.id DESC"
    )
    ret = conn.execute(query)
    data = ret.fetchall()
    if not data:
        show_message_box(msg_type="error", msg="The parcel is not yet received")
        conn.close()
        return

    else:
        data = data[0]
        if data[0] == "Dispatched":
            show_message_box(msg_type="error", msg="The parcel is already dispatched")
            conn.close()
            return

    query = (
        "INSERT INTO ParcelLocation ('parcelId', 'depotId', 'shipType', "
        f"'datetime') VALUES({parcel_id}, {depot_id}, (SELECT id "
        f"FROM ShipmentType WHERE type='Dispatched'), '{now}')"
    )
    try:
        conn.execute(query)
        conn.commit()
    except Exception as err:
        show_message_box(msg_type="error", msg=f"Unable to recieve parcel due to \n{err}")
    else:
        show_message_box(msg_type="info", msg="Parcel disptached from depot")
        closeDispatchPage()
        openDispatchPage()
    conn.close()


def showTrackingDetails():
    parcel_id = main_win.track_parcel.comboBox.currentText()

    if not parcel_id:
        show_message_box(msg_type="error", msg="Please provide parcel ID")
        return

    main_win.track_parcel.label_5.setText("")
    main_win.track_parcel.listWidget.clear()

    details = []
    conn = sql.connect(DB_FILE)
    query = f"SELECT location, datetime FROM Pickup WHERE parcelId={parcel_id}"
    ret = conn.execute(query)
    data = ret.fetchall()
    if not data:
        main_win.track_parcel.label_5.setText("Parcel not yet picked")
        conn.close()
        return
    else:
        data = data[0]
        timestamp = datetime.strptime(data[1], "%d-%m-%Y %H:%M:%S").strftime("%d-%b-%Y")
        details.append(f"{timestamp}: Parcel picked up")

        query = (
            "SELECT ParcelLocation.datetime, ShipmentType.type, City.name "
            "FROM ParcelLocation JOIN ShipmentType "
            "ON ParcelLocation.shipType=ShipmentType.id "
            "JOIN Depot ON ParcelLocation.depotId=Depot.id "
            "JOIN City ON Depot.cityId=City.id "
            f"WHERE parcelId={parcel_id} ORDER BY ParcelLocation.id ASC"
        )
        ret = conn.execute(query)
        data = ret.fetchall()
        if data:
            for row in data:
                timestamp = datetime.strptime(row[0], "%d-%m-%Y %H:%M:%S").strftime("%d-%b-%Y")
                transit_mode = "dispatched from" if row[1].lower() == "dispatched" else "received at"
                details.append(f"{timestamp}: Parcel {transit_mode} {row[2]}")

        query = f"SELECT datetime FROM Delivery WHERE parcelId={parcel_id}"
        ret = conn.execute(query)
        data = ret.fetchall()
        if data:
            data = data[0]
            timestamp = datetime.strptime(data[0], "%d-%m-%Y %H:%M:%S").strftime("%d-%b-%Y")
            details.append(f"{timestamp}: Parcel delivered")
        else:
            query = (
                "SELECT actionId, datetime FROM ParcelActionTaken "
                f"WHERE parcelId={parcel_id} AND actionId=(SELECT id FROM "
                f"ParcelAction WHERE action='Returned')"
            )
            ret = conn.execute(query)
            data = ret.fetchall()
            if data:
                data = data[0]
                timestamp = datetime.strptime(data[1], "%d-%m-%Y %H:%M:%S").strftime("%d-%b-%Y")
                details.append(f"{timestamp}: Parcel returned")

        details.reverse()
        for idx, detail in enumerate(details):
            if "Parcel picked up" in detail:
                detail = "📦" + detail
            elif "Parcel delivered" in detail:
                detail = "🏁" + detail
            elif "Parcel returned" in detail:
                detail = "❌" + detail
            else:
                detail = ("👁️‍🗨️" if idx == 0 else "🔽") + detail
            main_win.track_parcel.listWidget.addItem(QListWidgetItem(detail))
    conn.close()


###############################   Main Program   ##############################

if __name__ == "__main__":
    # try:
    # if hasattr(QtCore.Qt, 'AA_EnableHighDepiScaling'):
    #     QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    # if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    #     QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    # create or ignore database
    create_or_ignore_db()

    # create the application
    app = QApplication([])

    # https://stackoverflow.com/questions/67599432/setting-the-same-icon-as-application-icon-in-task-bar-for-pyqt5-application
    MY_APP_ID = "cttc.pms.v0.1.0"  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MY_APP_ID)

    # Get the screen resoultion, height & width for responsiveness
    # screen_resolution = app.desktop().screenGeometry()
    # SCREEN_WIDTH = screen_resolution.width()
    # SCREEN_HEIGHT = screen_resolution.height()

    # Set the app resizing methods for responsiveness
    # QtWidgets.QMainWindow.resizeEvent = resize_event
    # QtWidgets.QMainWindow.window_name = window_name

    main_win = MainWindow()
    main_win.setWindowIcon(QIcon("assets/images/PMS logo.png"))
    main_win.show()

    # show the home page initially
    # main_win.home.show()

    # create listeners
    ### home page buttons
    main_win.home.pushButton.clicked.connect(partial(travel, "forgot_password", "home"))
    main_win.home.pushButton_2.clicked.connect(doLogin)
    main_win.home.pushButton_3.clicked.connect(partial(travel, "signup", "home"))

    ### sigup page buttons
    main_win.signup.pushButton.clicked.connect(partial(travel, "home", "signup"))
    main_win.signup.pushButton_2.clicked.connect(doSignup)

    ### forgot_password page buttons
    main_win.forgot_password.pushButton.clicked.connect(partial(travel, "home", "forgot_password"))
    main_win.forgot_password.pushButton_2.clicked.connect(changePassword)

    # ### failure page buttons
    # main_win.failure.pushButton.clicked.connect(closeFailurePage)

    # ### success page buttons
    # main_win.success.pushButton.clicked.connect(closeSuccessPage)

    ### profile page buttons
    main_win.profile.pushButton_2.clicked.connect(partial(travel, "new_parcel", "profile"))
    main_win.profile.pushButton_3.clicked.connect(partial(travel, "pickup", "profile"))
    main_win.profile.pushButton_4.clicked.connect(partial(travel, "receive", "profile"))
    main_win.profile.pushButton_5.clicked.connect(partial(travel, "manage_role", "profile"))
    main_win.profile.pushButton_6.clicked.connect(modifyProfile)
    main_win.profile.pushButton_7.clicked.connect(partial(doLogout, "profile"))

    ### new_parcel page buttons
    main_win.new_parcel.pushButton.clicked.connect(partial(travel, "profile", "new_parcel"))
    main_win.new_parcel.pushButton_3.clicked.connect(partial(travel, "pickup", "new_parcel"))
    main_win.new_parcel.pushButton_4.clicked.connect(partial(travel, "receive", "new_parcel"))
    main_win.new_parcel.pushButton_5.clicked.connect(partial(travel, "manage_role", "new_parcel"))
    main_win.new_parcel.pushButton_6.clicked.connect(placeOrder)
    main_win.new_parcel.pushButton_7.clicked.connect(partial(doLogout, "new_parcel"))
    main_win.new_parcel.pushButton_9.clicked.connect(partial(travel, "my_parcel", "new_parcel"))
    main_win.new_parcel.pushButton_10.clicked.connect(partial(travel, "track_parcel", "new_parcel"))

    ### my_parcel page buttons
    main_win.my_parcel.pushButton.clicked.connect(partial(travel, "profile", "my_parcel"))
    main_win.my_parcel.pushButton_3.clicked.connect(partial(travel, "pickup", "my_parcel"))
    main_win.my_parcel.pushButton_4.clicked.connect(partial(travel, "receive", "my_parcel"))
    main_win.my_parcel.pushButton_5.clicked.connect(partial(travel, "manage_role", "my_parcel"))
    main_win.my_parcel.pushButton_6.clicked.connect(checkParcelDetails)
    main_win.my_parcel.pushButton_7.clicked.connect(partial(doLogout, "my_parcel"))
    main_win.my_parcel.pushButton_8.clicked.connect(partial(travel, "new_parcel", "my_parcel"))
    main_win.my_parcel.pushButton_10.clicked.connect(partial(travel, "track_parcel", "my_parcel"))

    ### pickup page buttons
    main_win.pickup.pushButton.clicked.connect(partial(travel, "profile", "pickup"))
    main_win.pickup.pushButton_2.clicked.connect(partial(travel, "new_parcel", "pickup"))
    main_win.pickup.pushButton_4.clicked.connect(partial(travel, "receive", "pickup"))
    main_win.pickup.pushButton_5.clicked.connect(partial(travel, "manage_role", "pickup"))
    main_win.pickup.pushButton_6.clicked.connect(completePickup)
    main_win.pickup.pushButton_7.clicked.connect(partial(doLogout, "pickup"))
    main_win.pickup.pushButton_9.clicked.connect(partial(travel, "deliver", "pickup"))

    ### deliver page buttons
    main_win.deliver.pushButton.clicked.connect(partial(travel, "profile", "deliver"))
    main_win.deliver.pushButton_2.clicked.connect(partial(travel, "new_parcel", "deliver"))
    main_win.deliver.pushButton_4.clicked.connect(partial(travel, "receive", "deliver"))
    main_win.deliver.pushButton_5.clicked.connect(partial(travel, "manage_role", "deliver"))
    main_win.deliver.pushButton_6.clicked.connect(checkBeforeDeliver)
    main_win.deliver.pushButton_7.clicked.connect(partial(doLogout, "deliver"))
    main_win.deliver.pushButton_8.clicked.connect(partial(travel, "pickup", "deliver"))
    main_win.deliver.pushButton_10.clicked.connect(completeDeliver)
    main_win.deliver.pushButton_11.clicked.connect(completeReturn)

    ### manage_role page buttons
    main_win.manage_role.pushButton.clicked.connect(partial(travel, "profile", "manage_role"))
    main_win.manage_role.pushButton_2.clicked.connect(partial(travel, "new_parcel", "manage_role"))
    main_win.manage_role.pushButton_3.clicked.connect(partial(travel, "pickup", "manage_role"))
    main_win.manage_role.pushButton_4.clicked.connect(partial(travel, "receive", "manage_role"))
    main_win.manage_role.pushButton_6.clicked.connect(findUserForMangeRole)
    main_win.manage_role.pushButton_7.clicked.connect(partial(doLogout, "manage_role"))
    main_win.manage_role.pushButton_9.clicked.connect(partial(travel, "assign_manager", "manage_role"))
    main_win.manage_role.pushButton_10.clicked.connect(assignRole)
    main_win.manage_role.pushButton_11.clicked.connect(partial(travel, "new_city", "manage_role"))
    main_win.manage_role.pushButton_12.clicked.connect(partial(travel, "new_depot", "manage_role"))

    ### new_city page buttons
    main_win.new_city.pushButton.clicked.connect(partial(travel, "profile", "new_city"))
    main_win.new_city.pushButton_2.clicked.connect(partial(travel, "new_parcel", "new_city"))
    main_win.new_city.pushButton_3.clicked.connect(partial(travel, "pickup", "new_city"))
    main_win.new_city.pushButton_4.clicked.connect(partial(travel, "receive", "new_city"))
    main_win.new_city.pushButton_7.clicked.connect(partial(doLogout, "new_city"))
    main_win.new_city.pushButton_8.clicked.connect(partial(travel, "manage_role", "new_city"))
    main_win.new_city.pushButton_9.clicked.connect(partial(travel, "assign_manager", "new_city"))
    main_win.new_city.pushButton_10.clicked.connect(expandCity)
    main_win.new_city.pushButton_12.clicked.connect(partial(travel, "new_depot", "new_city"))
    main_win.new_city.pushButton_13.clicked.connect(searchCity)

    ### new_depot page buttons
    main_win.new_depot.pushButton.clicked.connect(partial(travel, "profile", "new_depot"))
    main_win.new_depot.pushButton_2.clicked.connect(partial(travel, "new_parcel", "new_depot"))
    main_win.new_depot.pushButton_3.clicked.connect(partial(travel, "pickup", "new_depot"))
    main_win.new_depot.pushButton_4.clicked.connect(partial(travel, "receive", "new_depot"))
    main_win.new_depot.pushButton_7.clicked.connect(partial(doLogout, "new_depot"))
    main_win.new_depot.pushButton_8.clicked.connect(partial(travel, "manage_role", "new_depot"))
    main_win.new_depot.pushButton_9.clicked.connect(partial(travel, "assign_manager", "new_depot"))
    main_win.new_depot.pushButton_10.clicked.connect(inaugurateDepot)
    main_win.new_depot.pushButton_11.clicked.connect(partial(travel, "new_city", "new_depot"))
    main_win.new_depot.pushButton_13.clicked.connect(findCity)
    main_win.new_depot.pushButton_14.clicked.connect(findManager)

    ### assign_manager page buttons
    main_win.assign_manager.pushButton.clicked.connect(partial(travel, "profile", "assign_manager"))
    main_win.assign_manager.pushButton_2.clicked.connect(partial(travel, "new_parcel", "assign_manager"))
    main_win.assign_manager.pushButton_3.clicked.connect(partial(travel, "pickup", "assign_manager"))
    main_win.assign_manager.pushButton_4.clicked.connect(partial(travel, "receive", "assign_manager"))
    main_win.assign_manager.pushButton_7.clicked.connect(partial(doLogout, "assign_manager"))
    main_win.assign_manager.pushButton_8.clicked.connect(partial(travel, "manage_role", "assign_manager"))
    main_win.assign_manager.pushButton_10.clicked.connect(getDepotDetails)
    main_win.assign_manager.pushButton_11.clicked.connect(partial(travel, "new_city", "assign_manager"))
    main_win.assign_manager.pushButton_12.clicked.connect(partial(travel, "new_depot", "assign_manager"))
    main_win.assign_manager.pushButton_13.clicked.connect(assignManager)

    ### receive page buttons
    main_win.receive.pushButton.clicked.connect(partial(travel, "profile", "receive"))
    main_win.receive.pushButton_2.clicked.connect(partial(travel, "new_parcel", "receive"))
    main_win.receive.pushButton_3.clicked.connect(partial(travel, "pickup", "receive"))
    main_win.receive.pushButton_5.clicked.connect(partial(travel, "manage_role", "receive"))
    main_win.receive.pushButton_6.clicked.connect(recieveParcel)
    main_win.receive.pushButton_7.clicked.connect(partial(doLogout, "receive"))
    main_win.receive.pushButton_9.clicked.connect(partial(travel, "dispatch", "receive"))
    main_win.receive.pushButton_10.clicked.connect(getDepotDetailsForRecieve)

    ### dispatch page buttons
    main_win.dispatch.pushButton.clicked.connect(partial(travel, "profile", "dispatch"))
    main_win.dispatch.pushButton_2.clicked.connect(partial(travel, "new_parcel", "dispatch"))
    main_win.dispatch.pushButton_3.clicked.connect(partial(travel, "pickup", "dispatch"))
    main_win.dispatch.pushButton_5.clicked.connect(partial(travel, "manage_role", "dispatch"))
    main_win.dispatch.pushButton_6.clicked.connect(dispatchParcel)
    main_win.dispatch.pushButton_7.clicked.connect(partial(doLogout, "dispatch"))
    main_win.dispatch.pushButton_8.clicked.connect(partial(travel, "receive", "dispatch"))
    main_win.dispatch.pushButton_10.clicked.connect(getDepotDetailsForDispatch)

    ### track_parcel page buttons
    main_win.track_parcel.pushButton.clicked.connect(partial(travel, "profile", "track_parcel"))
    main_win.track_parcel.pushButton_3.clicked.connect(partial(travel, "pickup", "track_parcel"))
    main_win.track_parcel.pushButton_4.clicked.connect(partial(travel, "receive", "track_parcel"))
    main_win.track_parcel.pushButton_5.clicked.connect(partial(travel, "manage_role", "track_parcel"))
    main_win.track_parcel.pushButton_7.clicked.connect(partial(doLogout, "track_parcel"))
    main_win.track_parcel.pushButton_8.clicked.connect(partial(travel, "new_parcel", "track_parcel"))
    main_win.track_parcel.pushButton_9.clicked.connect(partial(travel, "my_parcel", "track_parcel"))
    main_win.track_parcel.pushButton_11.clicked.connect(showTrackingDetails)

    # execute the application
    app.exec_()
    app.quit()

    # delete the application
    del app

    # except Exception as err:
    #     print(err)
