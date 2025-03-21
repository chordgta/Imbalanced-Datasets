from fileinput import filename
import re
from main import app
from flask import request
import json
from werkzeug.utils import secure_filename
import os
import time
import redis
from dataAnalyze import getFile
#from predict import getPredictData
# from db import addRecord
import pandas as pd
from flask import jsonify
from predict import Transformdata,predictXGB
import logging

UPLOAD_FOLDER = 'D:/毕设/Financial-Fraud-Predict-System-main/Financial-Fraud-Predict-System-main/finance-server/uploads'
ALLOWED_EXTENSIONS = {'csv','xls','xlsx','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Redis配置
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
CACHE_KEY = 'table_data_cache'
CACHE_EXPIRE_TIME = 3600  # 缓存过期时间，单位秒

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xls', 'xlsx'}


# 文件上传处理
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({
                'state': 'error',
                'msg': '没有文件被上传'
            })

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'state': 'error',
                'msg': '未选择文件'
            })

        if file and allowed_file(file.filename):
            # 安全的文件名
            filename = secure_filename(file.filename)
            # 保存文件
            file_path = os.path.join('./uploads', filename)
            file.save(file_path)

            # 验证文件是否可以被正确读取和处理
            try:
                df = pd.read_csv(file_path)
                # 检查必要的列是否存在
                required_columns = ['transTime', 'transType', 'amount', 'cityPopulation',
                                    'birthDate', 'merchantLat', 'merchantLong',
                                    'latitude', 'longitude']

                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    os.remove(file_path)  # 删除不符合要求的文件
                    return jsonify({
                        'state': 'error',
                        'msg': f'文件缺少必要的列: {", ".join(missing_columns)}'
                    })

                return jsonify({
                    'state': 'success',
                    'info': {
                        'filename': filename,
                        'rows': len(df)
                    }
                })

            except Exception as e:
                if os.path.exists(file_path):
                    os.remove(file_path)  # 删除处理失败的文件
                return jsonify({
                    'state': 'error',
                    'msg': f'文件处理失败: {str(e)}'
                })

        return jsonify({
            'state': 'error',
            'msg': '不支持的文件类型'
        })

    except Exception as e:
        return jsonify({
            'state': 'error',
            'msg': f'上传失败: {str(e)}'
        })




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

# @app.route('/getData',methods=['GET','POST'])
# def getData():
#     msg = {}
#     filename = request.args.get('filename')
#     account = request.args.get('account')
#     if(filename):
#         msg = getPredictData(filename)
#         addRecord(account,filename)
#         return json.dumps(msg)
#     msg['state'] = 'fail'
#     msg['msg'] = "请求失败"
#     return json.dumps(msg)


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # 添加详细的日志
        # print("收到的请求头:", request.headers)
        # print("收到的原始数据:", request.get_data())
        # 直接获取原始数据并解析
        raw_data = request.get_data()
        # print("收到的原始数据:", raw_data)
        # 首先尝试直接获取json
        data = request.get_json(silent=True)
        if data is None:
            # 如果直接获取失败，尝试手动解析原始数据
            data = json.loads(raw_data.decode('utf-8'))


        if not data:
            return jsonify({
                'state': 'error',
                'msg': '没有接收到数据'
            })

        newdata = Transformdata(data)

        # 使用模型进行预测
        preresult = predictXGB(newdata)
        # print(preresult)
        # 示例返回结果
        formatted_result = {
            'predictions': preresult['predictions'].tolist(),  # 转换为Python列表
            'predictions_proba': preresult['predictions_proba'].tolist()[0]  # 获取概率值并转换为列表
        }

        return jsonify({
            'state': 'success',
            'result': {
                'predictions': formatted_result['predictions'],
                'predictions_proba': formatted_result['predictions_proba'],
                'fraud_probability': formatted_result['predictions_proba'][1]  # 欺诈概率
            }
        })

    except Exception as e:
        print("6666")
        return jsonify({
            'state': 'error',
            'msg': f"分析错误: {str(e)}"
        }), 500

