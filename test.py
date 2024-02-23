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
import time

port = 5000
# env = input('input your env: "dev or prod" ')
# if env == 'dev':
#     port = 5001
# elif env == 'prod':
#     port = 5000

# apiEndpoint = f"http://60.48.85.4:{port}"
apiEndpoint = f"http://192.168.0.119:{port}"


class Lobby:
    def __init__(self):
        self.window = Tk()
        self.window.title("Lobby")
        self.window.geometry('%dx%d+0+0' % (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=4)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_rowconfigure(2, weight=9)
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
        self.vid.release()

    def LaunchNameList(self):
        self.window.destroy()
        NameList()
        self.vid.release()

    def get_window_size(self):
        window_size = min(self.window.winfo_width(), self.window.winfo_height())
        return window_size

    def create_title_page(self):
        self.title_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid", height=self.window.winfo_height() * 0.2)

        def update_title(event=None):
            window_size = self.get_window_size()
            title_bold_font = ("Helvetica", window_size//15, "bold")
            name_bold_font = ("Helvetica", window_size//35, "bold", "underline")
            self.title_label.config(font=title_bold_font)
            self.name_label.config(font=name_bold_font, pady=window_size//18)
            self.border_frame.config(height=window_size//17)

        self.title_label = tk.Label(self.title_frame, text="LOBBY", font=("Helvetica", self.get_window_size()//15, 'bold'), anchor=W, bg='white')
        self.title_label.pack(side="left", expand=True, fill="both")

        self.name_label = tk.Label(self.title_frame, text="9MCLC", font=("Helvetica", self.get_window_size()//15, 'bold', "underline"), anchor=NE, bg='white', pady=self.get_window_size()//15)
        self.name_label.pack(side="right", expand=True, fill="both")

        self.border_frame = tk.Frame(self.window, bg="black", height=self.get_window_size()//17)
        self.border_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.title_frame.bind("<Configure>", update_title)

        self.title_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def create_toolbar(self):
        self.toolbar_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid", width=self.window.winfo_width() * 0.2)

        def update_toolbar(event=None):
            window_size = min(self.window.winfo_width(), self.window.winfo_height()) // 50
            bold_font = ("Helvetica", int(window_size//1.3), "bold")
            lobbyButton.config(font=bold_font, width=int(window_size//1.1))
            nameListButton.config(font=bold_font, width=int(window_size//1.1))
            registrationButton.config(font=bold_font, width=int(window_size//1.1))
            image = Image.open("./Logo.png")
            image.thumbnail((int(self.window.winfo_width() //10), int(self.window.winfo_width() //10)))
            image = ImageTk.PhotoImage(image)
            image_label.config(image=image)
            image_label.image = image

        self.toolbar_frame.bind("<Configure>", update_toolbar)

        lobbyButton = Button(self.toolbar_frame, text="LOBBY", command=self.LaunchLobby, font=("Helvetica", self.get_window_size()//18, 'bold'), width=150, cursor="hand2", relief='groove')
        lobbyButton.place(relx=0.5, rely=0.3, anchor="center")

        nameListButton = Button(self.toolbar_frame, text="NAME LIST", command=self.LaunchNameList, font=("Helvetica", self.get_window_size()//18, 'bold'), width=150, cursor="hand2", relief='groove')
        nameListButton.place(relx=0.5, rely=0.4, anchor="center")

        registrationButton = Button(self.toolbar_frame, text="REGISTRATION", command=self.LaunchRegistration, font=("Helvetica", self.get_window_size()//18, 'bold'), width=150, cursor="hand2", relief='groove')
        registrationButton.place(relx=0.5, rely=0.5, anchor="center")

        image = Image.open("./Logo.png")
        image.thumbnail((int(self.window.winfo_width() * 200), int(self.window.winfo_width() * 200)))
        image = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.toolbar_frame, image=image, bg='white')
        image_label.image = image

        image_label.place(relx=0.5, rely=0.9, anchor="s")
        
        self.toolbar_frame.grid(row=2, column=0, sticky="nsew")

    def create_function_frame(self):

        def update_function(event=None):
            window_size = self.get_window_size()
            text_bold_font = ("Helvetica", window_size//30, "bold")
            self.QRTextLabel.config(font=text_bold_font)
        
        self.function_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid")
        self.function_frame.grid(row=2, column=1, sticky="nsew")

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

        successButton = Button(self.function_frame, text="SUCCESS", command=self.show_success_label, font=("Helvetica", self.get_window_size()//18, 'bold'), width=15, cursor="hand2", relief='groove')
        successButton.place(relx=0, rely=0.3, anchor="center")

        nameListButton = Button(self.function_frame, text="FAIL", command=self.show_fail_label, font=("Helvetica", self.get_window_size()//18, 'bold'), width=15, cursor="hand2", relief='groove')
        nameListButton.place(relx=0, rely=0.4, anchor="center")


        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        self.function_frame.bind("<Configure>", update_function)
        self.UUIDCooldown = []
        self.update()

    def show_success_label(self, name="Yew Hong Yin"):
        self.infoFrame.grid_propagate(False)
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
        self.infoFrame.grid_propagate(False)

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
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_rowconfigure(2, weight=9)
        self.window.grid_propagate(False)
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
        self.title_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid", height=self.window.winfo_height() * 0.2)

        def update_title(event=None):
            window_size = self.get_window_size()
            title_bold_font = ("Helvetica", window_size//15, "bold")
            name_bold_font = ("Helvetica", window_size//35, "bold", "underline")
            self.title_label.config(font=title_bold_font)
            self.name_label.config(font=name_bold_font, pady=window_size//18)
            self.border_frame.config(height=window_size//17)

        self.title_label = tk.Label(self.title_frame, text="REGISTRATION", font=("Helvetica", self.get_window_size()//15, 'bold'), anchor=W, bg='white')
        self.title_label.pack(side="left", expand=True, fill="both")

        self.name_label = tk.Label(self.title_frame, text="9MCLC", font=("Helvetica", self.get_window_size()//15, 'bold', "underline"), anchor=NE, bg='white', pady=self.get_window_size()//15)
        self.name_label.pack(side="right", expand=True, fill="both")

        self.border_frame = tk.Frame(self.window, bg="black", height=self.get_window_size()//17)
        self.border_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.title_frame.bind("<Configure>", update_title)

        self.title_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def create_toolbar(self):
        self.toolbar_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid", width=self.window.winfo_width() * 0.2)

        def update_toolbar(event=None):
            window_size = min(self.window.winfo_width(), self.window.winfo_height()) // 50
            bold_font = ("Helvetica", int(window_size//1.3), "bold")
            lobbyButton.config(font=bold_font, width=int(window_size//1.1))
            nameListButton.config(font=bold_font, width=int(window_size//1.1))
            registrationButton.config(font=bold_font, width=int(window_size//1.1))
            image = Image.open("./Logo.png")
            image.thumbnail((int(self.window.winfo_width() //10), int(self.window.winfo_width() //10)))
            image = ImageTk.PhotoImage(image)
            image_label.config(image=image)
            image_label.image = image

        self.toolbar_frame.bind("<Configure>", update_toolbar)

        lobbyButton = Button(self.toolbar_frame, text="LOBBY", command=self.LaunchLobby, font=("Helvetica", self.get_window_size()//18, 'bold'), width=150, cursor="hand2", relief='groove')
        lobbyButton.place(relx=0.5, rely=0.3, anchor="center")

        nameListButton = Button(self.toolbar_frame, text="NAME LIST", command=self.LaunchNameList, font=("Helvetica", self.get_window_size()//18, 'bold'), width=150, cursor="hand2", relief='groove')
        nameListButton.place(relx=0.5, rely=0.4, anchor="center")

        registrationButton = Button(self.toolbar_frame, text="REGISTRATION", command=self.LaunchRegistration, font=("Helvetica", self.get_window_size()//18, 'bold'), width=150, cursor="hand2", relief='groove')
        registrationButton.place(relx=0.5, rely=0.5, anchor="center")

        image = Image.open("./Logo.png")
        image.thumbnail((int(self.window.winfo_width() * 200), int(self.window.winfo_width() * 200)))
        image = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.toolbar_frame, image=image, bg='white')
        image_label.image = image

        image_label.place(relx=0.5, rely=0.9, anchor="s")
        
        self.toolbar_frame.grid(row=2, column=0, sticky="nsew")

    def create_function_frame(self):
        def update_function(event=None):
            window_size = self.get_window_size()
            text_bold_font = ("Helvetica", window_size//40, "bold")
            entry_font = ("Helvetica", window_size//50)
            self.registerLabel.config(font=text_bold_font)
            self.name_Label.config(font=text_bold_font)
            self.phNumber_Label.config(font=text_bold_font)
            self.dob_Label.config(font=text_bold_font)
            self.submitButton.config(font=("Helvetica", window_size//40, "bold"), width=window_size//60)
            self.name_Entry.config(font=entry_font)
            self.phNumber_Entry.config(font=entry_font)
            self.dob_Entry.config(font=entry_font)

        def ph_on_entry_click(event):
            if self.phNumber_Entry.get() == "(EG: 012-34567890)":
                self.phNumber_Entry.delete(0, "end")
                self.phNumber_Entry.config(fg='black')

        def ph_on_focus_out(event):
            if self.phNumber_Entry.get() == "":
                self.phNumber_Entry.insert(0, "(EG: 012-34567890)")
                self.phNumber_Entry.config(fg='gray')
        
        def dob_on_entry_click(event):
            if self.dob_Entry.get() == "(EG: 2003-12-01)":
                self.dob_Entry.delete(0, "end")
                self.dob_Entry.config(fg='black')

        def dob_on_focus_out(event):
            if self.dob_Entry.get() == "":
                self.dob_Entry.insert(0, "(EG: 2003-12-01)")
                self.dob_Entry.config(fg='gray')
        self.function_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid")
        self.function_frame.grid(row=2, column=1, sticky="nsew")
        self.function_frame.grid_rowconfigure(0, weight=15)
        self.function_frame.grid_rowconfigure(1, weight=7)
        self.function_frame.grid_rowconfigure(2, weight=3)
        self.function_frame.grid_rowconfigure(3, weight=7)
        self.function_frame.grid_rowconfigure(4, weight=3)
        self.function_frame.grid_rowconfigure(5, weight=7)
        self.function_frame.grid_rowconfigure(6, weight=3)
        self.function_frame.grid_rowconfigure(7, weight=3)
        self.function_frame.grid_rowconfigure(8, weight=7)
        self.function_frame.grid_rowconfigure(9, weight=5)
        self.function_frame.grid_rowconfigure(10, weight=5)
        self.function_frame.grid_rowconfigure(11, weight=20)
        self.function_frame.grid_rowconfigure(12, weight=15)
        self.function_frame.grid_columnconfigure(0, weight=2)
        self.function_frame.grid_columnconfigure(1, weight=5)
        self.function_frame.grid_columnconfigure(2, weight=3)
        self.function_frame.grid_propagate(False)
        self.window.bind("<Configure>", update_function)

        successButton = Button(self.function_frame, text="SUCCESS", command=self.show_success_label, font=("Helvetica", self.get_window_size()//18, 'bold'), width=15, cursor="hand2", relief='groove')
        successButton.place(relx=0, rely=0.3, anchor="center")

        nameListButton = Button(self.function_frame, text="FAIL", command=self.show_fail_label, font=("Helvetica", self.get_window_size()//18, 'bold'), width=15, cursor="hand2", relief='groove')
        nameListButton.place(relx=0, rely=0.4, anchor="center")

        self.registerLabel = Label(self.function_frame, text="Register", font=("Helvetica", self.get_window_size()//15), bg='white')
        self.registerLabel.grid(row=0, column=0, columnspan=3)

        self.name_Label = Label(self.function_frame, text="Name", font=("Helvetica", self.get_window_size()//20), bg='white')
        self.name_Label.grid(row=1, column=0, sticky='e')

        self.name_Entry = Entry(self.function_frame, relief='solid', font=("Helvetica", self.get_window_size()//20), justify='left')
        self.name_Entry.grid(row=1, column=1, sticky='nsew')

        self.phNumber_Label = Label(self.function_frame, text="Phone Number", font=("Helvetica", self.get_window_size()//20), bg='white')
        self.phNumber_Label.grid(row=3, column=0, sticky='e')

        self.phNumber_Entry = Entry(self.function_frame, relief='solid', fg='gray', font=("Helvetica", self.get_window_size()//20), justify='left')
        self.phNumber_Entry.insert(0, "(EG: 012-34567890)")
        self.phNumber_Entry.bind('<FocusIn>', ph_on_entry_click)
        self.phNumber_Entry.bind('<FocusOut>', ph_on_focus_out)
        self.phNumber_Entry.grid(row=3, column=1, sticky='nsew')

        self.dob_Label = Label(self.function_frame, text="Date Of Birth", font=("Helvetica", self.get_window_size()//20), bg='white')
        self.dob_Label.grid(row=5, column=0, sticky='e')

        self.dob_Entry = Entry(self.function_frame, relief='solid', fg='gray', font=("Helvetica", self.get_window_size()//20), justify='left')
        self.dob_Entry.insert(0, "(EG: 2003-12-01)")
        self.dob_Entry.bind('<FocusIn>', dob_on_entry_click)
        self.dob_Entry.bind('<FocusOut>', dob_on_focus_out)
        self.dob_Entry.grid(row=5, column=1, sticky='nsew')

        self.submitButton = Button(self.function_frame, text="SUBMIT", command=self.Register, font=("Helvetica", self.get_window_size()//18, 'bold'), width=20, cursor="hand2", relief='groove')
        self.submitButton.grid(row=7, column=0, columnspan=3)

    def Register(self):
        phNumberPattern = re.compile(r'^\d{3}-\d{7,8}$')
        datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        name_Input = self.name_Entry.get()
        phNumber_Input = self.phNumber_Entry.get() if phNumberPattern.match(self.phNumber_Entry.get()) else None
        dob_Input = self.dob_Entry.get() if datePattern.match(self.dob_Entry.get()) else None
        
        if all([name_Input, phNumber_Input, dob_Input]):
            body = {
                "name": name_Input,
                "phoneNumber": phNumber_Input,
                "birthDate": dob_Input
            }
            userExist = requests.get(f'{apiEndpoint}/getUser', params=body)
            if userExist.json().get('rowCount') == 0:
                registerUser = requests.post(f'{apiEndpoint}/addUser', json=body)
                if registerUser.status_code == 200:
                    registerUserResponse = registerUser.json()
                    newQR = qrcode.make(registerUserResponse.get('UUID'))
                    current_directory = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(current_directory, 'QR Codes', f'{name_Input}.png')
                    newQR.save(file_path)
                    self.show_success_label()

                    self.name_Entry.delete(0, END)
                    self.phNumber_Entry.delete(0, END)
                    self.dob_Entry.delete(0, END)
            else:
                self.show_fail_label(401)
        else:
            self.show_fail_label(422)
    
    def show_success_label(self):
        self.successInfoFrame = tk.Frame(self.function_frame, bg="white")
        self.function_frame.grid_propagate(False)
        self.successInfoFrame.grid_rowconfigure(0, weight=4)
        self.successInfoFrame.grid_rowconfigure(1, weight=1)
        self.successInfoFrame.grid_rowconfigure(2, weight=2)
        self.successInfoFrame.grid_rowconfigure(3, weight=1)
        self.successInfoFrame.grid_columnconfigure(0, weight=1)
        self.successInfoFrame.grid(row=8, column=0, columnspan=3, rowspan=5, sticky='nsew')
        label1 = Label(self.successInfoFrame, text="REGISTER SUCCESSFULLY", font=("Helvetica", int(self.get_window_size()//30), 'bold'), bg='white')
        label1.grid(row=0, column=0)

        label2 = Label(self.successInfoFrame, text="QR HAS BEEN SENT TO YOUR WHATSAPP", font=("Helvetica", int(self.get_window_size()//50), 'bold'), bg='white')
        label2.grid(row=2, column=0)
        
        self.successInfoFrame.after(5000, self.successInfoFrame.destroy)

    def show_fail_label(self, error=401):
        self.failInfoFrame = tk.Frame(self.function_frame, bg="white")
        self.function_frame.grid_propagate(False)
        self.failInfoFrame.grid_rowconfigure(0, weight=4)
        self.failInfoFrame.grid_rowconfigure(1, weight=1)
        self.failInfoFrame.grid_rowconfigure(2, weight=2)
        self.failInfoFrame.grid_rowconfigure(3, weight=1)
        self.failInfoFrame.grid_columnconfigure(0, weight=1)
        self.failInfoFrame.grid(row=8, column=0, columnspan=3, rowspan=5, sticky='nsew')
        
        if error == 401:
            label1 = Label(self.failInfoFrame, text="REGISTER FAILED", font=("Helvetica", int(self.get_window_size()//30), 'bold'), bg='white')
            label1.grid(row=0, column=0)

            label2 = Label(self.failInfoFrame, text="USER ALREADY EXISTED", font=("Helvetica", int(self.get_window_size()//50), 'bold'), bg='white')
            label2.grid(row=2, column=0)
        elif error == 422:
            label1 = Label(self.failInfoFrame, text="REGISTER FAILED", font=("Helvetica", int(self.get_window_size()//40), 'bold'), bg='white')
            label1.grid(row=0, column=0)

            label2 = Label(self.failInfoFrame, text="INFORMATION INSERTED IN WRONG FORMAT", font=("Helvetica", int(self.get_window_size()//50), 'bold'), bg='white')
            label2.grid(row=2, column=0)
        
        self.failInfoFrame.after(5000, self.failInfoFrame.destroy)


class NameList:
    def __init__(self):
        self.window = Tk()
        self.window.title("NAMELIST")
        self.window.geometry('%dx%d+0+0' % (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=4)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_rowconfigure(2, weight=9)
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
        self.title_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid", height=self.window.winfo_height() * 0.2)

        def update_title(event=None):
            window_size = self.get_window_size()
            title_bold_font = ("Helvetica", window_size//15, "bold")
            name_bold_font = ("Helvetica", window_size//35, "bold", "underline")
            self.title_label.config(font=title_bold_font)
            self.name_label.config(font=name_bold_font, pady=window_size//18)
            self.border_frame.config(height=window_size//17)

        self.title_label = tk.Label(self.title_frame, text="NAMELIST", font=("Helvetica", self.get_window_size()//15, 'bold'), anchor=W, bg='white')
        self.title_label.pack(side="left", expand=True, fill="both")

        self.name_label = tk.Label(self.title_frame, text="9MCLC", font=("Helvetica", self.get_window_size()//15, 'bold', "underline"), anchor=NE, bg='white', pady=self.get_window_size()//15)
        self.name_label.pack(side="right", expand=True, fill="both")

        self.border_frame = tk.Frame(self.window, bg="black", height=self.get_window_size()//17)
        self.border_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.title_frame.bind("<Configure>", update_title)

        self.title_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def create_toolbar(self):
        self.toolbar_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid", width=self.window.winfo_width() * 0.2)

        def update_toolbar(event=None):
            window_size = min(self.window.winfo_width(), self.window.winfo_height()) // 50
            bold_font = ("Helvetica", int(window_size//1.3), "bold")
            lobbyButton.config(font=bold_font, width=int(window_size//1.1))
            nameListButton.config(font=bold_font, width=int(window_size//1.1))
            registrationButton.config(font=bold_font, width=int(window_size//1.1))
            image = Image.open("./Logo.png")
            image.thumbnail((int(self.window.winfo_width() //10), int(self.window.winfo_width() //10)))
            image = ImageTk.PhotoImage(image)
            image_label.config(image=image)
            image_label.image = image

        self.toolbar_frame.bind("<Configure>", update_toolbar)

        lobbyButton = Button(self.toolbar_frame, text="LOBBY", command=self.LaunchLobby, font=("Helvetica", self.get_window_size()//18, 'bold'), width=150, cursor="hand2", relief='groove')
        lobbyButton.place(relx=0.5, rely=0.3, anchor="center")

        nameListButton = Button(self.toolbar_frame, text="NAME LIST", command=self.LaunchNameList, font=("Helvetica", self.get_window_size()//18, 'bold'), width=150, cursor="hand2", relief='groove')
        nameListButton.place(relx=0.5, rely=0.4, anchor="center")

        registrationButton = Button(self.toolbar_frame, text="REGISTRATION", command=self.LaunchRegistration, font=("Helvetica", self.get_window_size()//18, 'bold'), width=150, cursor="hand2", relief='groove')
        registrationButton.place(relx=0.5, rely=0.5, anchor="center")

        image = Image.open("./Logo.png")
        image.thumbnail((int(self.window.winfo_width() * 200), int(self.window.winfo_width() * 200)))
        image = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.toolbar_frame, image=image, bg='white')
        image_label.image = image

        image_label.place(relx=0.5, rely=0.9, anchor="s")
        
        self.toolbar_frame.grid(row=2, column=0, sticky="nsew")

    def create_function_frame(self):
        function_frame = tk.Frame(self.window, bg="white", bd=2, relief="solid")
        function_label = tk.Label(function_frame, text="Function Frame", font=("Helvetica", 12), bg='white')
        function_label.pack(expand=True, fill="both")
        function_frame.grid(row=2, column=1, sticky="nsew")

def register_Page():
    reg = Tk()
    width, height = reg.winfo_screenwidth(), reg.winfo_screenheight()
    reg.geometry('%dx%d+0+0' % (width,height))
    def toggle_fullscreen(event = None):
        state = not reg.attributes('-fullscreen')
        reg.attributes('-fullscreen', state)

    def on_escape(event):
        reg.attributes('-fullscreen', False)
    reg.attributes('-fullscreen', True)

    reg.bind("<F11>", toggle_fullscreen)
    reg.bind("<Escape>", on_escape)
    reg.title("Register")

    registerLabel = Label(reg, text="Register", font=("Helvetica", 35))
    registerLabel.pack()
    registerLabel.place(relx= 0.5, rely=0.15, anchor=CENTER)

    name_Label = Label(reg, text="Name:", font=("Helvetica", 12))
    name_Label.pack()
    name_Label.place(relx= 0.35, rely=0.25, anchor=CENTER)

    name_Entry = Entry(reg)
    name_Entry.pack()
    name_Entry.place(relx= 0.5, rely=0.25, width=250, anchor=CENTER)

    phNumber_Label = Label(reg, text="Phone Number:", font=("Helvetica", 12))
    phNumber_Label.pack()
    phNumber_Label.place(relx= 0.35, rely=0.35, anchor=CENTER)

    phNumber_Entry = Entry(reg)
    phNumber_Entry.pack()
    phNumber_Entry.place(relx= 0.5, rely=0.35, width=250, anchor=CENTER)

    phNumber_Label2 = Label(reg, text="(Example: XXX-XXXXXXXX)", font=("Helvetica", 10))
    phNumber_Label2.pack()
    phNumber_Label2.place(relx= 0.5, rely=0.40, anchor=CENTER)

    dob_Label = Label(reg, text="Date Of Birth:", font=("Helvetica", 12))
    dob_Label.pack()
    dob_Label.place(relx= 0.35, rely=0.45, anchor=CENTER)

    dob_Entry = Entry(reg)
    dob_Entry.pack()
    dob_Entry.place(relx= 0.5, rely=0.45, width=250, anchor=CENTER)

    dob_Label2 = Label(reg, text="(Example: YYYY-MM-DD)", font=("Helvetica", 10))
    dob_Label2.pack()
    dob_Label2.place(relx= 0.5, rely=0.50, anchor=CENTER)    

    def registerNewUser():
        phNumberPattern = re.compile(r'^\d{3}-\d{7,8}$')
        datePattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        name_Input = name_Entry.get()
        phNumber_Input = phNumber_Entry.get() if phNumberPattern.match(phNumber_Entry.get()) else None
        dob_Input = dob_Entry.get() if datePattern.match(dob_Entry.get()) else None
        
        if all([name_Input, phNumber_Input, dob_Input]):
            body = {
                "name": name_Input,
                "phoneNumber": phNumber_Input,
                "birthDate": dob_Input
            }
            userExist = requests.get(f'{apiEndpoint}/getUser', params=body)
            if userExist.json().get('rowCount') == 0:
                registerUser = requests.post(f'{apiEndpoint}/addUser', json=body)
                if registerUser.status_code == 200:
                    registerUserResponse = registerUser.json()
                    newQR = qrcode.make(registerUserResponse.get('UUID'))
                    current_directory = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(current_directory, 'QR Codes', f'{name_Input}.png')
                    newQR.save(file_path)
                    show_temporary_label(reg, "Register Successfully")

                    name_Entry.delete(0, END)
                    phNumber_Entry.delete(0, END)
                    dob_Entry.delete(0, END)
            else:
                show_temporary_label(reg, "User already exist.")
        else:
            show_temporary_label(reg, "Information is not inserted in the correct format.")

    def show_temporary_label(window, message):
        label = Label(window, text=message, font=("Helvetica", 25))
        label.place(relx= 0.5, rely=0.7, anchor=CENTER)
        window.after(5000, label.destroy)

    submitButton = Button(reg, text="Submit", command=registerNewUser)
    submitButton.pack()
    submitButton.place(relx= 0.5, rely=0.55, width=150, anchor=CENTER)

    closeButton = Button(reg, text="Close", command=reg.destroy)
    closeButton.place(relx= 0.5, rely=0.60, width=300, anchor=CENTER)

    reg.mainloop()

def nameList_Page():
    nl = Tk()
    width, height = nl.winfo_screenwidth(), nl.winfo_screenheight()
    nl.geometry('%dx%d+0+0' % (width,height))
    nl.title("Name List")
    def toggle_fullscreen(event = None):
        state = not nl.attributes('-fullscreen')
        nl.attributes('-fullscreen', state)

    def on_escape(event):
        nl.attributes('-fullscreen', False)
    nl.attributes('-fullscreen', True)

    nl.bind("<F11>", toggle_fullscreen)
    nl.bind("<Escape>", on_escape)

    nameList_leftFrame = LabelFrame(nl, text="Name List", font=("Helvetica", 15))
    nameList_leftFrame.grid(row=0, column=0)
    nameList_leftframelabel = Label(nameList_leftFrame, padx = 500, pady = 300)

    def create_table(searchCriteria: str = ''):
        def show_temporary_label(message):
            label = Label(nl, text=message, font=("Helvetica", 25))
            label.place(x=620, y=550)
            nl.after(2000, label.destroy)
        def removeUser():
            def deleteUser():
                uuid = table.item(table.focus())['values'][4]
                requests.delete(f'{apiEndpoint}/removeUser', json={'UUID': uuid})
                cfm.destroy()
                update_table()
            if table.selection():
                cfm = Tk()
                width, height = cfm.winfo_screenwidth()/8, cfm.winfo_screenwidth()/16
                center_x, center_y = int((cfm.winfo_screenwidth() - width) / 2), int((cfm.winfo_screenheight() - height) / 2)
                cfm.geometry('%dx%d+%d+%d' % (width, height, center_x, center_y))
                cfm.title("Confirmation")
                
                name = table.item(table.focus())['values'][1]
                
                confirmationMessage_label = Label(cfm, text="Are you sure to remove user?", font=("Arial", 10))
                confirmationMessage_label.place(x=0, y=0)

                confirmationDetails_label = Label(cfm, text=f"Name: {name}", font=("Arial", 10))
                confirmationDetails_label.place(x=0, y=height/3)

                confirmButton = Button(cfm, text="Yes", command=deleteUser)
                confirmButton.place(x=0, y=height/3*2, width=width/2)
    
                closeButton = Button(cfm, text="Close", command=cfm.destroy)
                closeButton.place(x=width/2, y=height/3*2, width=width/2)
                cfm.mainloop()
            else:
                show_temporary_label("Please select a user")

        def unAttendUser():
            def clearUser():
                uuid = table.item(table.focus())['values'][4]
                requests.delete(f'{apiEndpoint}/removeAttendance', json={'UUID': uuid})
                cfm.destroy()
                update_table()
            if table.selection():
                name = table.item(table.focus())['values'][1]
                attended = table.item(table.focus())['values'][0]
                if attended == "No":
                    show_temporary_label("User is yet to be marked, you can't unmark an absent user")
                else:
                    cfm = Tk()
                    width, height = cfm.winfo_screenwidth()/8, cfm.winfo_screenwidth()/16
                    center_x, center_y = int((cfm.winfo_screenwidth() - width) / 2), int((cfm.winfo_screenheight() - height) / 2)
                    cfm.geometry('%dx%d+%d+%d' % (width, height, center_x, center_y))
                    cfm.title("Confirmation")

                    confirmationMessage_label = Label(cfm, text="Remove user's attendance", font=("Arial", 10))
                    confirmationMessage_label.place(x=0, y=0)

                    confirmationDetails_label = Label(cfm, text=f"Name: {name}", font=("Arial", 10))
                    confirmationDetails_label.place(x=0, y=30)

                    confirmButton = Button(cfm, text="Yes", command=clearUser)
                    confirmButton.place(x=0, y=60, width=width/2)

                    closeButton = Button(cfm, text="Close", command=cfm.destroy)
                    closeButton.place(x=width/2, y=60, width=width/2)
                    
                    cfm.mainloop()
            else:
                show_temporary_label("Please select a user")

        def AttendUser():
            def addUser():
                uuid = table.item(table.focus())['values'][4]
                Name = table.item(table.focus())['values'][1]
                requests.post(f'{apiEndpoint}/addAttendance', json={'UUID': uuid, 'name': Name})
                cfm.destroy()
                update_table()
            if table.selection():
                name = table.item(table.focus())['values'][1]
                attended = table.item(table.focus())['values'][0]
                if attended == "Yes":
                    show_temporary_label("User is already marked, you can't mark a marked user")
                else:
                    cfm = Tk()
                    width, height = cfm.winfo_screenwidth()/8, cfm.winfo_screenwidth()/16
                    center_x, center_y = int((cfm.winfo_screenwidth() - width) / 2), int((cfm.winfo_screenheight() - height) / 2)
                    cfm.geometry('%dx%d+%d+%d' % (width, height, center_x, center_y))
                    cfm.title("Confirmation")

                    confirmationMessage_label = Label(cfm, text="Mark user's attendance", font=("Arial", 10))
                    confirmationMessage_label.place(x=0, y=0)

                    confirmationDetails_label = Label(cfm, text=f"Name: {name}", font=("Arial", 10))
                    confirmationDetails_label.place(x=0, y=30)

                    confirmButton = Button(cfm, text="Yes", command=addUser)
                    confirmButton.place(x=0, y=60, width=width/2)

                    closeButton = Button(cfm, text="Close", command=cfm.destroy)
                    closeButton.place(x=width/2, y=60, width=width/2)
                    
                    cfm.mainloop()
            else:
                show_temporary_label("Please select a user")
        
        def updateSearchCriteria(*args):
                nonlocal searchCriteria
                searchCriteria = search_entry.get().strip()
                update_table()
        def update_table():
            def reformatData(data:list):
                returnData = []
                for row in data:
                    tempDict = {}
                    tempDict['Attended Today'] = row['Attended']
                    tempDict['Name'] = row['Name']
                    tempDict['PhoneNumber'] = row['PhoneNumber']
                    tempDict['BirthDate'] = row['BirthDate']
                    tempDict['UUID'] = row['UUID']
                    returnData.append(tempDict)
                return returnData
            def filterByName(data: list, target):
                if target == '':
                    filtered_data = data
                else:
                    filtered_data = [row for row in data if str(target.lower()) in row["Name"].lower()]

                return filtered_data
            data = requests.get(f"{apiEndpoint}/getTableData").json()
            formattedData = reformatData(data['users'])
            for row in table.get_children():
                table.delete(row)
            
            for col in formattedData[0].keys():
                table.heading(col, text=col)
                table.column(col, anchor="center", width=300)
            for row in filterByName(formattedData, searchCriteria):
                table.insert("", "end", values=list(row.values()))

        table = ttk.Treeview(nameList_leftFrame, columns=('Attended Today', 'Name', 'PhoneNumber', 'BirthDate', 'UUID'), show="headings", height=25)

        search_label = Label(nameList_leftFrame, text="Search:", font=("Helvetica", 12))
        search_label.place(x=500, y=550)

        search_entry = Entry(nameList_leftFrame)
        search_entry.place(relx=0.5, rely=0.5, width=250)
        search_entry.insert(0, searchCriteria)
        search_entry.bind("<KeyRelease>", updateSearchCriteria)

        removeButton = Button(nl, text="Remove User", command=removeUser)
        removeButton.place(relx=0.9, rely=0.2, width=150)

        unAttendButton = Button(nl, text="Unattend", command=unAttendUser)
        unAttendButton.place(relx=0.9, rely=0.3, width=150)

        AttendButton = Button(nl, text="Attend", command=AttendUser)
        AttendButton.place(relx=0.9, rely=0.4, width=150)

        update_table()

        table.pack()

    create_table()

    nameList_leftframelabel.pack()

    closeButton = Button(nl, text="close", command=nl.destroy)
    closeButton.place(x=630, y=700, width=300)

    nl.mainloop()

def main():
    app = Lobby()

main()