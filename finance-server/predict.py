import pandas as pd
from dataAnalyze import getFile
import joblib
from joblib import load
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging
from joblib import load
import os

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ------------------- 预处理阶段 ---------------------

# def Grade2Value(x):
#     if(ord(x)>=65):
#         return ord('H')-ord(x)
#     return x.astype(int)

def predictXGB(newdata):
    try:

        # 加载模型
        loaded_model = load('./uploads/XGBoostModel.joblib')
        # loaded_model = load('./uploads/XGBoost.joblib')

        logging.info("模型加载成功")

        # 检查输入数据
        if not isinstance(newdata, (np.ndarray, list, pd.DataFrame)):
            raise ValueError("输入数据格式不正确，应为 numpy 数组、列表或 DataFrame")

        # 使用加载的模型进行预测
        predictions = loaded_model.predict(newdata)  # 预测类别
        predictions_proba = loaded_model.predict_proba(newdata)  # 预测概率

        # 输出预测结果
        logging.info("预测完成")
        return {
            'predictions': predictions,
            'predictions_proba': predictions_proba
        }
    except FileNotFoundError:
        logging.error("模型文件未找到，请检查路径")
        return {
            'error': '模型文件未找到，请检查路径'
        }
    except Exception as e:
        logging.error(f"预测过程中发生错误: {str(e)}")
        return {
            'error': f'预测过程中发生错误: {str(e)}'
        }
        # column_mapping = {
        #     'trans_date_trans_time': 'transTime',  # CSV中的交易时间列名
        #     'category': 'transType',  # CSV中的交易类型列名
        #     'amt': 'amount',  # CSV中的交易金额列名
        #     'last': 'lastName',  # CSV中的姓列名
        #     'first': 'firstName',  # CSV中的名列名
        #     'gender': 'gender',  # CSV中的性别列名
        #     'long': 'longitude',  # CSV中的经度列名
        #     'lat': 'latitude',  # CSV中的纬度列名
        #     'city_pop': 'cityPopulation',  # CSV中的城市人口列名
        #     'dob': 'birthDate',  # CSV中的出生年月列名
        #     'merch_long': 'merchantLong',  # CSV中的商家经度列名
        #     'merch_lat': 'merchantLat'  # CSV中的商家纬度列名
        # }
# def Transformdata(data):
#     try:
#         # 将输入数据转换为DataFrame
#         if isinstance(data, dict):
#             df = pd.DataFrame([data])  # 如果是字典（单条数据），转换为DataFrame
#         else:
#             df = pd.DataFrame(data)  # 如果是多条数据
#
#         df['city_pop'] = pd.to_numeric(df['cityPopulation'], errors='coerce')
#         df['amt'] = pd.to_numeric(df['amount'], errors='coerce')
#         # 日期时间转换
#         df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
#         df['trans_date_trans_time'] = pd.to_datetime(df['transTime'], errors='coerce')
#
#         # 地理位置数据转换
#         df['merchantLat'] = pd.to_numeric(df['merchantLat'], errors='coerce')
#         df['merchantLong'] = pd.to_numeric(df['merchantLong'], errors='coerce')
#         df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
#         df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
#
#         # # 将日期列转换为 datetime 类型
#         # df['dob'] = pd.to_datetime(df['birthDate'])
#
#         # 提取出生年份并计算年龄
#         current_year = 2025
#         df['dob'] = current_year - pd.DatetimeIndex(df['birthDate']).year
#
#         # # 将交易日期时间列转换为 datetime 类型
#         # df['trans_date_trans_time'] = pd.to_datetime(df['transTime'])
#
#         # 提取时间、月份和星期几
#         df['time'] = pd.DatetimeIndex(df['trans_date_trans_time']).hour
#         df['month'] = pd.DatetimeIndex(df['trans_date_trans_time']).month
#         df['weekday'] = pd.DatetimeIndex(df['trans_date_trans_time']).weekday  # 0=星期一, 6=星期日
#
#         # 计算经纬度差值
#         df['Llat'] = abs(df['merchantLat'] - df['latitude'])
#         df['Llong'] = abs(df['merchantLong'] - df['longitude'])
#
#         # 加载保存的 One-Hot 编码列名
#         with open('one_hot_columns.txt', 'r') as f:
#             one_hot_columns = [line.strip() for line in f.readlines()]
#
#         # 对新数据进行 One-Hot 编码
#         new_data = pd.get_dummies(new_data, columns=['category'], drop_first=True)
#
#         # 确保新数据的 One-Hot 编码列与训练数据一致
#         for column in one_hot_columns:
#             if column not in new_data.columns:
#                 new_data[column] = 0  # 如果新数据缺少某些列，补 0
#
#         features = ['amt', 'city_pop', 'dob', 'time', 'weekday', 'Llat', 'Encoding']
#         result = df[features]
#
#         return result
#     except Exception as e:
#         print(f"数据转换过程中发生错误: {str(e)}")
#         return None
def Transformdata(data):
    try:
        # 将输入数据转换为DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame([data])  # 如果是字典（单条数据），转换为DataFrame
        else:
            df = pd.DataFrame(data)  # 如果是多条数据

        # 数值类型转换
        df['city_pop'] = pd.to_numeric(df['cityPopulation'], errors='coerce')
        df['amt'] = pd.to_numeric(df['amount'], errors='coerce')

        # 日期时间转换
        df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
        df['trans_date_trans_time'] = pd.to_datetime(df['transTime'], errors='coerce')

        # 地理位置数据转换
        df['merchantLat'] = pd.to_numeric(df['merchantLat'], errors='coerce')
        df['merchantLong'] = pd.to_numeric(df['merchantLong'], errors='coerce')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

        # 提取出生年份并计算年龄
        current_year = 2025
        df['dob'] = current_year - pd.DatetimeIndex(df['birthDate']).year

        # 提取时间、月份和星期几
        df['time'] = pd.DatetimeIndex(df['trans_date_trans_time']).hour
        df['month'] = pd.DatetimeIndex(df['trans_date_trans_time']).month
        df['weekday'] = pd.DatetimeIndex(df['trans_date_trans_time']).weekday  # 0=星期一, 6=星期日

        # 计算经纬度差值
        df['Llat'] = abs(df['merchantLat'] - df['latitude'])
        df['Llong'] = abs(df['merchantLong'] - df['longitude'])

        # 加载保存的 One-Hot 编码列名
        with open('./uploads/one_hot_columns.txt', 'r') as f:
            one_hot_columns = [line.strip() for line in f.readlines()]

        # 对 category 列进行 One-Hot 编码
        df = pd.get_dummies(df, columns=['transType'], drop_first=True)

        # 确保新数据的 One-Hot 编码列与训练数据一致
        for column in one_hot_columns:
            if column not in df.columns:
                df[column] = 0  # 如果新数据缺少某些列，补 0

        # 选择需要的特征列
        features = ['amt', 'city_pop', 'dob', 'time', 'weekday', 'Llat'] + one_hot_columns
        # print(features)
        result = df[features]

        return result
    except Exception as e:
        print(f"数据转换过程中发生错误: {str(e)}")
        return pd.DataFrame()  # 返回空的 DataFrame 以避免后续代码出错
