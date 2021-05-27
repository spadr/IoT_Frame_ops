import numpy as np
import requests
import time

#sin,cos.tan波を送信するテスト用コード

key = "YourAccessKey"

url    = "http://localhost/data/"+ key +",Senser00"
N      = 256       # サンプル数
dt     = 0.01      # サンプリング間隔
f1, f2 = 10, 20    # 周波数

t = np.arange(0, N*dt, dt) # 時間軸
freq = np.linspace(0, 1.0/dt, N) # 周波数軸

sin = np.sin(2*np.pi*f1*t) + 0.3 * np.random.randn(N)
cos = np.cos(2*np.pi*f1*t) + 0.3 * np.random.randn(N)
tan = np.tan(2*np.pi*f1*t) + 0.3 * np.random.randn(N)

for i in range(N):
    requests.get(url + "1," + str(sin[i]))
    requests.get(url + "2," + str(cos[i]))
    requests.get(url + "3," + str(tan[i]))
    time.sleep(60.0)
