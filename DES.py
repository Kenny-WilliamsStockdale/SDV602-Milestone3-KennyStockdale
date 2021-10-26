"""parses in which screen to view upon application load and next/previous builds.

"""
import build
import data_controller as dc

def one ():
    """upon application load checks if data is loaded, then redirects to Data Screen Explorer 1
    
    """
    dc.check_app_has_data()
    return build.show(two, three, "Data Screen Explorer 1")


def two ():
    """upon application load checks if data is loaded, then redirects to Data Screen Explorer 1
    
    """
    dc.check_app_has_data()
    return build.show(three, one, "Data Screen Explorer 2")


def three ():
    """upon application load checks if data is loaded, then redirects to Data Screen Explorer 1
    
    """
    dc.check_app_has_data()
    return build.show(one, two, "Data Screen Explorer 3")
    
    