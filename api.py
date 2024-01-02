from flask import Flask
from flask import jsonify
import uuid
app = Flask(__name__)

@app.route('/showUser')
def showAllUser():
    '''
    Get all registered user
    '''
    statusCode = 200
    # Fetch all username from the UserInfo table
    returnMsg = {"StatusCode":statusCode}
    return jsonify(returnMsg)

@app.route('/validate/<string:UserID>/')
def ValidateUser(UserID:str=None):
    '''
    Get Username by UserID
    '''
    statusCode = 200
    # Fetch rows that contains UserID
    # If got result = valid user
    # Return the UserID and the UserName
    # Else return 404, User Not Found

    returnMsg = {"StatusCode":statusCode, "UserID":UserID, "Name":UserID}
    return jsonify(returnMsg)

@app.route('/register/<string:UserName>/')
def RegisterUser(UserName:str):
    '''
    Registers new User

    {Parse In User Name}
    '''
    statusCode = 200
    UserID = uuid.uuid4()
    # Insert rows to database
    # Generate a QR code that is scannable and result as UserID *If UserID is passed in.
    returnMsg = {"StatusCode":statusCode, "Name":UserName, "UserID":UserID}
    return jsonify(returnMsg)

@app.route('/remove/<string:UserName>/')
def removeUser(UserName:str):
    '''
    Deletes a user from server
    '''
    statusCode = 200
    # Delete rows to database
    # Generate a QR code that is scannable and result as UserID *If UserID is passed in.
    returnMsg = {"StatusCode":statusCode, "Name":UserName, }
    return jsonify(returnMsg)


@app.route('/attendance/<string:UserID>/')
def markAttendance(UserID:str):
    statusCode = 200
    # delete rows in attendance database
    returnMsg = {"StatusCode":statusCode, "UserID":UserID, "Name":UserID}
    return jsonify(returnMsg)

@app.route('/unmarkattendance/<string:UserID>/')
def unmarkAttendance(UserID):
    statusCode = 200
    # Insert rows to attendance database
    returnMsg = {"StatusCode":statusCode, "UserID":UserID, "Name":UserID}
    return jsonify(returnMsg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)