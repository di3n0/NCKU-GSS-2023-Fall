import requests
import os
from datetime import datetime, timezone, timedelta

def checkin(UID,room_num):
    # 定义 Basic Authentication 的用户名和密码

    username = os.getenv('USERNAME')
    testpass = os.getenv('testpass')

    #print(username, password)

    api_url = "https://gss-ncku.azurewebsites.net/api/update/"
    #api_url = "https://gss8-1.azurewebsites.net/api/updateisempty/"
    
    current_time = datetime.now(timezone.utc)
    current_time_adjusted = current_time + timedelta(hours=8)
    current_time_str = current_time_adjusted.strftime( '%Y-%m-%d %H:%M:%S%z')
    print(current_time_str)

    data = {
        "cardid": UID,  # 替换为你的 cardid 值
        "room": room_num,  # 替换为你的 room 值
        "check_time": current_time_str  # 设置 check_time 为当前时间
    }

    # 设置 Basic Authentication
    auth = (username, testpass)

    # 发送 POST 请求，包括 Basic Authentication
    response = requests.post(api_url, data=data, auth=auth)
    if response.status_code == 200:
        print("Checking successfully.")
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

    return response.text

def checkout(room_num):
    # 定义 Basic Authentication 的用户名和密码
    username = os.getenv('USERNAME')
    testpass = os.getenv('testpass')

    api_url = "https://gss-ncku.azurewebsites.net/api/updateisempty/"
    
    current_time = datetime.now(timezone.utc)
    current_time_adjusted = current_time + timedelta(hours=8)
    current_time_str = current_time_adjusted.strftime( '%Y-%m-%d %H:%M:%S%z')
    print(current_time_str)

    data = {
        "room": room_num,  # 替换为你的 room 值
        "check_time": current_time_str  # 设置 check_time 为当前时间
    }

    # 设置 Basic Authentication
    auth = (username, testpass)

    # 发送 POST 请求，包括 Basic Authentication
    response = requests.post(api_url, data=data, auth=auth)
    if response.status_code == 200:
        print("Checking successfully.")
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

    return response.text