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

# port = None
# env = input('input your env: "dev or prod"')
# if env == 'dev':
#     port = 5001
# elif env == 'prod':
#     port = 5000

# apiEndpoint = f"http://60.48.85.4:{port}"
apiEndpoint = f"http://192.168.0.119:5001"

class App:
    def __init__(self, window, window_title):

        self.window = window
        self.window.title(window_title)

        self.barcode_data = None
        self.video_source = 0

        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas_width = int(self.window.winfo_screenwidth() / 2) - 20
        self.canvas_height = self.window.winfo_screenheight() - 20

        self.canvas = Canvas(window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.grid(row=0, column=0, pady=(((self.canvas_height)-(self.canvas_width/4*3))/2-40))

        registerButton = Button(window, text="Register", command=register_Page)
        registerButton.place(x=1115, y=290, width=150)

        manualAttendanceButton = Button(window, text="Name List", command=nameList_Page)
        manualAttendanceButton.place(x=1115, y=330, width=150)

        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((self.canvas_width,int(self.canvas_width /4*3))))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        
        barcodes = decode(frame)
        if barcodes:
            for barcode in barcodes:
                if self.barcode_data != barcode.data.decode('utf-8'):
                    self.barcode_data = barcode.data.decode('utf-8')
                    print(self.barcode_data)
                    verifyUser_label = Label(self.window, text="Verifying User", font=("Helvetica", 25))
                    verifyUser_label.place(x=0, y=0)
                    validUser = requests.get(f'{apiEndpoint}/validateUser', params={'UUID': self.barcode_data})
                    rResult = validUser.json()
                    if rResult.get('isExist') == True:
                        UserInfo = rResult.get('result')
                        englishName = UserInfo[0].get('EnglishName')
                        chineseName = UserInfo[0].get('ChineseName')
                        birthDate = datetime.strptime(UserInfo[0].get('BirthDate'), "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")
                        verifyAttendance_label = Label(self.window, text=f"Verifying Attendance - {englishName}", font=("Helvetica", 25))
                        verifyUser_label.destroy()
                        verifyAttendance_label.place(x=0, y=0)
                        validAttendance = requests.get(f'{apiEndpoint}/validateAttendance', params={'UUID': self.barcode_data})
                        rrResult = validAttendance.json()
                        if rrResult.get('isExist') == False:
                            markAttendance_label = Label(self.window, text="Marking Attendance", font=("Helvetica", 25))
                            verifyAttendance_label.destroy()
                            markAttendance_label.place(x=0, y=0)
                            markAttendance = requests.post(f'{apiEndpoint}/attendance', json={'UUID': self.barcode_data, "englishName": englishName, "chineseName": chineseName, "birthDate": birthDate})
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

    chiName_label = Label(reg, text="Phone Number:", font=("Helvetica", 12))
    chiName_label.pack()
    chiName_label.place(x=500, y=350)

    chiName_entry = Entry(reg)
    chiName_entry.pack()
    chiName_entry.place(x=650, y=350, width=250)

    chiName_label = Label(reg, text="(Example: XXX-XXXXXXXX)", font=("Helvetica", 10))
    chiName_label.pack()
    chiName_label.place(x=650, y=380)

    dob_label = Label(reg, text="Date Of Birth:", font=("Helvetica", 12))
    dob_label.pack()
    dob_label.place(x=500, y=450)

    dob_entry = Entry(reg)
    dob_entry.pack()
    dob_entry.place(x=650, y=450, width=250)

    dob_label = Label(reg, text="(Example: YYYY-MM-DD)", font=("Helvetica", 10))
    dob_label.pack()
    dob_label.place(x=650, y=480)    

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

            registerUser = requests.post(f'{apiEndpoint}/register', json=body)
            if registerUser.status_code == 200:
                rrResult = registerUser.json()
                newQR = qrcode.make(rrResult.get('UUID'))
                current_directory = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(current_directory, 'QR Codes', f'{engName_input}.png')
                newQR.save(file_path)

                sucess_label = Label(reg, text="Register Successfully", font=("Helvetica", 25))
                sucess_label.pack()
                sucess_label.place(x=620, y=550)

                engName_entry.delete(0, END)
                chiName_entry.delete(0, END)
                dob_entry.delete(0, END)
        else:
            fail_label = Label(reg, text="Some information arent inserted, please double check.", font=("Helvetica", 25))
            fail_label.pack()
            fail_label.place(x=380, y=550)

    submitButton = Button(reg, text="Submit", command=registerNewUser)
    submitButton.pack()
    submitButton.place(x=700, y=600, width=150)

    closeButton = Button(reg, text="close", command=reg.destroy)
    closeButton.place(x=630, y=700, width=300)

    reg.mainloop()

