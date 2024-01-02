from tkinter import *
import cv2
from pyzbar.pyzbar import decode
import requests
import qrcode
from datetime import datetime
import json
from PIL import Image, ImageTk

def main():
    win = Tk()
    width, height = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry('%dx%d+0+0' % (width,height))
    win.title("Lobby")

    leftFrame = LabelFrame(win, text="Left Frame")
    leftFrame.grid(row=0, column=0)
    leftframelabel = Label(leftFrame, padx = 300, pady = 350)
    leftframelabel.pack()

# #Camera (Working on it) [Error: Lagged in UI]

 
#     vid = cv2.VideoCapture(0) 

#     width, height = 600, 800

#     vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
#     vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 



#     def open_camera(openCam): 
#         # Capture the video frame by frame 
#         _, frame = vid.read()
#         openCam = openCam
#         barcodes=decode(frame)

#         # Convert image from one color space to other 
#         opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

#         # Capture the latest frame and transform to image 
#         captured_image = Image.fromarray(opencv_image) 

#         # Convert captured image to photoimage 
#         photo_image = ImageTk.PhotoImage(image=captured_image) 

#         # Displaying photoimage in the label 
#         label_widget.photo_image = photo_image 

#         # Configure image in the label 
#         label_widget.configure(image=photo_image) 

#         # Repeat the same process after every 10 seconds 
#         label_widget.after(10, open_camera) 
#         return openCam


#     # Create a label and display it on app 
#     label_widget = Label(leftFrame)
#     label_widget.pack()
#     openCam = None
#     openCam = open_camera(openCam)

    def registerPage():
        register_Page()

    def manualAttendancePage():
        manualAttendance_Page()

    def delUserPage():
        delUser_Page()


    registerButton = Button(win, text="Register", command=register_Page)
    registerButton.place(x=1115, y=290, width=150)

    manualAttendanceButton = Button(win, text="Manual Attendance", command=manualAttendance_Page)
    manualAttendanceButton.place(x=1115, y=330, width=150)

    delUserButton = Button(win, text="Remove User", command=delUser_Page)
    delUserButton.place(x=1115, y=370, width=150)

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
    
        body = {
            "englishName": engName_input,
            "chineseName": chiName_input,
            "birthDate": dob_input
        }

        registerUser = requests.post(f'http://192.168.0.119:5000/register', json=body)
        if registerUser.status_code == 200:

            sucess_label = Label(reg, text="Register Successfully", font=("Helvetica", 25))
            sucess_label.pack()
            success_label.place(x=0, y=0)

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