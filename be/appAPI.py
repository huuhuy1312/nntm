import json
import string
from sklearn.linear_model import LinearRegression
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import paho.mqtt.client as mqtt
# import schedule
from datetime import datetime,timedelta
import paho.mqtt.publish as publish
from pytz import timezone
import time
import pandas as pd
import numpy as np
import os
# from keras.preprocessing.image import load_img, img_to_array
app = Flask(__name__)
CORS(app, supports_credentials=False, methods=["GET", "POST", "PUT", "DELETE"])
import requests
# Import userDAO and MQTT constants
from dal import userDAO
from dal import plantDAO
from dal import taskDAO
from dal import haverstTimeDAO
import csv
import time
MQTT_SERVER = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_USER = "flslayder1312@gmail.com"
MQTT_PASSWORD = "Huuhuy1312@"
MQTT_TEMP_TOPIC = "ESP32/DHT11/Temp"
MQTT_HUM_TOPIC = "ESP32/DHT11/Hum"
MQTT_SOIL_TOPIC = "ESP32/DHT11/Soil"
MQTT_LIGHT_TOPIC = "ESP32/DHT11/Light"
MQTT_COUNTER_TOPIC = "ESP32/DHT11/Counter"
MQTT_TEN_CAY_TOPIC = "ESP32/DHT11/TenCay"
MQTT_UPLOAD_TOPIC = "ESP32/IdealTemp"

MQTT_TEST_TOPIC = "test2"
temp_arr = None
hum_arr = None
soil = None
light = None
ten_cay = None
client = mqtt.Client()
file_name = "sensor_data.csv"
counter =0
counter_cu = -1
import csv

def write_data_to_csv(file_name, data):
    # Read the last row from the CSV file
    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        last_row = None
        for row in reader:
            last_row = row

    # Compare new data with the last row
    if last_row is None or any(last_row[key] != data[0][key] for key in ('nhiet_do', 'do_am', 'do_am_dat', 'anh_sang')):
        # Write data to CSV
        with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['cay_trong', 'thoi_gian', 'nhiet_do', 'do_am', 'do_am_dat', 'anh_sang', 'trang_thai', 'san_luong']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data[0])

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TEMP_TOPIC)
        client.subscribe(MQTT_HUM_TOPIC)
        client.subscribe(MQTT_SOIL_TOPIC)
        client.subscribe(MQTT_LIGHT_TOPIC)
        client.subscribe(MQTT_COUNTER_TOPIC)
        client.subscribe(MQTT_TEN_CAY_TOPIC)
    else:
        print(f"Failed to connect, return code: {rc}")
def on_message(client, userdata, message):
    decoded_data = message.payload.decode()
    global temp_arr
    temp_arr = decoded_data
def on_message1(client, userdata, message):
    decoded_data = message.payload.decode()
    global ten_cay
    ten_cay = decoded_data
def on_message2(client, userdata, message):
    global hum_arr
    decoded_data = message.payload.decode()
    hum_arr = decoded_data
def on_message3(client, userdata, message):
    global soil
    decoded_data = message.payload.decode()
    soil = decoded_data
def on_message4(client, userdata, message):
    global light, file_name,temp_arr
    decoded_data = message.payload.decode()
    light = decoded_data
def on_message5(client, userdata, message):
    global temp_arr,hum_arr,soil,light,ten_cay,counter
    counter+=1
    print(counter)
    if True:
        df_data = pd.read_csv("sensor_data.csv")
        thoi_gian_cu_float = df_data.iloc[df_data.shape[0] -1]["thoi_gian"]
        thoi_gian_cu = str(thoi_gian_cu_float)
        time_object = datetime.strptime(thoi_gian_cu, '%Y-%m-%d %H:%M:%S')
        time_plus_one_minute = time_object + timedelta(hours=1)
        time_plus_one_minute_string = time_plus_one_minute.strftime('%Y-%m-%d %H:%M:%S')
        print(ten_cay)
        if(temp_arr and hum_arr and soil and light and  ten_cay and ten_cay.replace('"', '')!='Chua trong'):
            row = [{"cay_trong":ten_cay.replace('"', ''), "thoi_gian":time_plus_one_minute_string, "nhiet_do":temp_arr,"do_am":hum_arr,"do_am_dat":soil,"anh_sang":light,"trang_thai":"Binh thuong","san_luong":None}]
            write_data_to_csv(file_name,row)
