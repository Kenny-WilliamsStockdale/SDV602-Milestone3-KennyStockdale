def get_database():
    from pymongo import MongoClient
    
    # Get cert from and allow communicationm from database
    import certifi
    ca = certifi.where()
    
    # provide mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://Kenny:Password123@cluster0.rpudg.mongodb.net/SDV602-Database?retryWrites=true&w=majority"
    
    # create a connection using mongoclient 
    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)
    
    # create/select the database
    return client["Cluster0"]



