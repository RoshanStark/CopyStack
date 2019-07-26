# imports

#import for stack
from collections import deque

# import for clipboard
import clipboard

# imports for GUI(Tkinter)
from tkinter import *
from tkinter import ttk
import tkinter as tk

# imports for background
from system_hotkey import SystemHotkey
import time
import threading
import pyautogui

#------------------------------------------------------------------------------
#------------------------------------Tkinter-----------------------------------
#------------------------------------------------------------------------------

root = Tk()
root.geometry('530x176')
root.resizable(False, False)
root.title("Copy Stack")
root.iconbitmap(r'icons.ico')

global clipboard_text
global copy_dictionary
global paste_dictionary

#------------------------------------------------------------------------------

# frames used in this application

# logo frame
logo_frame = Frame(root, highlightbackground="green", highlightcolor="green",\
               highlightthickness=1, width=146, height=146, bd= 0)
logo_frame.place(x=2,y=2)

# hotkey frame
hotkey_frame = Frame(root, width=498, height= 50, bd= 0,relief =  RIDGE,\
                             background="gray87",borderwidth=1)
hotkey_frame.place(x = 150, y = 2)

# checkbox frame
buttons_frame = Frame(root, width=498, height= 40, bd= 0,relief =  RIDGE,\
                             background="gray87",borderwidth=1)
buttons_frame.place(x = 150, y = 52)

# buttons frame
buttons_frame = Frame(root, width=498, height= 57, bd= 0,relief =  RIDGE,\
                             background="gray87",borderwidth=1)
buttons_frame.place(x = 150, y = 92)

# roshan stark frame
stark_frame = Frame(root, width=528, height= 27, bd= 0,relief =  RIDGE,\
                             background="gray87",borderwidth=1)
stark_frame.place(x = 2, y = 150)

# roshan stark label
roshanstark_label = Label(root, text = " Developer: Roshan Stark ",\
                          relief=GROOVE)
roshanstark_label.place(x = 389,y = 152)

#------------------------------------------------------------------------------

# these lines used to place the image on the application
photo = PhotoImage(file="image.PNG")
photo_label = Label(logo_frame, image= photo).pack()

#------------------------------------------------------------------------------

# Copy Hotkeys label
copy_hotkey_label = Label(root, text = " Copy HotKey ",relief=RIDGE)\
                    .place(x = 155,y = 17)

# ComboBox select
copy_combo_values = ["ctrl+1",
                     "alt+1",
                     "ctrl+F2",
                     "alt+F2",
                     "shift+F2"
                     ]
copy_hotkey_select = ttk.Combobox(root,width=10,\
                                  values= copy_combo_values,state=NORMAL)
copy_hotkey_select.set("ctrl+1")
copy_hotkey_select.place(x = 240,y = 17)

# paste Hotkeys label
paste_hotkey_label = Label(root, text = " paste HotKey ",\
                           relief=RIDGE).place(x = 355,y = 17)

# ComboBox select
paste_combo_values = [ "ctrl+2",
                       "alt+2",
                       "ctrl+F3",
                       "alt+F3",
                       "shift+F3"
                       ]
paste_hotkey_select = ttk.Combobox(root,width=10,\
                                   values= paste_combo_values,state=NORMAL)
paste_hotkey_select.set("ctrl+2")
paste_hotkey_select.place(x = 440,y = 17)

#------------------------------------------------------------------------------

# stack checkbox
stack_checkbox_variable = IntVar()
stack_checkbox = Checkbutton(root, variable = stack_checkbox_variable,\
                               onvalue = 1, offvalue = 0, relief=RIDGE,\
                               state=NORMAL)
stack_checkbox.place(x =170, y = 59)

# stark label
stack_label = Label(root, text = "  Stack  ", relief=GROOVE)
stack_label.place(x = 200,y = 61)

#------------------------------------------------------------------------------
#buttons

def start_button_command():
    thread_start()
    start_button.config(state="disabled")
    start_button.config(bg="gray72")
    pause_button.config(state="normal")
    continue_button.config(state="disabled")
    pause_button.config(bg="gray93")
    stack_checkbox.config(state="disabled")
    copy_hotkey_select.config(state="disabled")
    paste_hotkey_select.config(state="disabled")
    root.iconify()

# start button
start_button = Button(root,text = " Start ", borderwidth=2, relief=RAISED,\
                      activeforeground="blue",activebackground="gray68",\
                      width=8, height=2,command = start_button_command,\
                      state=NORMAL)
start_button.place(x= 170, y=100)


def continue_button_command():
    pause_button.config(state="normal")
    continue_button.config(state="disabled")
    hotkeys_register()
    continue_button.config(bg="gray68")
    pause_button.config(bg="gray93")
    stack_checkbox.config(state="disabled")
    copy_hotkey_select.config(state="disabled")
    paste_hotkey_select.config(state="disabled")

# continue button
continue_button = Button(root,text = " Update ", borderwidth=2, relief=RAISED,\
                      activeforeground="green",activebackground="gray68",\
                      width=8, height=2, command = continue_button_command,\
                       state=DISABLED,bg="gray72")
