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
# from registration import Registration
# from namelist import NameList

apiEndpoint = f"http://192.168.0.119:{5000}"
# apiEndpoint = f"http://124.13.168.178:{5000}"


class Lobby:
    def __init__(self, window=None):
        self.window = window if window else Tk()
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

        self.video_source = 0
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
