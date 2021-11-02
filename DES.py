"""parses in which screen to view upon application load and next/previous builds.

"""
import build
import data_controller as dc
import db_controller as dbc


def one():
    """upon application load checks if data is loaded, then redirects to Data Screen Explorer 1

    """
    nextScreen = two
    previousScreen = three
    dc.check_app_has_data()
    return build.show(
        nextScreen,
        previousScreen,
        "Data Screen Explorer 1",
        dbc.chats("DES1 Chat")
    )


def two():
    """upon application load checks if data is loaded, then redirects to Data Screen Explorer 2

    """
    nextScreen = three
    previousScreen = one
    dc.check_app_has_data()
    return build.show(
        nextScreen, 
        previousScreen,
        "Data Screen Explorer 2",
        dbc.chats("DES2 Chat")
    )


def three():
    """upon application load checks if data is loaded, then redirects to Data Screen Explorer 3

    """
    nextScreen = one
    previousScreen = two
    dc.check_app_has_data()
    return build.show(
        nextScreen,
        previousScreen,
        "Data Screen Explorer 3",
        dbc.chats("DES3 Chat")
    )