@app.route('/getTableData', methods=['GET'])
def get_table_data():
    try:
        # 检查是否使用缓存
        use_cache = request.args.get('useCache', 'true').lower() == 'true'
        
        # 如果使用缓存且缓存存在，则返回缓存数据
        if use_cache:
            cached_data = redis_client.get(CACHE_KEY)
            if cached_data:
                return jsonify({
                    'state': 'success',
                    'data': json.loads(cached_data),
                    'from_cache': True
                })

        # 如果不使用缓存或缓存不存在，则读取CSV文件
        df = pd.read_csv('./uploads/RandomTest3.csv')
        if df.empty:
            print("CSV 文件为空")

        # 定义列映射关系（CSV文件的列名 -> 表格显示的列名）
        column_mapping = {
            'trans_date_trans_time': 'transTime',  # CSV中的交易时间列名
            'category': 'transType',  # CSV中的交易类型列名
            'amt': 'amount',  # CSV中的交易金额列名
            'last': 'lastName',  # CSV中的姓列名
            'first': 'firstName',  # CSV中的名列名
            'gender': 'gender',  # CSV中的性别列名
            'long': 'longitude',  # CSV中的经度列名
            'lat': 'latitude',  # CSV中的纬度列名
            'city_pop': 'cityPopulation',  # CSV中的城市人口列名
            'dob': 'birthDate',  # CSV中的出生年月列名
            'merch_long': 'merchantLong',  # CSV中的商家经度列名
            'merch_lat': 'merchantLat'  # CSV中的商家纬度列名
        }

        # 只选择需要的列
        selected_columns = list(column_mapping.keys())
        df_selected = df[selected_columns]

        # 重命名列
        df_selected = df_selected.rename(columns=column_mapping)

        # 转换为字典列表
        data = df_selected.to_dict('records')

        # 将数据存入Redis缓存
        redis_client.setex(CACHE_KEY, CACHE_EXPIRE_TIME, json.dumps(data))

        return jsonify({
            'state': 'success',
            'data': data,
            'from_cache': False
        })
    except redis.RedisError as e:
        print(f"Redis错误: {str(e)}")
        # Redis错误时仍然返回数据，但不缓存
        return get_table_data_without_cache()
    except Exception as e:
        print(f"数据处理错误: {str(e)}")
        return jsonify({
            'state': 'error',
            'msg': f"数据处理错误: {str(e)}"
        }), 500

def get_table_data_without_cache():
    """在Redis不可用时的备用方法"""
    try:
        df = pd.read_csv('./uploads/RandomTest2.csv')
        if df.empty:
            print("CSV 文件为空")

        # column_mapping = {
        #     'trans_date_trans_time': 'transTime',
        #     'category': 'transType',
        #     'amt': 'amount',
        #     'last': 'lastName',
        #     'first': 'firstName',
        #     'gender': 'gender',
        #     'long': 'longitude',
        #     'lat': 'latitude',
        #     'city_pop': 'cityPopulation',
        #     'dob': 'birthDate',
        #     'merch_long': 'merchantLong',
        #     'merch_lat': 'merchantLat'
        # }
        #
        # selected_columns = list(column_mapping.keys())
        # df_selected = df[selected_columns]
        # df_selected = df_selected.rename(columns=column_mapping)
        # data = df_selected.to_dict('records')
        data = BackData(df)
        return jsonify({
            'state': 'success',
            'data': data,
            'from_cache': False
        })
    except Exception as e:
        return jsonify({
            'state': 'error',
            'msg': f"数据处理错误: {str(e)}"
        }), 500


