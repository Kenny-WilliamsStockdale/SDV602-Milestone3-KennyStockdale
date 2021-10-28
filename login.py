"""
    This presents the user with a login page to create a username and password
    to access the application.
"""

import PySimpleGUI as sg
import db_controller as dbc
from DES import one as DES1
# ------------------------------- LOGIN MAIN PAGE START -------------------------------


def login_main():
    """
       Function allows user to create or enter an existing password to login to the application
    """
    layout = [
        [sg.Text(k='error')],
        [sg.Text('Username:')],
        [sg.Input(k='username')],
        [sg.Text('Password:')],
        [sg.Input(k='password')],
        [sg.Button('Login'), sg.Button('Register')],
        [sg.Button('Exit Application')]]
    window = sg.Window('Property Titles Login Page', layout, finalize=True)
    while True:
        event, values = window.read()
        print(event, values)

        if event == None or event == 'Exit Application':
            window.close()
            break
        if event == 'Login':
            username, password = values["username"], values["password"]
            if username == "" or password == "":
                window["error"].update("Please enter username and password")
                continue
            elif dbc.user_exists(username):
                if not dbc.check_password(username, password):
                    window["error"].update("Incorrect Password")
                    continue

                dbc.localuser = username
                window.close()
                return DES1
            else:
                window["error"].update(f'User {username} was not found.')
                continue

        if event == 'Register':
            window.close()
            return registration

# ------------------------------- LOGIN MAIN PAGE END -------------------------------

# ------------------------------- REGISTRATION PAGE START -------------------------------


def registration():
    """
        function opens welcome login page. Navigation to available
    """
    layout = [
        [sg.Text(k='error')],
        [sg.Text('Username:')],
        [sg.Input(k='username')],
        [sg.Text('Password:')],
        [sg.Input(k='password', password_char='*')],
        [sg.Text('Confirm Password:')],
        [sg.Input(k='confirm_password', password_char='*')],
        [sg.Button('Login'), sg.Button('Register')],
        [sg.Button('Exit Application')]]
    window = sg.Window('Property Titles Login Page', layout,
                       finalize=True, size=(350, 250))
    while True:
        event, values = window.read()
        print(event, values)

        if event == None or event == 'Exit Application':
            window.close()
            break
        if event == 'Register':
            username, password, confirm_password = values["username"], values["password"], values["confirm_password"]
            if username == "" or password == "" or confirm_password == "":
                window["error"].update("Please enter username and password")
                continue
            elif dbc.user_exists(username):
                window["error"].update("User already exists")
                continue
                
            elif password != confirm_password:
                window["error"].update("Passwords do not match")
                continue
 
            else:
                outcome = dbc.add_user(username, password)
                if outcome:
                    window["error"].update(f"{outcome}")
                dbc.localuser = username
                #print(dbc.localuser)
                window.close()
                return DES1

        if event == 'Login':
            window.close()
            return login_main
# ------------------------------- REGISTRATION PAGE END -------------------------------