def on_disconnect(client, userdata, rc):
    client.loop_stop(force=False)
    if rc != 0:
        print("Unexpected disconnection.")
    else:
        print("Disconnected")
def start_mqtt_listener():
    client.on_connect = on_connect
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.message_callback_add(MQTT_TEMP_TOPIC, on_message)
    client.message_callback_add(MQTT_TEN_CAY_TOPIC, on_message1)
    client.message_callback_add(MQTT_HUM_TOPIC, on_message2)
    client.message_callback_add(MQTT_SOIL_TOPIC, on_message3)
    client.message_callback_add(MQTT_LIGHT_TOPIC, on_message4)
    client.message_callback_add(MQTT_COUNTER_TOPIC, on_message5)
    client.connect(MQTT_SERVER, MQTT_PORT)
    client.loop_start()
dateCurrent = None
@app.route('/api', methods=["GET"])
def return_data():
    global temp_arr,hum_arr,soil,light
    if temp_arr and hum_arr and soil and light:
        
        return jsonify({"Temp": temp_arr, "Hum": hum_arr,"Soil":soil,"Light":light,"Cay":ten_cay})
    else:
        return jsonify({"Temp": None, "Hum": None,"Soil":None,"Light":None,"Cay":ten_cay})

@app.route('/mqtt', methods=["POST"])
def post_ideal_numbers():
    try:
        data = request.json
        if client.is_connected():
            publish.single(MQTT_UPLOAD_TOPIC, json.dumps(data), hostname=MQTT_SERVER, port=MQTT_PORT, auth={'username': MQTT_USER, 'password': MQTT_PASSWORD})
        else:
            print("Not connected to MQTT broker, will retry in 5 seconds")
    
        return jsonify("Success")
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/mqtt/postTenCay', methods=["POST"])
def post_ten_cay():
    try:
        data = request.json["ten_cay"].replace('"', '')
        print(data)
        if client.is_connected():
            publish.single(MQTT_TEN_CAY_TOPIC, json.dumps(data), hostname=MQTT_SERVER, port=MQTT_PORT, auth={'username': MQTT_USER, 'password': MQTT_PASSWORD})
        else:
            print("Not connected to MQTT broker, will retry in 5 seconds")
    
        return jsonify("Success")
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/thuhoach',methods =["POST"])
def thuhoach():
    data = request.json["san_luong"]
    print(data)
    df_data = pd.read_csv("sensor_data.csv")
    thoi_gian_cu_float = df_data.iloc[df_data.shape[0] -1]["thoi_gian"]    
    thoi_gian_cu = str(thoi_gian_cu_float)
    time_object = datetime.strptime(thoi_gian_cu, '%Y-%m-%d %H:%M:%S')
    time_plus_one_minute = time_object + timedelta(hours=1)
    time_plus_one_minute_string = time_plus_one_minute.strftime('%Y-%m-%d %H:%M:%S')
    row = [{"cay_trong":ten_cay.replace('"', ''), "thoi_gian":time_plus_one_minute_string, "nhiet_do":temp_arr,"do_am":hum_arr,"do_am_dat":soil,"anh_sang":light,"trang_thai":"Da Thu Hoach","san_luong":data}]
    write_data_to_csv(file_name,row)
    api_url = "http://127.0.0.1:8080/mqtt/postTenCay"
    payload = {'ten_cay':'Chua trong'}
    response  = requests.post(api_url,json = payload)
    return jsonify("Success")
@app.route('/updatePlantsWhenHarvest',methods =["POST"])
def updatePlantsWhenHarvest():
    df_data = pd.read_csv("sensor_data.csv")
    filtered_df = df_data[df_data['trang_thai'] == 'Da Thu Hoach']
    last_index= filtered_df.index[-1]
    last_row = filtered_df.index[-2]
    subset = df_data.iloc[last_row:last_index]
    average_temp = round(subset['nhiet_do'].mean(),2)
    average_humidity = round(subset['do_am'].mean(),2)
    average_soil_humidity = round(subset['do_am_dat'].mean(),2)
    average_light = round(subset['anh_sang'].mean(),2)
    ten_cay = df_data.loc[last_index,"cay_trong"]
    thoi_gian_giua = pd.to_datetime(df_data.loc[last_index, 'thoi_gian']) - pd.to_datetime(df_data.loc[last_row, 'thoi_gian'])
    thoi_gian_giua_gio = thoi_gian_giua.total_seconds() / 3600
    index = df_data.loc[last_index,"san_luong"]/thoi_gian_giua_gio
    tmp = plantDAO.updatePlantsWhenHarvest(average_temp,average_humidity,average_light,average_soil_humidity,index,ten_cay)
    id_plant = plantDAO.getPlantByName(ten_cay)
    print(id_plant["id"])
    addHarvest = haverstTimeDAO.saveHarvest(pd.to_datetime(df_data.loc[last_row, 'thoi_gian']),pd.to_datetime(df_data.loc[last_index, 'thoi_gian']),df_data.loc[last_index,"san_luong"],
                                            average_temp,average_humidity,average_light,average_soil_humidity,id_plant["id"])
    print(addHarvest)
    return jsonify("Success")
