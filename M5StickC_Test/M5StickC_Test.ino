#include <M5StickC.h>
#include "Canaspad.h"

Canaspad api = Canaspad();

const char  ssid[]       = "WiFi_ssid";
const char  password[]   = "WiFi_pass";
const char* api_username = "user@mail.com";
const char* api_password = "password";

int sensor_value = 0;

String sensor000;
String sensor001;
String sensor100;
String sensor101;

void setup() {
  M5.begin();
  
  Serial.begin(115200);
  
  if(not api.begin(ssid, password, 9, api_username, api_password)){
    Serial.println("Api Connection Faild");
    Serial.println(api.httpCode);
  }
  sensor000 = api.set("sensor000", "ch00", "number", 3, true);
  sensor001 = api.set("sensor001", "ch00", "number", 3, true);
  sensor100 = api.set("sensor100", "ch01", "number", 3, true);
  sensor101 = api.set("sensor101", "ch01", "number", 3, true);
  Serial.print("senser000 Device_token : ");
  Serial.println(sensor000);
}

void loop() {
  if (api.gettimestamp() % 30 == 0){
    api.add(String(float(sensor_value+0)), sensor000);
    api.add(String(float(sensor_value+2)), sensor001);
    api.add(String(float(sensor_value+10)), sensor100);
    api.add(String(float(sensor_value+100)), sensor101);

    if (api.send()) { 
      Serial.println(api.gettime());
      }
    else {
      int err_num = api.httpCode;
      Serial.print("Error on HTTP request!");
      Serial.println(err_num);
        
      }
    float res =  api.get(sensor000);
    Serial.print("API RETURN DATA :");
    Serial.println(res);
    delay(10*1000);
    sensor_value ++;
  }
}