def nameList_Page():
    nl = Tk()
    width, height = nl.winfo_screenwidth(), nl.winfo_screenheight()
    nl.geometry('%dx%d+0+0' % (width,height))
    nl.title("Name List")

    nameList_leftFrame = LabelFrame(nl, text="Name List", font=("Helvetica", 15))
    nameList_leftFrame.grid(row=0, column=0)
    nameList_leftframelabel = Label(nameList_leftFrame, padx = 500, pady = 300)


    def create_table(data: list, searchCriteria: str = ''):
        def removeUser():
            def deleteUser():
                uuid = table.item(table.focus())['values'][3]
                requests.delete(f'{apiEndpoint}/removeUser', json={'UUID': uuid})
                cfm.destroy()
                nl.destroy()
                nameList_Page()
            if table.selection():
                cfm = Tk()
                width, height = cfm.winfo_screenwidth()/8, cfm.winfo_screenwidth()/16
                center_x, center_y = int((cfm.winfo_screenwidth() - width) / 2), int((cfm.winfo_screenheight() - height) / 2)
                cfm.geometry('%dx%d+%d+%d' % (width, height, center_x, center_y))
                cfm.title("Confirmation")
                
                name = table.item(table.focus())['values'][2]
                
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
                selectionWarning_label = Label(nl, text="Please select a user", font=("Arial", 10))
                selectionWarning_label.place(x=1000, y=500)

        def unAttendUser():
            def clearUser():
                uuid = table.item(table.focus())['values'][3]
                requests.delete(f'{apiEndpoint}/unmarkAttendance', json={'UUID': uuid})
                cfm.destroy()
            if table.selection():
                name = table.item(table.focus())['values'][2]
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
                pass

        def AttendUser():
            def addUser():
                uuid = table.item(table.focus())['values'][3]
                engName = table.item(table.focus())['values'][2]
                chiName = table.item(table.focus())['values'][1]
                dob = datetime.strptime(table.item(table.focus())['values'][0], "%d/%m/%Y").strftime("%Y-%m-%d")
                requests.post(f'{apiEndpoint}/attendance', json={'UUID': uuid, 'englishName': engName, 'chineseName': chiName, 'birthDate': dob})
                cfm.destroy()
            if table.selection():
                name = table.item(table.focus())['values'][2]
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
                pass
        
        def selectItem(a):
            pass
            

        def filterByName(data: list, target):
            if target == '':
                filtered_data = data
            else:
                filtered_data = [row for row in data if row["EnglishName"].lower().startswith(str(target.lower()))]

            return filtered_data

        def updateSearchCriteria(*args):
            nonlocal searchCriteria
            searchCriteria = search_entry.get().strip()
            update_table()

        def update_table():
            for row in table.get_children():
                table.delete(row)
            
            for row in filterByName(data, searchCriteria):
                table.insert("", "end", values=list(row.values()))
        
        table = ttk.Treeview(nameList_leftFrame, columns=list(data[0].keys()), show="headings", height=25)

        search_label = Label(nameList_leftFrame, text="Search:", font=("Helvetica", 12))
        search_label.place(x=500, y=550)

        search_entry = Entry(nameList_leftFrame)
        search_entry.place(x=650, y=550, width=250)
        search_entry.insert(0, searchCriteria)
        search_entry.bind("<KeyRelease>", updateSearchCriteria)

        removeButton = Button(nl, text="Remove User", command=removeUser)
        removeButton.place(x=1300, y=350, width=150)

        unAttendButton = Button(nl, text="Unattend", command=unAttendUser)
        unAttendButton.place(x=1300, y=400, width=150)

        AttendButton = Button(nl, text="Attend", command=AttendUser)
        AttendButton.place(x=1300, y=550, width=150)

        for col in data[0].keys():
            table.heading(col, text=col)
            table.column(col, anchor="center", width=300)
            table.bind('<ButtonRelease-1>', selectItem)
            
        update_table()

        table.pack()
    
    def reformatData(data:list):
        returnData = []
        for row in data:
            row['BirthDate'] = datetime.strptime(row['BirthDate'], "%a, %d %b %Y %H:%M:%S %Z").strftime("%d/%m/%Y")
            returnData.append(row)
        return returnData

    data = requests.get(f"{apiEndpoint}/showUser").json()
    formattedData = reformatData(data['response'])

    create_table(formattedData)

    nameList_leftframelabel.pack()

    closeButton = Button(nl, text="close", command=nl.destroy)
    closeButton.place(x=630, y=700, width=300)

    nl.mainloop()

main()