@app.route('/getallusers', methods=['GET'])
def get_all_users():
    try:
        users = userDAO.getAllUsers()
        users = [user.to_dict() for user in users]
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/saveUser', methods=['POST'])
def save_user():
    try:
        data = request.json
        userDAO.saveUser(data)
        return jsonify("Success")
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        result = userDAO.checkUserExist(username, password)
        if result:
            return jsonify({"message": "success"})
        else:
            return jsonify({"error": "Đăng nhập không thành công. Tên người dùng hoặc mật khẩu không đúng."})
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/insertuser', methods=['POST'])
def insert_user():
    try:
        data = request.json
        userDAO.insertUser((data['username'], data['password'], data['email']))
        return jsonify("Success")
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/getUserByEmail/<email>', methods=["GET"])
def get_user_by_email(email):
    try:
        user = userDAO.getUserByEmail(email)
        if user:
            return jsonify(user.to_dict())
        else:
            return jsonify(None)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/getPlantByName/<name>', methods=["GET"])
def get_plant_by_name(name):
    try:
        plants = plantDAO.getPlantByName(name)
        if not plants:
            return jsonify({"error": "Plant not found"}), 404
        return jsonify(plants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
@app.route('/getPlantByTempAndHum', methods=["POST"])
def get_plant_by_temp_hum():
    try:
        data = request.json
        plants = plantDAO.getPlantByIdealTempAndIdealHum(data["temp"],data["hum"])
        plants = [user.to_dict() for user in plants]
        return jsonify(plants)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/getDataMeasureByNgay", methods=["POST"])
def get_data_measure():
    data = request.json
    startDate = pd.to_datetime(data["startDate"])
    endDate = pd.to_datetime(data["endDate"])
    chude = data["chude"]
    
    df = pd.read_csv("sensor_data.csv")
    df['thoi_gian'] = pd.to_datetime(df['thoi_gian'])
    mask = (df['thoi_gian'] >= startDate) & (df['thoi_gian'] <= endDate)
    filtered_df = df[mask]
    daily_avg = filtered_df.groupby(filtered_df['thoi_gian'].dt.strftime('%m/%d'))[chude].mean()
    daily_avg_rounded = {date: round(value, 2) for date, value in daily_avg.items()}
    
    return jsonify(daily_avg_rounded)
@app.route("/getDataMeasureByGio", methods=["POST"])
def get_data_measure_by_gio():
    data = request.json
    date = pd.to_datetime(data["date"])
    time_period = data["time_period"]
    topic = data["topic"]
    
    df = pd.read_csv("sensor_data.csv")
    df['thoi_gian'] = pd.to_datetime(df['thoi_gian'])
    date_mask = df['thoi_gian'].dt.date == date.date()
    df_date = df[date_mask]
    if time_period == 'AM':
        filtered_df = df_date[df_date['thoi_gian'].dt.hour < 12]
    elif time_period == 'PM':
        filtered_df = df_date[df_date['thoi_gian'].dt.hour >= 12]
    else:
        return jsonify({"error": "Invalid time period"})
    
    hourly_temperatures = filtered_df.set_index('thoi_gian').resample('H')[topic].mean().to_dict()
    hourly_temperatures = {hour.strftime('%H'+"h"): round(value, 2) for hour, value in hourly_temperatures.items()}
    
    return jsonify(hourly_temperatures)
@app.route("/getDataMeasureByDefault", methods=["POST"])
def get_data_measure_by_default():
    data = request.json
    topic = data["topic"]
    df = pd.read_csv("sensor_data.csv")
    df['thoi_gian'] = pd.to_datetime(df['thoi_gian'])
    sorted_df = df.sort_values(by='thoi_gian', ascending=False).head(10)
    hourly_temperatures = sorted_df.set_index('thoi_gian').resample('H')[topic].mean().to_dict()
    hourly_temperatures = {hour.strftime('%H'+"h"): round(value, 2) for hour, value in hourly_temperatures.items()}
    return jsonify(hourly_temperatures)
def tim_vi_tri_thoi_gian(df, thoi_gian_bat_dau, thoi_gian_ket_thuc):
    df_filtered = df[(df['thoi_gian'] == thoi_gian_bat_dau) | (df['thoi_gian'] == thoi_gian_ket_thuc)]
    vi_tri_thoi_gian_bat_dau = df_filtered.index[df_filtered['thoi_gian'] == thoi_gian_bat_dau].tolist()
    vi_tri_thoi_gian_ket_thuc = df_filtered.index[df_filtered['thoi_gian'] == thoi_gian_ket_thuc].tolist()
    return vi_tri_thoi_gian_bat_dau, vi_tri_thoi_gian_ket_thuc

def tinh_trung_binh_nhiet_do(df, vi_tri_thoi_gian_bat_dau, vi_tri_thoi_gian_ket_thuc, topic):
    so_luong = abs(vi_tri_thoi_gian_ket_thuc - vi_tri_thoi_gian_bat_dau) + 1
    so_phan_chia = 31
    so_phan_con_lai = so_luong % so_phan_chia
    so_phan = so_luong // so_phan_chia
    nhiet_do_trung_binh = {}
    for i in range(so_phan_chia+1):
        if i < so_phan_chia:
            start = vi_tri_thoi_gian_bat_dau + i * so_phan
            end = start + so_phan
            nhiet_do_trung_binh[df['thoi_gian'][start]] = round(df[topic][start:end].mean(), 2)
        else:
            nhiet_do_trung_binh[df['thoi_gian'][vi_tri_thoi_gian_ket_thuc-so_phan_con_lai+1]] = round(df[topic][vi_tri_thoi_gian_ket_thuc-so_phan_con_lai+1:vi_tri_thoi_gian_ket_thuc+1].mean(), 2)
    return nhiet_do_trung_binh
@app.route("/getDataMeasureSpecial", methods=["POST"])
def get_data_measure_special():
    df = pd.read_csv('sensor_data.csv')
    data = request.json
    start_time = data["start_time"]
    end_time = data["end_time"]
    topic = data["topic"]
    # Tìm vị trí của thời gian bắt đầu và kết thúc
    vi_tri_thoi_gian_bat_dau, vi_tri_thoi_gian_ket_thuc = tim_vi_tri_thoi_gian(df, start_time, end_time)
    
    # Tính trung bình nhiệt độ của 12 phần
    result = tinh_trung_binh_nhiet_do(df, vi_tri_thoi_gian_bat_dau[0], vi_tri_thoi_gian_ket_thuc[0],topic)
    print(vi_tri_thoi_gian_bat_dau,vi_tri_thoi_gian_ket_thuc)
    return jsonify({'result': result})

@app.route('/saveTask', methods=['POST'])
def save_task():
    try:
        data = request.json
        print(data)
        taskDAO.insertTask(data)
        return jsonify("Success")
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route("/getClaimedTasksByUserId/<int:user_id>",methods =["GET"])
def getClaimedTasksByUserId(user_id):
    try:
        tasks = taskDAO.getClaimedTasksByUserId(user_id)
        tasks = [task.to_dict() for task in tasks]
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error":str(e)}),500   

@app.route("/getAcceptedTasksByUserId/<int:user_id>",methods =["GET"])
def getAccpetedTasksByUserId(user_id):
    try:
        tasks = taskDAO.getAcceptedTasksByUserId(user_id)
        tasks = [task.to_dict() for task in tasks]
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error":str(e)}),500   
@app.route("/getAcceptedTodayTasksByUserId/<int:user_id>",methods =["GET"])
def getAcceptedTodayTasksByUserId(user_id):
    try:
        tasks = taskDAO.getAcceptedTodayTasksByUserId(user_id)
        tasks = [task.to_dict() for task in tasks]
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error":str(e)}),500   
@app.route("/acceptTaskByTaskId/<int:taskId>",methods=["POST"])
def acceptTaskByTaskId(taskId):
    try:

        taskDAO.acceptTaskByTaskId(taskId)
        return jsonify("Success")
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route("/completeTaskByTaskId/<int:taskId>",methods=["POST"])
def completeTaskByTaskId(taskId):
    try:
        print(taskId)
        taskDAO.completeTaskByTaskId(taskId)
        return jsonify("Success")
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route("/deniedTaskByTaskId",methods=["POST"])
def deniedTaskByTaskId():
    try:
        data = request.json
        taskId = data["id"]
        reason = data["reason"]
        taskDAO.deniedTaskByTaskId(taskId,reason)
        return jsonify("Từ Chối nhiệm vụ thành công")
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route("/getAcceptedTasks",methods =["GET"])
def getAcceptedTodayTasks():
    try:
        tasks = taskDAO.getAllAcceptedTasks()
        tasks = [task.to_dict() for task in tasks]
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error":str(e)}),500 
@app.route("/getClaimedTasks",methods =["GET"])
def getClaimedTasks():
    try:
        tasks = taskDAO.getAllClaimedTasks()
        tasks = [task.to_dict() for task in tasks]
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error":str(e)}),500
@app.route("/getDeniedTasks",methods =["GET"])
def getDeniedTasks():
    try:
        tasks = taskDAO.getAllDeniedTasks()
        tasks = [task.to_dict() for task in tasks]
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error":str(e)}),500  
@app.route("/getNameByUserId/<int:userId>",methods =["GET"])
def getNameByUserId(userId):
    try:
        name = taskDAO.getNameByUserId(userId)
        return jsonify(name)
    except Exception as e:
        return jsonify({"error":str(e)}),500
@app.route("/getHarvestTimeByIdPlant/<int:idPlant>",methods =["GET"])
def getHarvestTimeByIdPlant(idPlant):
    try:
        harvestTimes = haverstTimeDAO.getHarvestTimeByIdPlant(idPlant)
        return jsonify(harvestTimes)
    except Exception as e:
        return jsonify({"error":str(e)}),500
@app.route("/getAllPlants",methods=["GET"])
def getAllPlants():
    try:
        plants = plantDAO.getAllPlants()
        return jsonify(plants)
    except Exception as e:
        return jsonify({"error":str(e)}),500

import time
@app.route("/caculateIndexHarvest", methods=["POST"])
def caculateIndexHarvest():
    try:
        # start_time = time.time()
        df = pd.read_csv('sensor_data.csv')
        filtered_df = df[df['trang_thai'] == 'Da Thu Hoach' ]
        indices = filtered_df.index.tolist()
        indices.insert(0, 0)
        tong_hop = {}
        san_luong_csv =[]
        time_csv = []
        for i in range(len(indices)-1):
            start = indices[i]
            end = indices[i]+120
            cay_trong = df.iloc[indices[i+1]]["cay_trong"]
            time_trong = (pd.to_datetime(df.iloc[indices[i+1]]["thoi_gian"]) - pd.to_datetime(df.iloc[indices[i]]["thoi_gian"])).total_seconds() / 3600
            time_csv.append(df.iloc[indices[i]+1]["thoi_gian"])
            san_luong_csv.append(df.iloc[indices[i+1]]["san_luong"]/time_trong)
            khoang_gia_tri = df.iloc[start:end]
            khoang_gia_tri_chia = np.array_split(khoang_gia_tri,40)
            ndo_tb = [round(x["nhiet_do"].mean(),2) for x in khoang_gia_tri_chia]
            doam_tb = [round(x["do_am"].mean(),2) for x in khoang_gia_tri_chia]
            if cay_trong not in tong_hop:
                tong_hop[cay_trong] = {"san_luong": [], "thong_so": []}
            tong_hop[cay_trong]["san_luong"].append([df.iloc[indices[i+1]]["san_luong"]/time_trong])
            tong_hop[cay_trong]["thong_so"].append([ndo_tb,doam_tb])
        result = {}
        for key, value in tong_hop.items():
            x = np.array(value["thong_so"])
            y = np.array(value["san_luong"])
            X_reShaped = x.reshape(x.shape[0], -1)
            model = LinearRegression()
            model.fit(X_reShaped, y)
            
            new_data_request = np.array(request.json["new_data"])
            new_data = np.array(new_data_request)
            new_data_reshaped = new_data.reshape(1, -1)
            predicted_performance = model.predict(new_data_reshaped)
            
            result[key] = round(predicted_performance[0][0],5)
        print(result)
        return jsonify(result)
    except Exception as e:  
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    start_mqtt_listener()
    app.run(debug=True, port=8080)
