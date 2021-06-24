# IoT_Frame_ops
IoTデバイスをサーバに接続するためのAPIです。<br>
RaspberryPiやM5Stackなどのedge端末を接続して、ラフにIoTを実装しましょう。<br>
<br>
自宅のスマートホーム化、温室にスマート農業を導入、アナログ計器をスマホで確認など<br>
様々な活用方法が考えられます。<br>
[RaspberryPiをサーバーにしたい場合はこちら](https://github.com/spadr/IoT_Frame_RaspberryPi)<br>
<br>

### AWSやGoogle Cloud、その他企業のIoTサービスとの比較
自前運用のため、転送容量や料金を気にすることありません。<br>
また、サービス終了が起こりえないので、長期間にわたりIoTを稼働することができます。<br>
具体的には、不動産や大型の機械など長期間使用するもののIoT化でメリットが際立つでしょう。<br>
<br>
<br>
<br>
このAPIはDocker上で稼働します。<br>
APIの使い方や具体的な使用例は→https://canaspad.com/post/1/
<br>

# Usage

### 動作確認のための手順
```
#このリポジトリをGit cloneする
$ git clone https://github.com/spadr/IoT_Frame_ops.git

#cdを移動
$ cd IoT_Frame_ops

#.env.exampleを.envにリネーム
$ mv .env.example .env

#app/entrypoint.shの権限変更
$ chmod +x app/entrypoint.sh

#イメージをビルドし、各コンテナを起動
$ sudo docker-compose -f docker-compose.yml up -d --build

#稼働状況を確認
$ sudo docker-compose -f docker-compose.yml ps -a
すべてUpになっていればOKです

#ブラウザで確認
http://localhost/にアクセスして動作確認してください。
また、開発環境用にメールサーバが http://localhost/8025 で稼働していますので、
認証メールは上記URLからご確認ください。

#実際にデータを送信する
test.pyにsin,cos.tan波を送信するテスト用コードを記載しております。
認証メールに記載されているアクセスキーを設定の上、お使いください。
また、実際にマイコンを使って送信する場合は下記のリポジトリにサンプルコードがあります。
https://github.com/spadr/CANASPAD-IoT_SAMPLE
```
### その他の操作
```
#データの初期化
$ sudo docker-compose -f docker-compose.yml exec app python manage.py flush --no-input

#マイグレーション
$ sudo docker-compose -f docker-compose.yml exec app python manage.py makemigrations

#DBの作成
$ sudo docker-compose -f docker-compose.yml exec app python manage.py migrate

#静的ファイルのコピー
$ sudo docker-compose -f docker-compose.yml exec app python manage.py collectstatic --no-input --clear

#Djangoの管理者ユーザの登録
$ sudo docker-compose -f docker-compose.yml exec app python manage.py createsuperuser

#イメージをビルドし、各コンテナを起動
$ sudo docker-compose -f docker-compose.yml up -d --build

#イメージ、コンテナ、ボリューム、ネットワークを削除
$ sudo docker-compose -f docker-compose.yml down

#各コンテナを開始
$ sudo docker-compose -f docker-compose.yml start

#各コンテナを停止
$ sudo docker-compose -f docker-compose.yml stop

#各コンテナをリスタート
$ sudo docker-compose -f docker-compose.yml restart

#稼働状況を確認
$ sudo docker-compose -f docker-compose.yml ps -a
```

### M5StickCからデータを送信する場合のサンプルコード
```
#include <WiFi.h>
#include <HTTPClient.h>
#include <M5StickC.h>

const char SSID[] = "Your WIFI SSID";
const char PASSWORD[] = "Your WIFI PASS";

const char* host     = "IPv4 Adress";
const char* event    = "/data/";
const char* device_name    = "Your Device Name";
const char* access_key    = "Your Access Key"; 
//アカウントの新規登録のためにお送りした、アクティベーションメールに記載されています
int sensor_value = 0; //センサーの値を格納します

void setup() {
  M5.begin();
  
  Serial.begin(115200);
  
  WiFi.begin(SSID, PASSWORD);
  Serial.print("WiFi connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }
  Serial.println(" connected");
}

void loop() {
  HTTPClient http;
  
  String URL = "http://";
         URL += String(host);
         URL += String(event);
         URL += String(access_key)   + ",";
         URL += String(device_name)  + ",";
         URL += String(sensor_value) + "/";
  
  Serial.print("Requesting URL: ");
  Serial.println(URL);
  
  http.begin(URL);
  
  int httpCode = http.GET();
  if (httpCode > 0) { //Check for the returning code
    String payload = http.getString();
    Serial.println(httpCode);
    Serial.println(payload);
    }
  else {
      Serial.print("Error on HTTP request!");
      Serial.println(httpCode);
    }
  
  http.end();
  
  delay(30*60*1000);
  sensor_value ++;
}
```


### 追加機能 : 温室の情報を可視化する機能(AGRI)
```
#温室の情報を可視化する機能とは?
温室の気温や湿度、CO2濃度などを可視化するダッシュボードです。
所謂スマートアグリでよく見る機能です。

#何ができるの?
温室の温度などを棟ごとに、推移や分布の形で確認できます。

#どうやって使うの?
例
device_name："AGRI-Temperature(˚C)_Humidity(%)-0_0_2"
sensor_value："25.7,58.3"

device_nameにはセンサーに関わるメタ情報を記載します。
書き込む情報は"AGRI", 測定項目(単位), 位置情報(棟番号_X軸_Y軸)で、それぞれを"-"で区切ります。

sensor_valueにはdevice_nameにある測定項目の測定値を順番通りに記載します。

```
