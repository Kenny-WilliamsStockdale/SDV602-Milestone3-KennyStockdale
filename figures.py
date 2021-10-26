"""draws the graphs with reference to the data in the data_filters.py file

"""
import data_filters as df
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


# ------ANCHOR PIE CHART SECTION------
def pie():
    """pie chart with imported data_filters csv data

    Returns:
        [function]: get the current plot figure
    """
    labels, values = df.sizeFish()
    fig1, ax1 = plt.subplots(figsize=(10, 4.2))
    ax1.pie(values, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=0)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')
    ax1.legend(loc='upper right')
    plt.title('Size of Angler Fish in New Zealand waters (millimeters)')
    return plt.gcf()

# ------ANCHOR LINE PLOT SECTION------
def line_plot():
    """line plot with imported data_filters csv data

    Returns:
        [function]: get the current plot figure
    """
    labels = []
    values = []
    data = df.fishAmountYear()
    # sorting
    for key in sorted(data.keys()):
        labels.append(key)
        values.append(data[key])
    fig1, ax1 = plt.subplots(figsize=(10, 4.2))
    ax1.set_ylabel('Number of fish')
    ax1.set_xlabel('Year')
    ax1.set_title('Angler fish observed')
    blue_patch = mpatches.Patch(color='blue', label='Line')
    plt.legend(handles=[blue_patch])
    plt.plot(labels, values)
    return plt.gcf()

# ------ANCHOR STACK PLOT SECTION------
def stack_plot():
    """stack plot with imported data_filters csv data

    Returns:
        [function]: get the current plot figure
    """
    min, max = df.depth()
    idxes = range(0, len(min))
    y1  = min
    y2  = max
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.stackplot(idxes, y1, y2)
    ax.set_title('Min and max depth of angler fish examined')
    ax.set_ylabel('min and max depth (meters)')
    ax.set_xlabel('Index number of entries (ID)')
    orange_patch = mpatches.Patch(color='orange', label='max-depth')
    blue_patch = mpatches.Patch(color='blue', label='min-depth')
    plt.legend(handles=[orange_patch,blue_patch])
    
    return plt.gcf()

