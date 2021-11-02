"""Simple Data Explorer screen template
    that can be used as a module for different displays of data
"""
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import figures
import data_controller as dc
import login
import DES
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from db_controller import accounts
matplotlib.use('TkAgg')

 # ------ ANCHOR DELETE CANVAS SECTION ------ #
def delete_figure_agg(figure_agg):
    """Deletes the figure and canvas upon call. Used for switching between data explorer screens
    Args:
        figure_agg 
    """
    figure_agg.get_tk_widget().forget()
    plt.close('all')

 # ------ ANCHOR GET GRAPH DATA SECTION ------ #
def get_figure(des_name):
    """gets graph figures to print onto canvas/Data Explorer screen template

    Args:
        des_name ([String]): [Title of window]

    Returns:
        [function]: [returns the figure.py graph function to draw onto canvas]
    """
    if des_name == 'Data Screen Explorer 1':
        return figures.pie()
    if des_name == 'Data Screen Explorer 2':
        return figures.line_plot()
    if des_name == 'Data Screen Explorer 3':
        return figures.stack_plot()


def show(nextScreen, previousScreen, des_name, chats):
    """Generates a template for data explorer screens. 
    As every screen has the same template it makes sense to bundle it together.
    Allows for basic navigation between all generated screens

    Args:
        nextScreen ([function]): uses DES.py to parse information through the build to dictate what screen is shown
        previousScreen ([function]): uses DES.py to parse information through the build to dictate what screen is shown
        des_name ([string]): returns which DES screen name is shown and selected

    """

    # ------ ANCHOR MENU SECTION ------ #
    menu_def = [['&File', ['&Open Upload', '&Open Merge', '&Logout', '&Exit']],
                ['&Navigation', [
                    '&Size of Angler fish(DES1)', '&Angler fish observed(DES2)', '&Min and max depth of angler fish(DES3)']],
                ['&Help', '&About...'],
                ]
    
    
    # ------ ANCHOR DRAW CANVAS SECTION ------ #
    def draw_figure(canvas, figure):
        """ Draws the figure for the canvas. Draws the NavigationToolbar2Tk to use with the figure.

        Args:
            canvas : figure : returns the figure canvas aggregation object

        """
        if canvas.children:
            for child in canvas.winfo_children():
                child.destroy()
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        NavigationToolbar2Tk.toolitems = [t for t in NavigationToolbar2Tk.toolitems if t[0] not in (
        'Subplots', 'Back', 'Forward', 'Save')]

        # pack_toolbar=False will make it easier to use a layout manager later on.

        toolbar = NavigationToolbar2Tk(figure_canvas_agg, canvas, pack_toolbar=False)
        toolbar.update()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        toolbar.pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    # ------ ANCHOR GUI/LAYOUT SECTION ------ #
    layout = [
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
        [sg.Canvas(key='-CANVAS-')],
        [sg.Multiline( key='chat',default_text='Chat History:',
                      size=(55, 11), font=('current 12'), disabled=True),
        sg.Frame(layout=[
            
        [sg.Multiline(key='chatinput-key',size=(80, 7), font=('current 12'))],
        [sg.Button('Send', key='send_key', size=(81, 0), font=('current 12'))],
        ], title='Chat input', font=('current 12') )],
        
        [sg.Button('Previous', font=('current 20')), sg.Button('Next', font=('current 20') )]]

    window = sg.Window(des_name,
                       layout,
                       default_element_size=(12, 1),
                       default_button_element_size=(12, 1),
                       finalize=True,
                       size=(1000, 720))
    
    fig = get_figure(des_name)
    fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    
    #Start chat thread
    thread = chats.thread_start(chats)

    # ------ ANCHOR LOOP & PROCESS BUTTON & MENU CHOICES ------ #
    while True:
        event, values = window.read(timeout=1000, timeout_key="TIMEOUT")
        
        if event == 'TIMEOUT':
            window['chat'].update(chats.chat)
            continue
        
        if event == None or event == 'Exit':
            accounts["localuser"] = ""
            chats.exitflag = 1
            thread.join()
            window.close()
            break
        print(event, values)
        # ------ Process button choices ------ #
        if event == 'Previous':
            if fig_canvas_agg:
                delete_figure_agg(fig_canvas_agg)
            chats.exitflag = 1
            thread.join()
            window.close()
            return previousScreen()
        if event == 'Next':
            if fig_canvas_agg:
                delete_figure_agg(fig_canvas_agg)
            chats.exitflag = 1
            thread.join()
            window.close()
            return nextScreen()

        # ------ Process menu choices ------ #
        if event == 'About...':
            sg.popup('About this program', 'Version 1.0',
                     'PySimpleGUI Version', sg.version,  grab_anywhere=True,)
        if event == 'Open Upload':
            file_name = sg.PopupGetFile('Please select file to upload (the file to add to or merge in)',
                                        file_types=(("Comma separated value", "*.csv")))
            dc.upload(file_name)
            if fig_canvas_agg:
                delete_figure_agg(fig_canvas_agg)
            fig = get_figure(des_name)
            fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
        if event == 'Open Merge':
            file_name = sg.PopupGetFile('Please select file to upload (the file to add to or merge in)',
                                        file_types=(("Comma separated value", "*.csv")))
            dc.merge(file_name)
            if fig_canvas_agg:
                delete_figure_agg(fig_canvas_agg)
            fig = get_figure(des_name)
            fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
            
        if event == 'Size of Angler fish(DES1)':
            chats.exitflag = 1
            thread.join()
            window.close()
            return DES.one()
        if event == 'Angler fish observed(DES2)':
            chats.exitflag = 1
            thread.join()
            window.close()
            return DES.two()
        if event == 'Min and max depth of angler fish(DES3)':
            chats.exitflag = 1
            thread.join()
            window.close()
            return DES.three()
        if event == 'Logout':
            accounts["localuser"] = ""
            chats.exitflag = 1
            thread.join()
            window.close()
            return login.login_main()
        if event == 'send_key':
            if values['chatinput-key']  == '':
                print('Nothing to send')
                continue
            result = chats.send_message(accounts['localuser'], values['chatinput-key'])
            if result:
                print('error')
            window['chat'].update('')
            continue
        
