"""Data from csv uploaded has been filtered into data that can be used in a graph/display format.

"""
import data_controller as dc

def fishAmountYear():  #Lineplot data
    """
    Returns:
        [dictionary]: the number of fish in any given year, observed.
    """
    data = dc.data
    dictline = {}
    for row in data:
        if row[19] != "":
            if row[19] in dictline.keys():
                dictline[row[19]] += int(row[10])
            else:
                dictline[row[19]] = int(row[10])

    return (dictline)


def sizeFish():  # Piechart data
    """
    Returns:
        [dictionary]: returns the size of fish in selected categories of sizes in millimeters
    """
    data = dc.data
    barData = {
        '1-50': 0,
        '51-100': 0,
        '101-150': 0,
        '151-200': 0,
        '201-250': 0,
        '251+': 0
    }
    for row in data:
        size = int(row[6].split(' ')[0]) if row[6] != '' else 0

        if size in range(1, 51):
            barData['1-50'] += 1
        elif size in range(51, 101):
            barData['51-100'] += 1
        elif size in range(101, 151):
            barData['101-150'] += 1
        elif size in range(151, 201):
            barData['151-200'] += 1
        elif size in range(201, 251):
            barData['201-250'] += 1
        elif size > 251:
            barData['251+'] += 1
    labels = list(barData.keys())
    values = list(barData.values())
    return labels, values

def depth ():  # Stackplot data
    """
    Returns:
        [lists]: returns min and max size of observed fish in depth (meters)
    """
    data = dc.data
    min = []
    max = []
    for row in data:
        if row[27] != "" and row[28] != "":
            min.append(int(row[27]))
            max.append(int(row[28]))
            
    return min, max
    

# def merge(newFile, currentFile):
#     dc.append(newFile, currentFile)