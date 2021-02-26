import PySimpleGUI as sg

sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.In() , sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

layout = [ [sg.Text('Some text on Row 1', key='_TEXT1_')],
            [sg.Input(key='_FILEBROWSE_', enable_events=True, visible=True)],
            [sg.FileBrowse(target='_FILEBROWSE_')],
            [sg.In() , sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
            [sg.OK()], ]
# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    print('You entered ', values)
    window.FindElement('_TEXT1_').Update('ererere', text_color='red')
    print(window.FindElement('_TEXT1_').text())

window.close()
