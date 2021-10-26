"""# Invoking start script/function for user to begin the proccess of using the application.  
"""
import login

# Run any window object passed in 
def run(window):
    if window == None or window == "Exit":
        return
    window = window()
    run(window)

# ------ANCHOR START MAIN APP SECTION------
if __name__ == "__main__":
    run(login.login_main)