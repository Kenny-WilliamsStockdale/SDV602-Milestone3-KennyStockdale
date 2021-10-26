
#Method for debugging code instead of using gui. Parse data first 

# import csv

# def upload(file_path):
    
#     with open(file_path, newline='') as csvFile:
#         rows = csv.reader(csvFile, delimiter=',')
#         data = []
#         for row in rows:
#             data.append(row)
#     headers = data.pop(0)
#     return data
# dc.upload("./data/test_data_1.csv")