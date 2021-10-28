from db import get_database
localuser = ""

dbname = get_database()
# ---User---------------

def add_user(username, password):
    collection_name = dbname["users"]
    
    user = {"_id": username, "password": password}
    
    try: 
        collection_name.insert_one(user)
    except:
        alert = "Could not add user"
        return alert

def user_exists(username):
    
    collection_name = dbname["users"]
    
    user = collection_name.find_one({"_id": username})
    return True if user else False

def check_password(username, password):
    
    collection_name= dbname["users"]
    
    user = collection_name.find_one({"_id": username})
    
    return True if user["password"] == password else False