"""controlls how the test data is used throughout the application.
Allows for uploading and merging of data
  
"""
import csv
import db_controller as dbc

data = []
dbname = dbc.get_database()
# ------ANCHOR UPLOAD SECTION------
def upload(file_path):
    """takes local data and uploads it to an empty list to be read by the application

    Args:
        file_path: gets the file path that relates to the data being uploaded

    Returns:
        [list]: returns a list of data contained in the uploaded csv file
    """
    global data
    
    collection_name = dbname["data"]
    
    if collection_name.find_one({}) == None:
        collection_name.insert_one({"data": []})
    
    with open(file_path, newline='') as csvFile:
        rows = csv.reader(csvFile, delimiter=',')
        data = []
        for row in rows:
            data.append(row)
    headers = data.pop(0)
    
    collection_name.find_one_and_replace({},{"data": data})
    return data

# ------ANCHOR MERGE SECTION------
def merge(file_path):
    """takes local data and merges it to an empty list to be read by the application

    Args:
        file_path: gets the file path that relates to the data being merged

    Returns:
        [list]: returns a list of data including the newly appended data to the list
    """
    global data
    collection_name = dbname["data"]
    
    with open(file_path, newline='') as csvFile:
        rows = csv.reader(csvFile, delimiter=',')
        merge = []
        for row in rows:
            merge.append(row)
    headers = merge.pop(0)
    for row in merge:
        data.append(row)
    collection_name.find_one_and_replace({},{"data": data})
    return data

# ------ANCHOR INITIAL CHECK AND THEN UPLOAD SECTION------
def check_app_has_data():
    """checks if the application has data already loaded. If not prompts user to load data.
    
    """
    import data_controller as dc
    import PySimpleGUI as sg
    global data
    
    collection_name = dbname["data"]
    
    if collection_name.find_one({}) == None:
        collection_name.insert_one({"data": []})
    data = collection_name.find_one({})["data"]
    
    if dc.data == []:
        file_name = sg.PopupGetFile('Please select file to upload (the file to add to or merge in)',
                                    file_types=(("Comma separated value", "*.csv"),))
        if not file_name:
            raise Exception("No file provided. Exiting application.")
        dc.upload(file_name)
        if dc.data == []:
            raise Exception("App did not receive data. Exiting application.")