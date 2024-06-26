from tkinter import *
import tkinter as tk
from tkinter import ttk
import cv2
from pyzbar.pyzbar import decode
import requests
import qrcode
from datetime import datetime
from PIL import Image, ImageTk
import os
import re

# env = input('input your env: "dev or prod" ')
# if env == 'dev':
#     port = 5001
# elif env == 'prod':
#     port = 5000

apiEndpoint = f"http://192.168.0.119:{5000}"
# apiEndpoint = f"http://124.13.168.178:{5000}"


class Lobby:
    def __init__(self):
        self.window = Tk()
        self.window.title("Lobby")
        self.window.geometry('%dx%d+0+0' % (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=4)
        self.window.grid_rowconfigure(0, weight=2)
        self.window.grid_rowconfigure(1, weight=8)
        self.window.minsize(800, 400)
        self.window.grid_propagate(False)
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
        Lobby()

    def LaunchRegistration(self):
        self.window.destroy()
        Registration()

    def LaunchNameList(self):
        self.window.destroy()
        NameList()

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

        self.title_label = tk.Label(self.pageTitleFrame, text="LOBBY", font=("Helvetica", self.get_window_size()//15, 'bold'), anchor=W, bg='white')
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
            text_bold_font = ("Helvetica", window_size//30, "bold")
            self.QRTextLabel.config(font=text_bold_font)
        
        self.function_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid")
        self.function_frame.grid(row=1, column=1, sticky="nsew")
        self.function_frame.grid_propagate(False)

        self.function_frame.grid_columnconfigure(0, weight=15)
        self.function_frame.grid_columnconfigure(1, weight=20)
        self.function_frame.grid_columnconfigure(2, weight=10)
        self.function_frame.grid_columnconfigure(3, weight=40)
        self.function_frame.grid_columnconfigure(4, weight=15)
        self.function_frame.grid_rowconfigure(0, weight=10)
        self.function_frame.grid_rowconfigure(1, weight=10)
        self.function_frame.grid_rowconfigure(2, weight=10)
        self.function_frame.grid_rowconfigure(3, weight=65)
        self.function_frame.grid_rowconfigure(4, weight=5)

        self.textFrame = tk.Frame(self.function_frame, bg="white", bd=2, relief="solid")
        self.QRFrame = tk.Frame(self.function_frame, bg="white", bd=2, relief="solid")
        self.infoFrame = tk.Frame(self.function_frame, bg="white", bd=2, relief="solid")
        self.textFrame.grid_propagate(False)
        self.QRFrame.grid_propagate(False)
        self.infoFrame.grid_propagate(False)


        self.textFrame.grid(row=1, column=1, sticky='nsew')
        self.QRFrame.grid(row=3,column=1,sticky='nsew')
        self.infoFrame.grid(row=1, column=3, rowspan=3, sticky='nsew')

        self.QRTextLabel = tk.Label(self.textFrame, text="SHOW QR HERE", font=("Helvetica", self.get_window_size(), 'bold'), anchor="center", bg='white')
        self.QRTextLabel.pack(expand=True, fill="both")

        self.QRFrame.grid_propagate(False)
        self.canvas = Canvas(self.QRFrame)
        self.canvas.grid(sticky='nsew')

        self.QRFrame.grid_rowconfigure(0, weight=1)
        self.QRFrame.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.infoFrame.grid_rowconfigure(0, weight=1)
        self.infoFrame.grid_columnconfigure(0, weight=1)

        self.video_source = 1
        self.vid = cv2.VideoCapture(self.video_source)
        self.function_frame.bind("<Configure>", update_function)
        self.UUIDCooldown = []
        self.update()

    def show_success_label(self, name="Yew Hong Yin"):
        self.successInfoFrame = tk.Frame(self.infoFrame, bg="white")
        self.successInfoFrame.grid_rowconfigure(0, weight=4)
        self.successInfoFrame.grid_rowconfigure(1, weight=2)
        self.successInfoFrame.grid_rowconfigure(2, weight=2)
        self.successInfoFrame.grid_rowconfigure(3, weight=2)
        self.successInfoFrame.grid_columnconfigure(0, weight=1)
        self.successInfoFrame.grid(row=0, column=0, sticky='nsew')
        image = Image.open("./Checkmark.png")
        image.thumbnail((int(self.successInfoFrame.winfo_width()*200), int(self.infoFrame.winfo_width()*200)))
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(self.successInfoFrame, image=image, bg='white', anchor='n')
        image_label.image = image

        image_label.grid(row=0, column=0)

        label1 = Label(self.successInfoFrame, text="Attendance Marked\nSuccessfully", font=("Helvetica", int(self.get_window_size()//40)), bg='white')
        label1.grid(row=1, column=0)

        label2 = Label(self.successInfoFrame, text="WELCOME", font=("Helvetica", int(self.get_window_size()//40)), bg='white')
        label2.grid(row=2, column=0)

        label3 = Label(self.successInfoFrame, text=name, font=("Helvetica", int(self.get_window_size()//40)), bg='white')
        label3.grid(row=3, column=0)

        self.successInfoFrame.after(5000, self.successInfoFrame.destroy)

    def show_fail_label(self, message="Failed", name="YHY", time=None):
        self.failInfoFrame = tk.Frame(self.infoFrame, bg="white")

        if message == "Failed":
            self.failInfoFrame.grid_rowconfigure(0, weight=4)
            self.failInfoFrame.grid_rowconfigure(1, weight=6)
            self.failInfoFrame.grid_columnconfigure(0, weight=1)
            self.failInfoFrame.grid(row=0, column=0, sticky='nsew')
            image = Image.open("./Cross.png")
            image.thumbnail((int(self.failInfoFrame.winfo_width()*200), int(self.failInfoFrame.winfo_width()*200)))
            image = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.failInfoFrame, image=image, bg='white', anchor='n')
            image_label.image = image

            image_label.grid(row=0, column=0)
            label1 = Label(self.failInfoFrame, text="Attendance Marking Failed\nError Occured\nPlease contact Admin.", font=("Helvetica", int(self.get_window_size()//40)), bg='white')
            label1.grid(row=1, column=0)

            label2 = Label(self.failInfoFrame, text=name, font=("Helvetica", int(self.get_window_size()//40)), bg='white')
            label2.grid(row=2, column=0)
            self.failInfoFrame.after(5000, self.failInfoFrame.destroy)
        elif message == "Marked":
            self.failInfoFrame.grid_rowconfigure(0, weight=4)
            self.failInfoFrame.grid_rowconfigure(1, weight=2)
            self.failInfoFrame.grid_rowconfigure(2, weight=2)
            self.failInfoFrame.grid_rowconfigure(3, weight=2)
            self.failInfoFrame.grid_columnconfigure(0, weight=1)
            self.failInfoFrame.grid(row=0, column=0, sticky='nsew')
            image = Image.open("./Cross.png")
            image.thumbnail((int(self.failInfoFrame.winfo_width()*200), int(self.failInfoFrame.winfo_width()*200)))
            image = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.failInfoFrame, image=image, bg='white', anchor='n')
            image_label.image = image

            image_label.grid(row=0, column=0)
            label1 = Label(self.failInfoFrame, text="Attendance Marked\nAlready At", font=("Helvetica", int(self.get_window_size()//40)), bg='white')
            label1.grid(row=1, column=0)

            label2 = Label(self.failInfoFrame, text=time, font=("Helvetica", int(self.get_window_size()//40)), bg='white')
            label2.grid(row=2, column=0)

            label3 = Label(self.failInfoFrame, text=name, font=("Helvetica", int(self.get_window_size()//40)), bg='white')
            label3.grid(row=3, column=0)
            self.failInfoFrame.after(5000, self.failInfoFrame.destroy)
        elif message == "Invalid":
            self.failInfoFrame.grid_rowconfigure(0, weight=4)
            self.failInfoFrame.grid_rowconfigure(1, weight=6)
            self.failInfoFrame.grid_columnconfigure(0, weight=1)
            self.failInfoFrame.grid(row=0, column=0, sticky='nsew')
            image = Image.open("./Cross.png")
            image.thumbnail((int(self.failInfoFrame.winfo_width()*200), int(self.failInfoFrame.winfo_width()*200)))
            image = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.failInfoFrame, image=image, bg='white', anchor='n')
            image_label.image = image

            image_label.grid(row=0, column=0)
            label1 = Label(self.failInfoFrame, text="QR Code is not valid", font=("Helvetica", int(self.get_window_size()//40)), bg='white')
            label1.grid(row=1, column=0)
            self.failInfoFrame.after(5000, self.failInfoFrame.destroy)

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).transpose(Image.FLIP_LEFT_RIGHT))
            self.canvas.create_image(self.QRFrame.winfo_width()/2, 0, image=self.photo, anchor=N)
            
        barcodes = decode(frame)
        if barcodes:
            for barcode in barcodes:
                uuid = barcode.data.decode('utf-8')
                if uuid not in self.UUIDCooldown:
                    self.startUUIDCooldown(uuid=uuid)
                    userExists = requests.get(f'{apiEndpoint}/getUser', params={'UUID': uuid})
                    userExistsResult = userExists.json()
                    if userExistsResult.get('rowCount') == 1:
                        UserInfo = userExistsResult.get('users')[0]
                        name = UserInfo.get('Name')
                        attendanceExists = requests.get(f'{apiEndpoint}/getAttendance', params={'UUID': uuid})
                        attendanceExistsResult = attendanceExists.json()
                        if attendanceExistsResult.get('rowCount') == 0:
                            markAttendance = requests.post(f'{apiEndpoint}/addAttendance', json={'UUID': uuid, "name": name})
                            if markAttendance.status_code == 200:
                                self.show_success_label(name=name)
                            else:
                                self.show_fail_label(message='Failed', name=name)
                        else:
                            attendanceTiming = attendanceExistsResult.get("result")[0].get('TimeOfAttendance')
                            self.show_fail_label(message='Marked', name=name, time=datetime.strptime(attendanceTiming, "%a, %d %b %Y %H:%M:%S %Z").strftime("%I:%M:%S %p"))
                    else:
                        self.show_fail_label(message='Invalid')   

        self.function_frame.after(20, self.update)

    def startUUIDCooldown(self, uuid):
        self.UUIDCooldown.append(uuid)
        self.window.after(10000, lambda: self.UUIDCooldown.remove(uuid))


class Registration:
    def __init__(self):
        self.window = Tk()
        self.window.title("REGISTRATION")
        self.window.geometry('%dx%d+0+0' % (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=4)
        self.window.grid_rowconfigure(0, weight=2)
        self.window.grid_rowconfigure(1, weight=8)
        self.window.minsize(800, 400)
        self.window.grid_propagate(False)
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

        self.window.mainloop()

    def LaunchLobby(self):
        self.window.destroy()
        Lobby()

    def LaunchRegistration(self):
        self.window.destroy()
        Registration()

    def LaunchNameList(self):
        self.window.destroy()
        NameList()

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

        self.title_label = tk.Label(self.pageTitleFrame, text="REGISTRATION", font=("Helvetica", self.get_window_size()//15, 'bold'), anchor=W, bg='white')
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
            entry_font = ("Helvetica", window_size//50)
            self.registerLabel.config(font=text_bold_font)
            self.name_Label.config(font=text_bold_font)
            self.phNumber_Label.config(font=text_bold_font)
            self.submitButton.config(font=("Helvetica", window_size//40, "bold"), width=window_size//60)
            self.name_Entry.config(font=entry_font)
            self.phNumber_Entry.config(font=entry_font)
            self.infoFrame.grid(row=0, column=3, rowspan=6, sticky='nsew', pady=int(self.get_window_size()//18))

        def ph_on_entry_click(event):
            if self.phNumber_Entry.get() == "(EG: 012-34567890)":
                self.phNumber_Entry.delete(0, "end")
                self.phNumber_Entry.config(fg='black')

        def ph_on_focus_out(event):
            if self.phNumber_Entry.get() == "":
                self.phNumber_Entry.insert(0, "(EG: 012-34567890)")
                self.phNumber_Entry.config(fg='gray')
        self.function_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid")
        self.function_frame.grid_propagate(False)
        self.function_frame.grid(row=1, column=1, sticky="nsew")
        self.function_frame.grid_rowconfigure(0, weight=10)
        self.function_frame.grid_rowconfigure(1, weight=12)
        self.function_frame.grid_rowconfigure(2, weight=3)
        self.function_frame.grid_rowconfigure(3, weight=12)
        self.function_frame.grid_rowconfigure(4, weight=3)
        self.function_frame.grid_rowconfigure(5, weight=3)
        self.function_frame.grid_rowconfigure(6, weight=8)
        self.function_frame.grid_columnconfigure(0, weight=1)
        self.function_frame.grid_columnconfigure(1, weight=4)
        self.function_frame.grid_columnconfigure(2, weight=1)
        self.function_frame.grid_columnconfigure(3, weight=4)
        self.function_frame.grid_columnconfigure(4, weight=1)
        self.function_frame.bind("<Configure>", update_function)
        
        self.infoFrame = tk.Frame(self.function_frame, bg="white", bd=2, relief="solid")
        self.infoFrame.grid_propagate(False)
        self.infoFrame.grid(row=0, column=3, rowspan=4, sticky='nsew', pady=int(self.get_window_size()//18))
        self.infoFrame.grid_rowconfigure(0, weight=1)
        self.infoFrame.grid_columnconfigure(0, weight=1)

        self.registerLabel = Label(self.function_frame, text="Register", font=("Helvetica", self.get_window_size()//15), bg='white')
        self.registerLabel.grid(row=0, column=1)

        self.name_Label = Label(self.function_frame, text="Name", font=("Helvetica", self.get_window_size()//20), bg='white')
        self.name_Label.grid(row=1, column=0, sticky='e')

        self.name_Entry = Entry(self.function_frame, relief='solid', font=("Helvetica", self.get_window_size()//20), justify='center')
        self.name_Entry.grid(row=1, column=1, sticky='nsew')

        self.phNumber_Label = Label(self.function_frame, text="Phone Number", font=("Helvetica", self.get_window_size()//20), bg='white')
        self.phNumber_Label.grid(row=3, column=0, sticky='e')

        self.phNumber_Entry = Entry(self.function_frame, relief='solid', fg='gray', font=("Helvetica", self.get_window_size()//20), justify='center')
        self.phNumber_Entry.insert(0, "(EG: 012-34567890)")
        self.phNumber_Entry.bind('<FocusIn>', ph_on_entry_click)
        self.phNumber_Entry.bind('<FocusOut>', ph_on_focus_out)
        self.phNumber_Entry.grid(row=3, column=1, sticky='nsew')

        self.submitButton = Button(self.function_frame, text="SUBMIT", command=self.Register, font=("Helvetica", self.get_window_size()//18, 'bold'), width=20, cursor="hand2", relief='groove')
        self.submitButton.grid(row=5, column=1)

    def Register(self):
        phNumberPattern = re.compile(r'^\d{3}-\d{7,8}$')
        name_Input = self.name_Entry.get()
        phNumber_Input = self.phNumber_Entry.get() if phNumberPattern.match(self.phNumber_Entry.get()) else None
        
        if all([name_Input, phNumber_Input]):
            body = {
                "name": name_Input,
                "phoneNumber": phNumber_Input
            }
            userExist = requests.get(f'{apiEndpoint}/getUser', params=body)
            if userExist.json().get('rowCount') == 0:
                registerUser = requests.post(f'{apiEndpoint}/addUser', json=body)
                if registerUser.status_code == 200:
                    registerUserResponse = registerUser.json()
                    self.newQR = qrcode.make(registerUserResponse.get('UUID'))
                    current_directory = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(current_directory, 'QR Codes', f'{name_Input}.png')
                    self.newQR.save(file_path)
                    self.success(name=name_Input)

                    self.name_Entry.delete(0, END)
                    self.phNumber_Entry.delete(0, END)
            else:
                self.show_fail_label(401)
        else:
            self.show_fail_label(422)

    def showQRCode(self, name):
        self.QRInfoFrame = tk.Frame(self.infoFrame, bg="white")
        self.QRInfoFrame.grid_rowconfigure(0, weight=4)
        self.QRInfoFrame.grid_rowconfigure(1, weight=2)
        self.QRInfoFrame.grid_columnconfigure(0, weight=1)
        self.QRInfoFrame.grid(row=0, column=0, sticky='nsew')
        self.QRImage = Image.open(f"./QR Codes/{name}.png")
        self.QRImage.thumbnail((int(self.QRInfoFrame.winfo_width()*300), int(self.QRInfoFrame.winfo_width()*300)))
        self.QRImage = ImageTk.PhotoImage(self.QRImage)
        self.QRImage_label = tk.Label(self.QRInfoFrame, image=self.QRImage, bg='white', anchor='n')
        self.QRImage_label.image = self.QRImage

        self.QRImage_label.grid(row=0, column=0)

        self.label1 = Label(self.QRInfoFrame, text=f"9MCLC\n{name}", font=("Helvetica", int(self.get_window_size()//40)), bg='white', wraplength=200)
        self.label1.grid(row=1, column=0)

        self.QRInfoFrame.after(60000, self.QRInfoFrame.destroy)

    def success(self, name="Yew Hong Yin"):
        self.showQRCode(name= name)
        self.show_success_label()

    def show_success_label(self):
        self.successInfoFrame = tk.Frame(self.function_frame, bg="white")
        self.successInfoFrame.grid_propagate(False)
        self.successInfoFrame.grid_rowconfigure(0, weight=4)
        self.successInfoFrame.grid_rowconfigure(1, weight=1)
        self.successInfoFrame.grid_rowconfigure(2, weight=2)
        self.successInfoFrame.grid_rowconfigure(3, weight=1)
        self.successInfoFrame.grid_columnconfigure(0, weight=1)
        self.successInfoFrame.grid(row=6, column=2, columnspan=3, rowspan=5, sticky='nsew')
        label1 = Label(self.successInfoFrame, text="REGISTER", font=("Helvetica", int(self.get_window_size()//30), 'bold'), bg='white')
        label1.grid(row=0, column=0)

        label2 = Label(self.successInfoFrame, text="SUCCESSFULLY", font=("Helvetica", int(self.get_window_size()//50), 'bold'), bg='white')
        label2.grid(row=2, column=0)

        # label2 = Label(self.successInfoFrame, text="QR HAS BEEN SENT TO YOUR WHATSAPP", font=("Helvetica", int(self.get_window_size()//50), 'bold'), bg='white')
        # label2.grid(row=2, column=0)
        
        self.successInfoFrame.after(5000, self.successInfoFrame.destroy)

    def show_fail_label(self, error=401):
        self.failInfoFrame = tk.Frame(self.function_frame, bg="white")
        self.failInfoFrame.grid_propagate(False)
        self.failInfoFrame.grid_rowconfigure(0, weight=4)
        self.failInfoFrame.grid_rowconfigure(1, weight=1)
        self.failInfoFrame.grid_rowconfigure(2, weight=2)
        self.failInfoFrame.grid_rowconfigure(3, weight=1)
        self.failInfoFrame.grid_columnconfigure(0, weight=1)
        self.failInfoFrame.grid(row=6, column=2, columnspan=3, rowspan=5, sticky='nsew')
        
        if error == 401:
            label1 = Label(self.failInfoFrame, text="REGISTER FAILED", font=("Helvetica", int(self.get_window_size()//30), 'bold'), bg='white')
            label1.grid(row=0, column=0)

            label2 = Label(self.failInfoFrame, text="USER ALREADY EXISTED", font=("Helvetica", int(self.get_window_size()//50), 'bold'), bg='white')
            label2.grid(row=2, column=0)
        elif error == 422:
            label1 = Label(self.failInfoFrame, text="REGISTER FAILED", font=("Helvetica", int(self.get_window_size()//40), 'bold'), bg='white')
            label1.grid(row=0, column=0)

            label2 = Label(self.failInfoFrame, text="INFORMATION INSERTED\nIN WRONG FORMAT", font=("Helvetica", int(self.get_window_size()//50), 'bold'), bg='white')
            label2.grid(row=2, column=0)
        
        self.failInfoFrame.after(5000, self.failInfoFrame.destroy)


class NameList:
    def __init__(self):
        self.window = Tk()
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
        Lobby()

    def LaunchRegistration(self):
        self.window.destroy()
        Registration()

    def LaunchNameList(self):
        self.window.destroy()
        NameList()

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

def main():
    app = Lobby()

main()