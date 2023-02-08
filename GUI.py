import PySimpleGUI as sg
from PIL import Image
import io
import time
import sys, os
import requests
from pathlib import Path
NAME_SIZE = 23
from get_product import product


def name(name):
    dots = NAME_SIZE - len(name) - 2
    return sg.Text(name + ' ' + '' * dots, size=(NAME_SIZE, 1), justification='r', pad=(0, 10), font='_ 10 bold')


def exception_window(msg):
    layout = [
        [sg.Text(msg, font="Arial 16", pad=(230, 10), background_color='red', justification='c')],
        [sg.Button('OK', enable_events=True, font='Arial 12 bold', key='-EXCEPTION_OK-')]
    ]
    window = sg.Window('The PySimpleGUI', layout, finalize=True,
                       right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT,
                       keep_on_top=True, background_color='red', element_justification='c')
    return window


def operation_window(url):
    product_instance.get_product_page(url)
    image = product_instance.image
    image = image.resize((200, 200))
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    layout_r = [
        [sg.Text('product title:', font='_ 10 bold', background_color='black', pad=(50, 10)),
         sg.Text(product_instance.title, font='_ 10 bold')],
        [sg.Image(data=bio.getvalue(), p=(430, 0))],
        [sg.Frame('', [[sg.Text(f"Base Price: {product_instance.price}",
                                pad=(22, 0), background_color='#14D8B3', text_color='black', font='_ 9 bold')]],
                  border_width=5, pad=(440, 5), background_color='#14D8B3')]
    ]
    window = sg.Window('The PySimpleGUI Element List', layout_r, finalize=True,
                       right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT,
                       keep_on_top=True,
                       size=(1080, 720))
    return window


def make_window(theme=None):

    sg.theme(theme)
    Menu = sg.Menu

    treedata = sg.TreeData()

    treedata.Insert("", '_A_', 'Tree Item 1', [1234], )
    treedata.Insert("", '_B_', 'B', [])
    treedata.Insert("_A_", '_A1_', 'Sub Item 1', ['can', 'be', 'anything'], )

    image = Image.open('amazon1.png')
    bio = io.BytesIO()
    image.save(bio, format="PNG")

    layout_l = [
        [name('URL'), sg.InputText(size=(50, 1), key='-URL-', disabled=False,
                                   default_text='https://www.amazon.com/-/he/DEWALT-%D7%9E%D7%A9%D7%95%D7%9C%D7%91%D7%AA-%D7%90%D7%9C%D7%97%D7%95%D7%98%D7%99-%D7%A1%D7%95%D7%9C%D7%9C%D7%95%D7%AA-DCK44C2/dp/B082G2MKX8?ref_=Oct_DLandingS_D_bf6e40fe_68')],
        [name('Duration (Days) lowest price'), sg.Input(s=15, default_text=3, justification='c',key='-DURATION-'),
         name('Sample Interval (Hours)'), sg.Input(s=15, default_text=2, justification='c', key='-INTERVAL-')],
        [name('Receiver Email'), sg.InputText(size=(50, 1), key='-EMAIL_CONFIG-')],
        [name('Sender Email Password'), sg.InputText(size=(20, 1), key='-PASS_CONFIG-', password_char='*')],
        [sg.Button('START', enable_events=True, button_color='green', font='Arial 12 bold', p=(475, 0), key='-START-')],
    ]

    layout_r = [
        [name('Canvas'), sg.Canvas(background_color=sg.theme_button_color()[1], size=(125,40))],
    ]

    # Note - LOCAL Menu element is used (see about for how that's defined)
    layout = [[Menu([['File', ['Exit']], ['Edit', ['Edit Me', ]]],  k='-CUST MENUBAR-', p=0)],
              [sg.T('Amazon Price Bot', text_color="black", font='Cooper 16 bold', justification='c', expand_x=True),
               sg.Image(data=bio.getvalue(), key="-IMAGE-")],
              [sg.Col(layout_l, p=0)]]

    window = sg.Window('The PySimpleGUI Element List', layout, finalize=True,
                       right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT,
                       keep_on_top=True,
                       size=(1080, 720))

    return window


from multiprocessing import Process, Queue
def interval_product_sampling(q, interval, days, url):
    prod = product()
    hours = days * 24
    min = hours * 60
    sec = min * 60
    total_start = time.time()
    while True:
        total_end = time.time()
        total_time_ms = total_end - total_start
        print("total_time_ms", total_time_ms)
        if total_time_ms*1000 > sec:
            break
        time.sleep(interval*60*60)
        prod.get_product_page(url)
        q.put(prod.price)


window1, window2 = make_window(), None
product_instance = product()
queue = Queue()
p = None

while True:
    window, event, values = sg.read_all_windows()
    # print(event, values)
    if (event == sg.WIN_CLOSED or event == 'Exit'):
        if window == window1:
            break
        else:
            window.close()
    if event == 'Edit Me':
        sg.execute_editor(__file__)
    if event == '-EXCEPTION_OK-':
        window.close()
    if event == '-START-':
        try:
            response = requests.get(window1['-URL-'].get())
        except Exception as e:
            exception_window(e)
            continue
        p = Process(target=interval_product_sampling, args=(queue, window1['-INTERVAL-'].get(),
                                                            window1['-DURATION-'].get(), window1['-URL-'].get()))
        p.start()
        window2 = operation_window(window1['-URL-'].get())
    if queue.empty() == False:
        price = queue.get()
        print(price)
    elif event == 'Version':
        sg.popup_scrolled(__file__, sg.get_versions(), keep_on_top=True, non_blocking=True)
if p is not None:
    p.join()
    p.close()
window.close()