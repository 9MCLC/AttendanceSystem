from tkinter import *
import tkinter as tk
from tkinter import ttk
from pyzbar.pyzbar import decode
import requests
from PIL import Image, ImageTk
import os
import json

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

apiEndpoint = config['apiEndpoint']
class NameList:
    def __init__(self, window=None):
        self.window = window if window else Tk()
        self.window.title("NAMELIST")
        self.window.geometry('%dx%d+0+0' % (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=4)
        self.window.grid_rowconfigure(0, weight=2)
        self.window.grid_rowconfigure(1, weight=8)
        self.window.minsize(800, 400)
        def toggle_fullscreen(event = None):
            state = not self.window.attributes('-fullscreen')
            self.window.attributes('-fullscreen', state)

        def on_escape(event):
            self.window.attributes('-fullscreen', False)
        self.window.attributes('-fullscreen', True)
        self.window.bind("<F11>", toggle_fullscreen)
        self.window.bind("<Escape>", on_escape)
        self.create_function_frame()
        self.create_title_page()
        self.create_toolbar()

        # self.update()
        self.window.mainloop()

    def LaunchLobby(self):
        self.window.destroy()
        # Lobby()

    def LaunchRegistration(self):
        self.window.destroy()
        # Registration()

    def LaunchNameList(self):
        self.window.destroy()
        # NameList()

    def get_window_size(self):
        window_size = min(self.window.winfo_width(), self.window.winfo_height())
        return window_size

    def create_title_page(self):
        self.title_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid")
        self.title_frame.grid_propagate(False)

        def update_title(event=None):
            window_size = self.window.winfo_width()
            title_bold_font = ("Helvetica", window_size//20, "bold")
            name_bold_font = ("Helvetica", window_size//50, "bold")
            self.title_label.config(font=title_bold_font)
            self.name_label.config(font=name_bold_font)

        self.title_frame.bind("<Configure>", update_title)

        self.title_frame.grid_rowconfigure(0, weight=10)
        self.title_frame.grid_rowconfigure(1, weight=50)
        self.title_frame.grid_rowconfigure(2, weight=10)
        self.title_frame.grid_rowconfigure(3, weight=1)
        self.title_frame.grid_rowconfigure(4, weight=9)
        self.title_frame.grid_rowconfigure(5, weight=10)
        self.title_frame.grid_columnconfigure(0, weight=1)
        self.title_frame.grid_columnconfigure(1, weight=1)
        self.title_frame.grid_columnconfigure(2, weight=1)

        self.pageTitleFrame = tk.Frame(self.title_frame, bg="white")
        self.churchTitleFrame = tk.Frame(self.title_frame, bg="white")
        self.borderTitleFrame = tk.Frame(self.title_frame, bg="black")
        self.lineTitleFrame = tk.Frame(self.title_frame, bg="black")
        self.pageTitleFrame.grid_propagate(False)
        self.churchTitleFrame.grid_propagate(False)
        self.borderTitleFrame.grid_propagate(False)
        self.lineTitleFrame.grid_propagate(False)
        self.pageTitleFrame.grid(column=0, row=0, rowspan=5, columnspan=2, sticky="nsew")
        self.churchTitleFrame.grid(column=2, row=1, sticky="nsew")
        self.borderTitleFrame.grid(column=0, row=5, columnspan=3, sticky="nsew")
        self.lineTitleFrame.grid(column=2, row=3, sticky="nsew")
        
        self.pageTitleFrame.grid_rowconfigure(0, weight=1)
        self.pageTitleFrame.grid_columnconfigure(0, weight=1)
        self.churchTitleFrame.grid_rowconfigure(0, weight=1)
        self.churchTitleFrame.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(self.pageTitleFrame, text="NAMELIST", font=("Helvetica", self.get_window_size()//15, 'bold'), anchor=W, bg='white')
        self.title_label.grid(sticky='nsew')

        self.name_label = tk.Label(self.churchTitleFrame, text="9MCLC  ", font=("Helvetica", self.get_window_size()//15, 'bold'), anchor=SE, bg='white')
        self.name_label.grid(sticky='nsew')

        self.title_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def create_toolbar(self):
        self.toolbar_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid", width=self.window.winfo_width() * 0.2)
        self.toolbar_frame.grid_propagate(False)

        def update_toolbar(event=None):
            window_size = self.window.winfo_width()
            bold_font = ("Helvetica", int(window_size//80), "bold")
            lobbyButton.config(font=bold_font)
            nameListButton.config(font=bold_font)
            registrationButton.config(font=bold_font)
            image = Image.open("./Logo.png")
            image.thumbnail((int(self.window.winfo_width() //10), int(self.window.winfo_width() //10)))
            image = ImageTk.PhotoImage(image)
            image_label.config(image=image)
            image_label.image = image

        self.toolbar_frame.bind("<Configure>", update_toolbar)

        self.toolbar_frame.grid_columnconfigure(0, weight=1)
        self.toolbar_frame.grid_columnconfigure(1, weight=8)
        self.toolbar_frame.grid_columnconfigure(2, weight=1)
        self.toolbar_frame.grid_rowconfigure(0, weight=10)
        self.toolbar_frame.grid_rowconfigure(1, weight=30)
        self.toolbar_frame.grid_rowconfigure(2, weight=10)
        self.toolbar_frame.grid_rowconfigure(3, weight=30)
        self.toolbar_frame.grid_rowconfigure(4, weight=10)
        self.toolbar_frame.grid_rowconfigure(5, weight=30)
        self.toolbar_frame.grid_rowconfigure(6, weight=10)
        self.toolbar_frame.grid_rowconfigure(7, weight=50)
        self.toolbar_frame.grid_rowconfigure(8, weight=10)
        self.lobbyButtonFrame = tk.Frame(self.toolbar_frame, bg="white")
        self.nameListButtonFrame = tk.Frame(self.toolbar_frame, bg="white")
        self.registrationFrame = tk.Frame(self.toolbar_frame, bg="white")
        self.logoFrame = tk.Frame(self.toolbar_frame, bg="white")
        self.lobbyButtonFrame.grid_propagate(False)
        self.nameListButtonFrame.grid_propagate(False)
        self.registrationFrame.grid_propagate(False)
        self.logoFrame.grid_propagate(False)

        self.lobbyButtonFrame.grid(row=1, column=1, sticky='nsew')
        self.nameListButtonFrame.grid(row=3, column=1, sticky='nsew')
        self.registrationFrame.grid(row=5, column=1, sticky='nsew')
        self.logoFrame.grid(row=7, column=1, sticky='nsew')
        self.logoFrame.grid_rowconfigure(0, weight=1)
        self.logoFrame.grid_columnconfigure(0, weight=1)
        self.lobbyButtonFrame.grid_rowconfigure(0, weight=1)
        self.lobbyButtonFrame.grid_columnconfigure(0, weight=1)
        self.nameListButtonFrame.grid_rowconfigure(0, weight=1)
        self.nameListButtonFrame.grid_columnconfigure(0, weight=1)
        self.registrationFrame.grid_rowconfigure(0, weight=1)
        self.registrationFrame.grid_columnconfigure(0, weight=1)

        lobbyButton = Button(self.lobbyButtonFrame, text="LOBBY", command=self.LaunchLobby, font=("Helvetica", self.get_window_size()//18, 'bold'), cursor="hand2", relief='groove')
        lobbyButton.grid(sticky='nsew')

        nameListButton = Button(self.nameListButtonFrame, text="NAME LIST", command=self.LaunchNameList, font=("Helvetica", self.get_window_size()//18, 'bold'), cursor="hand2", relief='groove')
        nameListButton.grid(sticky='nsew')

        registrationButton = Button(self.registrationFrame, text="REGISTRATION", command=self.LaunchRegistration, font=("Helvetica", self.get_window_size()//18, 'bold'), cursor="hand2", relief='groove')
        registrationButton.grid(sticky='nsew')

        image = Image.open("./Logo.png")
        image.thumbnail((int(self.window.winfo_width() * 200), int(self.window.winfo_width() * 200)))
        image = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.logoFrame, image=image, bg='white')
        image_label.image = image

        image_label.grid(sticky='nsew')
        
        self.toolbar_frame.grid(row=1, column=0, sticky="nsew")

    def create_function_frame(self):
        def update_function(event=None):
            window_size = self.get_window_size()
            text_bold_font = ("Helvetica", window_size//40, "bold")
            entry_font = ("Helvetica", window_size//50, 'bold')
            self.searchLabel.config(font=text_bold_font)
            self.searchEntry.config(font=entry_font)
            self.unattendButton.config(font=entry_font)
            self.attendButton.config(font=entry_font)
            self.removeButton.config(font=entry_font)

        def search_on_entry_click(event):
            if self.searchEntry.get() == "Enter name here...":
                self.searchEntry.delete(0, "end")
                self.searchEntry.config(fg='black')

        def search_on_focus_out(event):
            if self.searchEntry.get() == "":
                self.searchEntry.insert(0, "Enter name here...")
                self.searchEntry.config(fg='gray')

        def updateSearchCriteria(event):
            self.searchCriteria = self.searchEntry.get().strip()
            self.update_table()

        self.function_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid")
        self.function_frame.grid(row=1, column=1, sticky="nsew")
        self.function_frame.grid_propagate(False)
        self.function_frame.grid_rowconfigure(0, weight=5)
        self.function_frame.grid_rowconfigure(1, weight=5)
        self.function_frame.grid_rowconfigure(2, weight=5)
        self.function_frame.grid_rowconfigure(3, weight=70)
        self.function_frame.grid_rowconfigure(4, weight=15)
        self.function_frame.grid_columnconfigure(0, weight=5)
        self.function_frame.grid_columnconfigure(1, weight=20)
        self.function_frame.grid_columnconfigure(2, weight=40)
        self.function_frame.grid_columnconfigure(3, weight=10)
        self.function_frame.grid_columnconfigure(4, weight=20)
        self.function_frame.grid_columnconfigure(5, weight=5)
        self.function_frame.bind("<Configure>", update_function)
        
        self.searchLabel = Label(self.function_frame, text="Search:", font=("Helvetica", self.get_window_size()//10), bg='white', justify='left')
        self.searchLabel.grid(row=1, column=1, sticky='nsew')

        self.searchEntry = Entry(self.function_frame, relief='solid', fg='gray', justify='left', bd=2)
        self.searchEntry.insert(0, "Enter name here...")
        self.searchEntry.bind('<FocusIn>', search_on_entry_click)
        self.searchEntry.bind('<FocusOut>', search_on_focus_out)
        self.searchEntry.bind("<KeyRelease>", updateSearchCriteria)
        self.searchEntry.grid(row=1, column=2, sticky='nsew')

        self.table_frame = tk.Frame(self.function_frame, bg="white", bd=2, relief="solid")
        self.table_frame.grid(row=3, column=1, columnspan=2, sticky="nsew")
        self.table_frame.grid_propagate(False)
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        self.button_frame = tk.Frame(self.function_frame, bg="white")
        self.button_frame.grid(row=3, column=4, sticky="nsew")
        self.button_frame.grid_propagate(False)
        self.button_frame.grid_rowconfigure(0, weight=20)
        self.button_frame.grid_rowconfigure(1, weight=10)
        self.button_frame.grid_rowconfigure(2, weight=5)
        self.button_frame.grid_rowconfigure(3, weight=10)
        self.button_frame.grid_rowconfigure(4, weight=5)
        self.button_frame.grid_rowconfigure(5, weight=10)
        self.button_frame.grid_rowconfigure(6, weight=20)
        self.button_frame.grid_columnconfigure(0, weight=1)

        self.unattendButton = Button(self.button_frame, text="Unattend User", command=self.unattend, font=("Helvetica", self.get_window_size()//18, 'bold'), width=20, cursor="hand2", relief='groove')
        self.unattendButton.grid(row=1, column=0)

        self.attendButton = Button(self.button_frame, text="Attend User", command=self.attend, font=("Helvetica", self.get_window_size()//18, 'bold'), width=20, cursor="hand2", relief='groove')
        self.attendButton.grid(row=3, column=0)

        self.removeButton = Button(self.button_frame, text="Remove User", command=self.remove, font=("Helvetica", self.get_window_size()//18, 'bold'), width=20, cursor="hand2", relief='groove')
        self.removeButton.grid(row=5, column=0)

        self.create_table()

    def update_table(self):
        def reformatData(data:list):
            returnData = []
            for row in data:
                tempDict = {}
                tempDict['Name'] = row['Name']
                tempDict['PhoneNumber'] = row['PhoneNumber']
                tempDict['Attendance'] = row['Attended']
                returnData.append(tempDict)
            return returnData
        def filterByName(data: list, target):
            if target == '':
                filtered_data = data
            else:
                filtered_data = [row for row in data if str(target.lower()) in row["Name"].lower()]

            return filtered_data
        data = requests.get(f"{apiEndpoint}/getTableData").json()
        self.formattedData = reformatData(data['users'])
        for row in self.table.get_children():
            self.table.delete(row)
            
        for col in self.formattedData[0].keys():
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=300)
        for row in filterByName(self.formattedData, self.searchCriteria):
            self.table.insert("", "end", values=list(row.values()))

    def create_table(self):
        self.table = ttk.Treeview(self.table_frame, columns=('Name', 'PhoneNumber', 'Attendance'), show="headings")
        self.table.grid(row=0, column=0, sticky='nsew')
        self.searchCriteria = ''
        self.update_table()

    def unattend(self):
        def clearUser():
            name = self.table.item(self.table.focus())['values'][0]
            uuid = requests.get(f'{apiEndpoint}/getUser', params={'name': name}).json().get('users')[0].get('UUID')
            requests.delete(f'{apiEndpoint}/removeAttendance', json={'UUID': uuid})
            cfm.destroy()
            self.update_table()
        if self.table.selection():
            name = self.table.item(self.table.focus())['values'][0]
            attended = self.table.item(self.table.focus())['values'][2]
            if attended == "No":
                self.temp_msg(message="You can't unmark an absent user")
            else:
                cfm = Tk()
                width, height = cfm.winfo_screenwidth()/8, cfm.winfo_screenwidth()/16
                cfm.geometry('%dx%d+%d+%d' % (cfm.winfo_screenwidth()/8, cfm.winfo_screenwidth()/16, int((cfm.winfo_screenwidth() - width) / 2), int((cfm.winfo_screenheight() - height) / 2)))
                cfm.title("Confirmation")
                cfm.grid_rowconfigure(0, weight=1)
                cfm.grid_rowconfigure(1, weight=1)
                cfm.grid_rowconfigure(2, weight=1)
                cfm.grid_columnconfigure(0, weight=1)
                cfm.grid_columnconfigure(1, weight=4)
                cfm.grid_columnconfigure(2, weight=1)
                cfm.grid_columnconfigure(3, weight=4)
                cfm.grid_columnconfigure(4, weight=1)

                confirmationMessage_label = Label(cfm, text="Remove user's attendance", font=("Arial", 10), justify='center')
                confirmationMessage_label.grid(row=0, column=0, columnspan=5, sticky='nsew')

                confirmationDetails_label = Label(cfm, text=f"Name: {name}", font=("Arial", 10), justify='center')
                confirmationDetails_label.grid(row=1, column=0, columnspan=5, sticky='nsew')

                confirmButton = Button(cfm, text="Yes", command=clearUser, cursor="hand2", relief='groove')
                confirmButton.grid(row=2, column=1, sticky='nsew')

                closeButton = Button(cfm, text="Close", command=cfm.destroy, cursor="hand2", relief='groove')
                closeButton.grid(row=2, column=3, sticky='nsew')
                    
                cfm.mainloop()
        else:
            self.temp_msg(message='PLEASE SELECT A USER')

    def attend(self):
        def addUser():
            name = self.table.item(self.table.focus())['values'][0]
            uuid = requests.get(f'{apiEndpoint}/getUser', params={'name': name}).json().get('users')[0].get('UUID')
            requests.post(f'{apiEndpoint}/addAttendance', json={'UUID': uuid, 'name': name})
            cfm.destroy()
            self.update_table()
        if self.table.selection():
            name = self.table.item(self.table.focus())['values'][0]
            attended = self.table.item(self.table.focus())['values'][2]
            if attended == "Yes":
                self.temp_msg(message="You can't mark a marked user")
            else:
                cfm = Tk()
                width, height = cfm.winfo_screenwidth()/8, cfm.winfo_screenwidth()/16
                cfm.geometry('%dx%d+%d+%d' % (cfm.winfo_screenwidth()/8, cfm.winfo_screenwidth()/16, int((cfm.winfo_screenwidth() - width) / 2), int((cfm.winfo_screenheight() - height) / 2)))
                cfm.title("Confirmation")
                cfm.grid_rowconfigure(0, weight=1)
                cfm.grid_rowconfigure(1, weight=1)
                cfm.grid_rowconfigure(2, weight=1)
                cfm.grid_columnconfigure(0, weight=1)
                cfm.grid_columnconfigure(1, weight=4)
                cfm.grid_columnconfigure(2, weight=1)
                cfm.grid_columnconfigure(3, weight=4)
                cfm.grid_columnconfigure(4, weight=1)

                confirmationMessage_label = Label(cfm, text="Mark user's attendance", font=("Arial", 10), justify='center')
                confirmationMessage_label.grid(row=0, column=0, columnspan=5, sticky='nsew')

                confirmationDetails_label = Label(cfm, text=f"Name: {name}", font=("Arial", 10), justify='center')
                confirmationDetails_label.grid(row=1, column=0, columnspan=5, sticky='nsew')

                confirmButton = Button(cfm, text="Yes", command=addUser, cursor="hand2", relief='groove')
                confirmButton.grid(row=2, column=1, sticky='nsew')

                closeButton = Button(cfm, text="Close", command=cfm.destroy, cursor="hand2", relief='groove')
                closeButton.grid(row=2, column=3, sticky='nsew')
                    
                cfm.mainloop()
        else:
            self.temp_msg(message="PLEASE SELECT A USER")

    def remove(self):
        def deleteUser():
            name = self.table.item(self.table.focus())['values'][0]
            uuid = requests.get(f'{apiEndpoint}/getUser', params={'name': name}).json().get('users')[0].get('UUID')
            requests.delete(f'{apiEndpoint}/removeUser', json={'UUID': uuid})
            cfm.destroy()
            self.update_table()
        if self.table.selection():
            cfm = Tk()
            width, height = cfm.winfo_screenwidth()/8, cfm.winfo_screenwidth()/16
            cfm.geometry('%dx%d+%d+%d' % (cfm.winfo_screenwidth()/8, cfm.winfo_screenwidth()/16, int((cfm.winfo_screenwidth() - width) / 2), int((cfm.winfo_screenheight() - height) / 2)))
            cfm.title("Confirmation")
            cfm.grid_rowconfigure(0, weight=1)
            cfm.grid_rowconfigure(1, weight=1)
            cfm.grid_rowconfigure(2, weight=1)
            cfm.grid_columnconfigure(0, weight=1)
            cfm.grid_columnconfigure(1, weight=4)
            cfm.grid_columnconfigure(2, weight=1)
            cfm.grid_columnconfigure(3, weight=4)
            cfm.grid_columnconfigure(4, weight=1)
                
            name = self.table.item(self.table.focus())['values'][0]

            confirmationMessage_label = Label(cfm, text="Are you sure to remove user?", font=("Arial", 10), justify='center')
            confirmationMessage_label.grid(row=0, column=0, columnspan=5, sticky='nsew')

            confirmationDetails_label = Label(cfm, text=f"Name: {name}", font=("Arial", 10), justify='center')
            confirmationDetails_label.grid(row=1, column=0, columnspan=5, sticky='nsew')

            confirmButton = Button(cfm, text="Yes", command=deleteUser, cursor="hand2", relief='groove')
            confirmButton.grid(row=2, column=1, sticky='nsew')

            closeButton = Button(cfm, text="Close", command=cfm.destroy, cursor="hand2", relief='groove')
            closeButton.grid(row=2, column=3, sticky='nsew')
            cfm.mainloop()
        else:
            self.temp_msg(message='PLEASE SELECT A USER')
    
    def temp_msg(self, message):
        self.selectUserFrame = tk.Frame(self.function_frame, bg="white")
        self.selectUserFrame.grid_propagate(False)
        self.selectUserFrame.grid_rowconfigure(0, weight=1)
        self.selectUserFrame.grid_columnconfigure(0, weight=1)
        self.selectUserFrame.grid(row=4, column=1, columnspan=2, sticky='nsew')
        label1 = Label(self.selectUserFrame, text=message, font=("Helvetica", int(self.get_window_size()//30), 'bold'), bg='white')
        label1.grid(row=0, column=0)
        
        self.selectUserFrame.after(5000, self.selectUserFrame.destroy)
