import cv2
from pyzbar.pyzbar import decode
import requests
import qrcode
from datetime import datetime
import os

def autoAttendanceMarking():
    cap = cv2.VideoCapture(0)
    barcode_data = None
    while True:
        # Read a frame from the webcam
        _, frame = cap.read()

        # Decode QR codes
        barcodes = decode(frame)

        # Display the frame
        cv2.imshow('Webcam QR Code Reader', frame)
        
        # Check for QR codes
        if barcodes:
            for barcode in barcodes:
                if barcode_data != barcode.data.decode('utf-8'):
                    barcode_data = barcode.data.decode('utf-8')
                    validUser = requests.get(f'http://192.168.0.118:5000/validateUser', params={'UUID': barcode_data})
                    rResult = validUser.json()
                    if rResult.get('isExist') == True:
                        UserInfo = rResult.get('result')
                        englishName = UserInfo[0].get('EnglishName')
                        chineseName = UserInfo[0].get('ChineseName')
                        birthDate = datetime.strptime(UserInfo[0].get('BirthDate'), "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")

                        validAttendance = requests.get(f'http://192.168.0.118:5000/validateAttendance', params={'UUID': barcode_data})
                        rrResult = validAttendance.json()
                        if rrResult.get('isExist') == False:
                            markAttendance = requests.post(f'http://192.168.0.118:5000/attendance', json={'UUID': barcode_data, "englishName": englishName, "chineseName": chineseName, "birthDate": birthDate})
                            if markAttendance.status_code == 200:
                                print(f'{englishName} - Attendance Marked Successfully')
                            else:
                                print(f'Attendance Marking Failed, Error Occured, please contact Admin.')
                        else:
                            attendanceTiming = rrResult.get("result")[0].get('TimeOfAttendance')
                            print(f'{englishName} - Attendance already marked at {datetime.strptime(attendanceTiming, "%a, %d %b %Y %H:%M:%S %Z").strftime("%H:%M:%S")}')
                    else:
                        print('QR Code is not a valid QR Code, if you did not register before, please register a new user.')
                    print(f"QR Code data: {barcode_data}")

        # Exit when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

def manualAttendance():
    UserID = input('UUID')
    englishName = input('englishName')
    chineseName = input('chineseName')
    
    markAttendance = requests.get(f'http://192.168.0.118:5000/attendance?uuid={UserID}&englishname={englishName}&chinesename={chineseName}')
    if markAttendance.status_code == 200:
        print(f'{englishName} - Attendance Marked Successfully')
    else:
        print(f'Attendance Marking Failed, Error Occured, please contact Admin.')

def registerNewUser():
    englishName = input('englishName')
    chineseName = input('chineseName')
    birthDate = input('BirthDate Format: YYYY-MM-DD')
    
    if englishName and chineseName and birthDate:
        validRegistration = requests.get(f'http://192.168.0.118:5000/validateRegistration', params={"englishName": englishName, "chineseName": chineseName, "birthDate": birthDate})
        rResult = validRegistration.json()
        if rResult.get('isExist') == True:
            print('User is already a registered user, please refer to this QR Code for your future use. Thanks!')
        else:
            body = {
                "englishName": englishName,
                "chineseName": chineseName,
                "birthDate": birthDate
            }
            registerUser = requests.post(f'http://192.168.0.118:5000/register', json=body)
            rrResult = registerUser.json()
            print(rrResult)
            newQR = qrcode.make(rrResult.get('UUID'))
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, 'QR Codes', f'{englishName}.png')
            newQR.save(file_path)
            if rrResult.get('isSuccess') is not None and rrResult.get('isSuccess'):
                print('User registered, please take a photo of this QR Code, for future purposes test, if you require a physical QR Code, please contact Office.')

def updateAttendanceList():
    users = requests.get("http://192.168.0.118:5000/showUser")
    attendance = requests.get("http://192.168.0.118:5000/showAllAttendance")

    usersList = users.json().get("Response")
    attendanceList = attendance.json().get("result")
    attendanceUUIDList = [User.get("UUID") for User in attendanceList]
    newUsersList = []
    for user in usersList:
        if user.get("UUID") in attendanceUUIDList:
            user["Attended"] = True
        else:
            user["Attended"] = False
        newUsersList.append(user)
    
    print(newUsersList)

if __name__ == "__main__":
    updateAttendanceList()