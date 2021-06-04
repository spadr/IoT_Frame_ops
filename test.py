import numpy as np
import requests
import time

#sin,cos.tan波を送信するテスト用コード

key = "EQFbZpGGwnTR3za882qnPc28c249719188a274b2f227291cfe656634e11777bb46894cf14c18afeb4635f"

url    = "http://localhost/dev/"+ key
N      = 5000       # サンプル数
dt     = 1/576      # サンプリング間隔
f1, f2 = 48,258     # 周波数

t = np.arange(0, N*dt, dt) # 時間軸
freq = np.linspace(0, 1.0/dt, N) # 周波数軸

sin = (np.sin(2*np.pi*f1*t) + 1) + 0.3 * np.random.randn(N)
cos = np.cos(2*np.pi*f1*t)# + 0.3 * np.random.randn(N)
tan = np.tan(2*np.pi*f1*t)# + 0.3 * np.random.randn(N)

def device1(url,i):
    string = ""
    string += url 
    string += ",GH-Temperature(˚C)_Humidity(%)_HD-2_0_0,"
    string += str(1622787535 + 600*i) + "," 
    string += str(abs(sin[i])*15) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20)
    return string

def device2(url,i):
    string = ""
    string += url 
    string += ",GH-Temperature(˚C)_Humidity(%)-0_0_1,"
    string += str(1622787535 + 600*i) + "," 
    string += str(abs(sin[i])*15) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20)
    return string

def device3(url,i):
    string = ""
    string += url 
    string += ",GH-Temperature(˚C)_Humidity(%)-1_1_1,"
    string += str(1622787535 + 600*i) + "," 
    string += str(abs(sin[i])*15) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20) + "," 
    string += str(abs(sin[i])*20 + sin[i]/20)
    return string

def device4(url,i):
    string = ""
    string += url 
    string += ",GH-CO2(ppm)-1_1_1,"
    string += str(1622787535 + 600*i) + "," 
    string += str(abs(sin[i])*15)
    return string

def device5(url,i):
    string = ""
    string += url 
    string += ",GH-pF(pF)-1_1_1,"
    string += str(1622787535 + 600*i) + "," 
    string += str(abs(sin[i])*15)
    return string

def device6(url,i):
    string = ""
    string += url 
    string += ",GH-EC(pF)-1_0_1,"
    string += str(1622787535 + 600*i) + "," 
    string += str(abs(sin[i])*15)
    return string


for i in range(N):
    requests.get(device1(url,i))
    requests.get(device2(url,i))
    requests.get(device3(url,i))
    requests.get(device4(url,i))
    requests.get(device5(url,i))
    requests.get(device6(url,i))