# def Grade2Value(x):
#     if isinstance(x, str) and len(x) == 1 and ord(x) >= 65:  # 确保 x 是单个字母
#         return ord('H') - ord(x)
#     return int(x)  # 对于其他类型的数据，转换为整数
#
# def Home2Value(x):
#     if(x=='MORTGAGE'):
#         return 1
#     elif(x=='RENT'):
#         return 2
#     elif(x=='OWN'):
#         return 3
#
# def preprocessing(file):
#     # 深拷贝一份，不改变原数据
#     df = file.copy(deep=True)
#     # 利率类型转float
#     df['int_rate'] = df['int_rate'].astype(str).str[:-1].astype(float)
#     # 信誉等级转数值类型
#     df['grade'] = df.grade.apply(lambda x:Grade2Value(x))
#     # 住房情况转换为数值类型
#     df['home_ownership'] =df.home_ownership.apply(lambda x:Home2Value(x))
#     # 检查每个字段的数据类型是否已全部转换为数值类型
#     # for i in range(df.shape[1]):
#     #     if(df.dtypes[i]=='object'):
#     #         return {}
#     # 归一化处理,z-score 标准正态分布
#     # std = StandardScaler()
#     # std_x = std.fit_transform(df)
#     return df


# # ------------------- 预处理阶段 ---------------------
#
# def predictLabel(file):
#     # 预处理,获取合法样本
#     x = preprocessing(file)
#     # if(x=="error"):
#     #     return "error"
#     # 加载模型
#     xgb = joblib.load("./model/xgb_plus.joblib")
#     y_pred = xgb.predict(x)
#
#     return y_pred
#
#
# def getPredictData(filename):
#     # DataFrame格式数据
#     file = getFile(filename)
#     # 获取预测的label
#     label_pred = predictLabel(file)
#     # if(label_pred=="error"):
#     #     return {
#     #         'state':'fail',
#     #         'msg':'数据格式存在错误'
#     #     }
#     print("--------------------",label_pred)
#     file['tag'] = label_pred
#     file.to_csv(f"./uploads/res_{filename}")
#     return_file = file.iloc[:500,:]
#     # DataFrame转换为json数据
#     json_data = return_file.to_json(orient='records',force_ascii=False)
#     return {
#         'state':'success',
#         'info':json_data,
#         'res_url':f"/uploads/res_{filename}"
#     }