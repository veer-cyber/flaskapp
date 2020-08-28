import warnings
from datetime import timedelta

import os

from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = 'sessionData'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

class LoginVO(db.Model):
    __tablename__ = 'loginmaster'
    loginId = db.Column('loginid', db.Integer, primary_key=True, autoincrement=True)
    loginFirstname = db.Column('loginfirstname', db.String(100), nullable=False)
    loginSecondname = db.Column('loginsecondname', db.String(100), nullable=False)
    loginUsername = db.Column('loginusername', db.String(100), nullable=False)
    loginPassword = db.Column('loginpassword', db.String(100), nullable=False)

db.create_all()

@app.route('/')
def loginUser():

    return render_template('index.html')

@app.route('/user/createUser', methods=['GET'])
def createUser():

    return render_template('createRoom.html')

@app.route('/user/addUser', methods=['POST'])
def addUser():
    print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
    firstName = request.form['fname']
    secondName = request.form['sname']
    userName = request.form['uname']
    password = request.form['pass']

    loginVO = LoginVO()
    loginVO.loginFirstname = firstName
    loginVO.loginSecondname = secondName
    loginVO.loginUsername = userName
    loginVO.loginPassword = password
    print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
    db.session.add(loginVO)
    print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    db.session.commit()
    return redirect(url_for('loginUser'))

@app.route('/user/login', methods=['POST'])
def checkUser():
    print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
    userName = request.form['uname']
    password = request.form['password']

    loginVO = LoginVO()
    print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    loginList = loginVO.query.filter_by(loginUsername=userName, loginPassword=password).first()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(loginList)
    if loginList == None:
        return render_template('index.html', error="Username or Password is invalid")
    else:
        return render_template('chatArea.html')




if __name__ == '__main__':
    app.run()