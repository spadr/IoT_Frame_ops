import numpy as np
import requests
import datetime

#sin,cos.tan波を送信するテスト用コード

key = "Access_Key"#Accesskey

url    = "http://localhost/dev/"+ key
N      = 5000       # サンプル数
dt     = 1/576      # サンプリング間隔
f1, f2 = 48,258     # 周波数

now_timestamp = int(datetime.datetime.now().timestamp())
start_timestamp = now_timestamp - 3 * 24 * 60 * 60
skip_time = 60*30

t = np.arange(0, N*dt, dt) # 時間軸
freq = np.linspace(0, 1.0/dt, N) # 周波数軸

sin = (np.sin(2*np.pi*f1*t) + 1) + 0.3 * np.random.randn(N)
cos = np.cos(2*np.pi*f1*t)# + 0.3 * np.random.randn(N)
tan = np.tan(2*np.pi*f1*t)# + 0.3 * np.random.randn(N)

def device1(url,i):
    string = ""
    string += url 
    string += ",AGRI-Temperature(˚C)_Humidity(%)_HD-0_0_0,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20)
    return string

def device2(url,i):
    string = ""
    string += url 
    string += ",AGRI-Temperature(˚C)_Humidity(%)-0_0_1,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20)
    return string

def device3(url,i):
    string = ""
    string += url 
    string += ",AGRI-Temperature(˚C)_Humidity(%)-0_0_2,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20)
    return string

def device4(url,i):
    string = ""
    string += url 
    string += ",AGRI-CO2(ppm)-0_0_0,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15)
    return string

def device5(url,i):
    string = ""
    string += url 
    string += ",AGRI-pF(pF)-0_0_0,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15)
    return string

def device6(url,i):
    string = ""
    string += url 
    string += ",AGRI-EC(pF)-0_0_0,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15)
    return string

def device7(url,i):
    string = ""
    string += url 
    string += ",AGRI-CO2(ppm)-0_0_1,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15)
    return string

def device8(url,i):
    string = ""
    string += url 
    string += ",AGRI-pF(pF)-0_0_1,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15)
    return string

def device9(url,i):
    string = ""
    string += url 
    string += ",AGRI-EC(pF)-0_0_1,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15)
    return string

def device10(url,i):
    string = ""
    string += url 
    string += ",AGRI-CO2(ppm)-0_0_2,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15)
    return string

def device11(url,i):
    string = ""
    string += url 
    string += ",AGRI-pF(pF)-0_0_2,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15)
    return string

def device12(url,i):
    string = ""
    string += url 
    string += ",AGRI-EC(pF)-0_0_2,"
    string += str(start_timestamp + skip_time*i) + "," 
    string += str(abs(sin[i])*15)
    return string

for i in range(N):
    if (start_timestamp + skip_time*i)> now_timestamp:
        print("END!!!!")
        break
    requests.get(device1(url,i))
    requests.get(device2(url,i))
    requests.get(device3(url,i))
    requests.get(device4(url,i))
    requests.get(device5(url,i))
    requests.get(device6(url,i))
    requests.get(device7(url,i))
    requests.get(device8(url,i))
    requests.get(device9(url,i))
    requests.get(device10(url,i))
    requests.get(device11(url,i))
    requests.get(device12(url,i))
    print((start_timestamp + skip_time*i) - now_timestamp)