continue_button.place(x= 260, y=100)


def pause_button_command():
    copyhotkey_variable = copy_hotkey_select.get()
    pastehotkey_variable = paste_hotkey_select.get()
    copyhotkey_un_register(copyhotkey_variable)
    pastehotkey_un_register(pastehotkey_variable)
    pause_button.config(state="disabled")
    continue_button.config(state="normal")
    pause_button.config(bg="gray68")
    continue_button.config(bg="gray93")
    stack_checkbox.config(state="normal")
    copy_hotkey_select.config(state="normal")
    paste_hotkey_select.config(state="normal")


# pause button
pause_button = Button(root,text = " Pause ", borderwidth=2, relief=RAISED,\
                      activeforeground="red",activebackground="gray68",\
                      width=8, height=2, command = pause_button_command,\
                      state=DISABLED,bg="gray72")
pause_button.place(x= 350, y=100)


def clear_button_command():
    print('clear executed')
    copy_stack.clear()

# clear button
clear_button = Button(root,text = " Clear ", borderwidth=2, relief=RAISED,\
                      activeforeground="blue",activebackground="gray68",\
                      width=8, height=2,command = clear_button_command,\
                      state=NORMAL)
clear_button.place(x= 440, y=100)

#------------------------------------------------------------------------------
#------------------------------------Background--------------------------------
#------------------------------------------------------------------------------

# implementing stack
copy_stack = deque()


# this function gets executed when hotkey is pressed   
def copy_execute(x, y, z):
    pyautogui.hotkey('ctrl','c')
    print('copy executed')
    time.sleep(1)
    clipboard_text = clipboard.paste() #text will have the content of clipboard
    clipboard_text_tostring = str(clipboard_text)
    copy_stack.append(clipboard_text_tostring)


# this function gets executed when hotkey is pressed   
def paste_execute(x, y, z):
    if stack_checkbox_variable.get() == 0:
        # if check box is not checked (if 0)
        print('paste executed')
        try:
            clipboard.copy(copy_stack.popleft())
        except:
            print('overflow')
        pyautogui.hotkey('ctrl','v')

    else:
        # if checkbox is checked (if 1 )
        print('paste executed')
        try:
            clipboard.copy(copy_stack.pop())
        except:
            print('overflow')
        pyautogui.hotkey('ctrl','v')

    
# dictionaries
copy_dictionary = { 'ctrl+1':('control', '1'),
                    'alt+1':('alt', '1'),
                    'ctrl+F2':('control', 'f2'),
                    'alt+F2':('alt', 'f2'),
                    'shift+F2':('shift', 'f2')
                    }
paste_dictionary = { 'ctrl+2':('control', '2'),
                    'alt+2':('alt', '2'),
                    'ctrl+F3':('control', 'f3'),
                    'alt+F3':('alt', 'f3'),
                    'shift+F3':('shift', 'f3')
                    }


def set_copyhotkey_register(hot_key_variable):
    for key_reg, value_reg in copy_dictionary.items():
        if hot_key_variable == key_reg:
            copyhotkey.register(value_reg, callback=lambda:print("Easy!"))


def set_pastehotkey_register(hot_key_variable):
    for key_reg, value_reg in paste_dictionary.items():
        if hot_key_variable == key_reg:
            pastehotkey.register(value_reg, callback=lambda:print("Easy!"))


def copyhotkey_un_register(hot_key_variable):
    for key_unreg, value_unreg in copy_dictionary.items():
        if hot_key_variable == key_unreg:
            copyhotkey.unregister(value_unreg)


def pastehotkey_un_register(hot_key_variable):
    for key_unreg, value_unreg in paste_dictionary.items():
        if hot_key_variable == key_unreg:
            pastehotkey.unregister(value_unreg)
            
            
# registering a hotkey
def hotkeys_register():
    copyhotkey_variable = copy_hotkey_select.get()
    set_copyhotkey_register(copyhotkey_variable)

    pastehotkey_variable = paste_hotkey_select.get()
    set_pastehotkey_register(pastehotkey_variable)
    
    
# unregistering a hotkey
def copyhotkey_un_register(hot_key_variable):
    for key_unreg, value_unreg in copy_dictionary.items():
        if hot_key_variable == key_unreg:
            copyhotkey.unregister(value_unreg)


def pastehotkey_un_register(hot_key_variable):
    for key_unreg, value_unreg in paste_dictionary.items():
        if hot_key_variable == key_unreg:
            pastehotkey.unregister(value_unreg)
            
    
# target function of thread (i.ethread starts from here)
def execute_thread():
    time.sleep(1)
    print('thread executed')
    hotkeys_register()

    
# defining hotkeys for copy and paste
copyhotkey = SystemHotkey(consumer = copy_execute)
pastehotkey =SystemHotkey(consumer = paste_execute)

# this line creates a thead     
thread_variable = threading.Thread(target=execute_thread)


# this function used to start a thread when start button is pressed
def thread_start():
    thread_variable.start()


#------------------------------------------------------------------------------
# main loop of tkinter

root.mainloop()

#------------------------------------------------------------------------------





