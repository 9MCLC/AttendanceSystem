from tkinter import *
import tkinter as tk
from tkinter import ttk
import cv2
from pyzbar.pyzbar import decode
import requests
import qrcode
from datetime import datetime
import json
from PIL import Image, ImageTk
import os

class App:
    def __init__(self, window, window_title):
        self.apiEndpoint = "http://210.186.31.209:5000"

        self.window = window
        self.window.title(window_title)

        self.barcode_data = None
        self.video_source = 0

        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas_width = int(self.window.winfo_screenwidth() / 2) - 20
        self.canvas_height = self.window.winfo_screenheight() - 20

        self.canvas = Canvas(window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        registerButton = Button(window, text="Register", command=register_Page)
        registerButton.place(x=1115, y=290, width=150)

        manualAttendanceButton = Button(window, text="Manual Attendance", command=manualAttendance_Page)
        manualAttendanceButton.place(x=1115, y=330, width=150)

        delUserButton = Button(window, text="Remove User", command=delUser_Page)
        delUserButton.place(x=1115, y=370, width=150)

        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        
        barcodes = decode(frame)
        if barcodes:
            for barcode in barcodes:
                if self.barcode_data != barcode.data.decode('utf-8'):
                    self.barcode_data = barcode.data.decode('utf-8')
                    print(self.barcode_data)
                    verifyUser_label = Label(self.window, text="Verifying User", font=("Helvetica", 25))
                    verifyUser_label.place(x=0, y=0)
                    validUser = requests.get(f'{self.apiEndpoint}/validateUser', params={'UUID': self.barcode_data})
                    rResult = validUser.json()
                    if rResult.get('isExist') == True:
                        UserInfo = rResult.get('result')
                        englishName = UserInfo[0].get('EnglishName')
                        chineseName = UserInfo[0].get('ChineseName')
                        birthDate = datetime.strptime(UserInfo[0].get('BirthDate'), "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")
                        verifyAttendance_label = Label(self.window, text=f"Verifying Attendance - {englishName}", font=("Helvetica", 25))
                        verifyUser_label.destroy()
                        verifyAttendance_label.place(x=0, y=0)
                        validAttendance = requests.get(f'{self.apiEndpoint}/validateAttendance', params={'UUID': self.barcode_data})
                        rrResult = validAttendance.json()
                        if rrResult.get('isExist') == False:
                            markAttendance_label = Label(self.window, text="Marking Attendance", font=("Helvetica", 25))
                            verifyAttendance_label.destroy()
                            markAttendance_label.place(x=0, y=0)
                            markAttendance = requests.post(f'{self.apiEndpoint}/attendance', json={'UUID': self.barcode_data, "englishName": englishName, "chineseName": chineseName, "birthDate": birthDate})
                            if markAttendance.status_code == 200:
                                attendanceMarked_label = Label(self.window, text=f"Attendance Marked Successfully - {englishName}", font=("Helvetica", 25))
                                markAttendance_label.destroy()
                                attendanceMarked_label.place(x=0, y=0)
                            else:
                                print(f'Attendance Marking Failed, Error Occured, please contact Admin.')
                        else:
                            attendanceTiming = rrResult.get("result")[0].get('TimeOfAttendance')
                            print(f'{englishName} - Attendance already marked at {datetime.strptime(attendanceTiming, "%a, %d %b %Y %H:%M:%S %Z").strftime("%H:%M:%S")}')
                    else:
                        print('QR Code is not a valid QR Code, if you did not register before, please register a new user.')

        self.window.after(1, self.update)

def main():
    win = Tk()
    win.geometry('%dx%d+0+0' % (win.winfo_screenwidth(), win.winfo_screenheight()))

    app = App(win, "Lobby")

    win.mainloop()


def register_Page():
    reg = Tk()
    width, height = reg.winfo_screenwidth(), reg.winfo_screenheight()
    reg.geometry('%dx%d+0+0' % (width,height))
    reg.title("Register")

    registerLabel = Label(reg, text="Register", font=("Helvetica", 20))
    registerLabel.pack()
    registerLabel.place(x=710, y=150)

    engName_label = Label(reg, text="English Name:", font=("Helvetica", 12))
    engName_label.pack()
    engName_label.place(x=500, y=250)

    engName_entry = Entry(reg)
    engName_entry.pack()
    engName_entry.place(x=650, y=250, width=250)

    chiName_label = Label(reg, text="Chinese Name:", font=("Helvetica", 12))
    chiName_label.pack()
    chiName_label.place(x=500, y=310)

    chiName_entry = Entry(reg)
    chiName_entry.pack()
    chiName_entry.place(x=650, y=310, width=250)

    dob_label = Label(reg, text="Date Of Birth:", font=("Helvetica", 12))
    dob_label.pack()
    dob_label.place(x=500, y=370)

    dob_entry = Entry(reg)
    dob_entry.pack()
    dob_entry.place(x=650, y=370, width=250)

    dob_label = Label(reg, text="(YYYY-MM-DD)", font=("Helvetica", 10))
    dob_label.pack()
    dob_label.place(x=920, y=370)    

    def registerNewUser():
        engName_input = engName_entry.get()
        chiName_input = chiName_entry.get()
        dob_input = dob_entry.get()
        
        if all([engName_input, chiName_input, dob_input]):
            body = {
                "englishName": engName_input,
                "chineseName": chiName_input,
                "birthDate": dob_input
            }

            registerUser = requests.post(f'http://210.186.31.209:5000/register', json=body)
            if registerUser.status_code == 200:
                rrResult = registerUser.json()
                newQR = qrcode.make(rrResult.get('UUID'))
                current_directory = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(current_directory, 'QR Codes', f'{engName_input}.png')
                newQR.save(file_path)

                sucess_label = Label(reg, text="Register Successfully", font=("Helvetica", 25))
                sucess_label.pack()
                sucess_label.place(x=0, y=0)

                engName_entry.delete(0, END)
                chiName_entry.delete(0, END)
                dob_entry.delete(0, END)
        else:
            fail_label = Label(reg, text="Some information arent inserted, please double check.", font=("Helvetica", 25))
            fail_label.pack()
            fail_label.place(x=0, y=0)

    submitButton = Button(reg, text="Submit", command=registerNewUser)
    submitButton.pack()
    submitButton.place(x=700, y=430, width=150)

    closeButton = Button(reg, text="close", command=reg.destroy)
    closeButton.place(x=630, y=700, width=300)

    reg.mainloop()

def manualAttendance_Page():
    mlatd = Tk()
    width, height = mlatd.winfo_screenwidth(), mlatd.winfo_screenheight()
    mlatd.geometry('%dx%d+0+0' % (width,height))
    mlatd.title("Manual Attendance")

    attendance_leftFrame = LabelFrame(mlatd, text="Attendance", font=("Helvetica", 15))
    attendance_leftFrame.grid(row=0, column=0)
    attendance_leftframelabel = Label(attendance_leftFrame, padx = 300, pady = 300)
    attendance_leftframelabel.pack()

    markAttendanceButton = Button(mlatd, text="Mark Attendance")
    markAttendanceButton.place(x=1000, y=300, width=200)

    unmarkAttendanceButton = Button(mlatd, text="Unmark Attendance")
    unmarkAttendanceButton.place(x=1000, y=350, width=200)

    closeButton = Button(mlatd, text="close", command=mlatd.destroy)
    closeButton.place(x=630, y=700, width=300)

    mlatd.mainloop()

def delUser_Page():
    du = Tk()
    width, height = du.winfo_screenwidth(), du.winfo_screenheight()
    du.geometry('%dx%d+0+0' % (width,height))
    du.title("Remove User")

    delUser_leftFrame = LabelFrame(du, text="All User", font=("Helvetica", 15))
    delUser_leftFrame.grid(row=0, column=0)
    delUser_leftframelabel = Label(delUser_leftFrame, padx = 300, pady = 300)
    delUser_leftframelabel.pack()

    deleteButton = Button(du, text="Remove User")
    deleteButton.place(x=1000, y=300, width=200)

    closeButton = Button(du, text="close", command=du.destroy)
    closeButton.place(x=630, y=700, width=300)

    du.mainloop()

main()