@app.route('/getFraudData', methods=['GET'])
def get_fraud_data():
    try:
        filename = request.args.get('filename')
        print(filename)
        if not filename:
            return jsonify({
                'state': 'error',
                'msg': '未提供文件名'
            })

        file_path = os.path.join('./uploads', filename)
        if not os.path.exists(file_path):
            return jsonify({
                'state': 'error',
                'msg': '文件不存在'
            })

        # 读取CSV文件
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            return jsonify({
                'state': 'error',
                'msg': f'文件读取失败: {str(e)}'
            })
        column_mapping = [
            'transTime',  # CSV中的交易时间列名
            'transType',  # CSV中的交易类型列名
            'amount',  # CSV中的交易金额列名
            'lastName',  # CSV中的姓列名
            'firstName',  # CSV中的名列名
             'gender',  # CSV中的性别列名
            'longitude',  # CSV中的经度列名
         'latitude',  # CSV中的纬度列名
             'cityPopulation',  # CSV中的城市人口列名
            'birthDate',  # CSV中的出生年月列名
             'merchantLong',  # CSV中的商家经度列名
             'merchantLat'  # CSV中的商家纬度列名
        ]

        # 只选择需要的列
        # selected_columns = list(column_mapping.keys())
        df_selected = df[column_mapping]

        # 重命名列
        # df_selected = df_selected.rename(columns=column_mapping)

        # 转换为字典列表
        data = df_selected.to_dict('records')
        # 数据转换
        transformed_data = Transformdata(df)
        if transformed_data is None:
            return jsonify({
                'state': 'error',
                'msg': '数据转换失败'
            })

        prediction_result = predictXGB(transformed_data)

        # 检查是否有错误
        if 'error' in prediction_result:
            return jsonify({
                'state': 'error',
                'msg': prediction_result['error']
            })

        # 获取预测结果
        predictions = prediction_result['predictions']
        probabilities = prediction_result['predictions_proba']

        # 获取欺诈数据
        fraud_mask = predictions == 1
        fraud_indices = fraud_mask.nonzero()[0]
        # 获取原始数据中的欺诈记录
        fraud_data = df.iloc[fraud_indices].to_dict('records')
        # 添加欺诈概率
        for i, row in enumerate(fraud_data):
            row['fraudProbability'] = float(probabilities[fraud_indices[i]][1])
            # 定义列映射关系（CSV文件的列名 -> 表格显示的列名）

        print(data)
        return jsonify({
            'state': 'success',
            'totalCount': len(df),
            'fraudCount': len(fraud_data),
            'fraudData': fraud_data,
            'allData': data
        })

    except Exception as e:
        print("处理过程中发生错误:", str(e))
        return jsonify({
            'state': 'error',
            'msg': f'处理失败: {str(e)}'
        }), 500

def BackData(df):
    column_mapping = {
        'trans_date_trans_time': 'transTime',
        'category': 'transType',
        'amt': 'amount',
        'last': 'lastName',
        'first': 'firstName',
        'gender': 'gender',
        'long': 'longitude',
        'lat': 'latitude',
        'city_pop': 'cityPopulation',
        'dob': 'birthDate',
        'merch_long': 'merchantLong',
        'merch_lat': 'merchantLat'
    }

    selected_columns = list(column_mapping.keys())
    df_selected = df[selected_columns]
    df_selected = df_selected.rename(columns=column_mapping)
    data = df_selected.to_dict('records')

    return data


# @app.route('/getLoanData', methods=['GET', 'POST'])
# def getLoanData():
#     msg = {}
#     filename = request.args.get('filename')
#     if(filename):
#         msg['info'] = getLoanAmount(filename)
#         msg['state'] = 'success'
#         return json.dumps(msg)
#     msg['state'] = 'fail'
#     msg['msg'] = "请求失败"
#     return json.dumps(msg)
#
# @app.route('/getEmpData', methods=['GET', 'POST'])
# def getEmpData():
#     msg = {}
#     filename = request.args.get('filename')
#     if(filename):
#         msg['info'] = getEmpAmount(filename)
#         msg['state'] = 'success'
#         return json.dumps(msg)
#     msg['state'] = 'fail'
#     msg['msg'] = "请求失败"
#     return json.dumps(msg)
#
# @app.route('/getGradeData', methods=['GET', 'POST'])
# def getGradeData():
#     msg = {}
#     filename = request.args.get('filename')
#     if(filename):
#         msg['info'] = getGradeAmount(filename)
#         msg['state'] = 'success'
#         return json.dumps(msg)
#     msg['state'] = 'fail'
#     msg['msg'] = "请求失败"
#     return json.dumps(msg)
#
# @app.route('/getPredictRes',methods=['GET','POST'])
# def getPredictRes():
#     msg = {}
#     filename = request.args.get('filename')
#     account = request.args.get('account')
#     if(filename):
#         msg = getPredictData(filename)
#         addRecord(account,filename)
#         return json.dumps(msg)
#     msg['state'] = 'fail'
#     msg['msg'] = "请求失败"
#     return json.dumps(msg)
    
    

