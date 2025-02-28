from fileinput import filename
import re
from main import app
from flask import request
import json
from werkzeug.utils import secure_filename
import os
import time
from dataAnalyze import getLoanAmount,getEmpAmount,getGradeAmount,getFile
from predict import getPredictData
from db import addRecord


UPLOAD_FOLDER = 'D:/毕设/Financial-Fraud-Predict-System-main/Financial-Fraud-Predict-System-main/finance-server/uploads'
ALLOWED_EXTENSIONS = {'csv','xls','xlsx','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    msg = {}
    print("-------",request.files)
    if('file' not in request.files):
        msg['state'] = 'fail'
        msg['msg'] = "文件获取失败"
        return json.dumps(msg)
    file = request.files['file']
    print("-------------",file)
    if(file.filename == ''):
        msg['state'] = 'fail'
        msg['msg'] = "文件获取失败"
        return json.dumps(msg)
    print("---------------",file.filename)
    if(file and allowed_file(file.filename)):
        print("-------------------------------------------")
        filename = secure_filename(file.filename)
        print(f"----------{filename}-------------")
        # save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # print('save_path',save_path)
        filename = re.sub(r'[^\w\.-]', '_', filename)
        file.save(f"{UPLOAD_FOLDER}/{filename}")
        msg['state'] = 'success'
        msg['info'] = {
            'filename':filename
        }
        return json.dumps(msg)
    msg['msg'] = 'fail'
    msg['msg'] = "请求错误"
    return json.dumps(msg)

@app.route('/getXGBoost',methods = ['GET','POST'])
def getXGBoost():
    msg = {}
    modelname = request.args.get('modelname')

    if(modelname):
        file = getFile(modelname)
        msg['path'] = '/XGBoostROC.png'
        msg['state'] = 'success'
        msg['AUC'] = file.at[0,'AUC']
        msg['Precision'] = file.at[0, 'Precision']
        msg['Recall'] = file.at[0, 'Recall']
        msg['F1Score'] = file.at[0, 'F1Score']
        return json.dumps(msg)

@app.route('/getData',methods=['GET','POST'])
def getData():
    msg = {}
    filename = request.args.get('filename')
    account = request.args.get('account')
    if(filename):
        msg = getPredictData(filename)
        addRecord(account,filename)
        return json.dumps(msg)
    msg['state'] = 'fail'
    msg['msg'] = "请求失败"
    return json.dumps(msg)


@app.route('/getLoanData', methods=['GET', 'POST'])
def getLoanData():
    msg = {}
    filename = request.args.get('filename')
    if(filename):
        msg['info'] = getLoanAmount(filename)
        msg['state'] = 'success'
        return json.dumps(msg)
    msg['state'] = 'fail'
    msg['msg'] = "请求失败"
    return json.dumps(msg)

@app.route('/getEmpData', methods=['GET', 'POST'])
def getEmpData():
    msg = {}
    filename = request.args.get('filename')
    if(filename):
        msg['info'] = getEmpAmount(filename)
        msg['state'] = 'success'
        return json.dumps(msg)
    msg['state'] = 'fail'
    msg['msg'] = "请求失败"
    return json.dumps(msg)

@app.route('/getGradeData', methods=['GET', 'POST'])
def getGradeData():
    msg = {}
    filename = request.args.get('filename')
    if(filename):
        msg['info'] = getGradeAmount(filename)
        msg['state'] = 'success'
        return json.dumps(msg)
    msg['state'] = 'fail'
    msg['msg'] = "请求失败"
    return json.dumps(msg)

@app.route('/getPredictRes',methods=['GET','POST'])
def getPredictRes():
    msg = {}
    filename = request.args.get('filename')
    account = request.args.get('account')
    if(filename):
        msg = getPredictData(filename)
        addRecord(account,filename)
        return json.dumps(msg)
    msg['state'] = 'fail'
    msg['msg'] = "请求失败"
    return json.dumps(msg)
    
    

