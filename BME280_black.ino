/***************************************************************
*  BME280 気圧・温湿度センサおよびダストセンサ用                       　　　　 
*  センサ値を取得してXBee経由でゲートウェイに送信する                       
*                         
*  電源には9V電池を使用                                        
*  実験及び打ち上げにはArduino Uno Rev3を使用　　　　　　　    
* 
*  最終更新日：2017年9月 
*  作成者：宇宙開発研究部 OKB                                  
***************************************************************/


#include "Seeed_BME280.h"
#include <Wire.h>
#include <PString.h>

//BME280クラス
BME280 bme280;

void setup()
{
  Serial.begin(9600);
  bme280.init();
}

void loop()
{
  //BME280センサデータ取得
  float tmp = bme280.getTemperature();//温度
  float pre = bme280.getPressure()/100.0;
  float hum = bme280.getHumidity();//湿度
  
  char tmpc[10],prec[10],humc[10];
  
  dtostrf(tmp,7,2,tmpc);
  dtostrf(pre,7,2,prec);
  dtostrf(hum,7,2,humc); 
  
  char buffer1[100];
  PString str1(buffer1,sizeof(buffer1));
  
  str1 += "bbbbb";
  str1 += ",";
  str1 += tmpc;
  str1 += ",";
  str1 += prec;
  str1 += ",";
  str1 += humc;
  str1 += "\n";
  
   Serial.print(str1);
 
  delay(1000);
}
