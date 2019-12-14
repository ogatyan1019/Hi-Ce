import smbus
import serial
import time
import datetime
import math
#import requests
import urllib.request, json
#from urlparse import urlparse
#import json
import MySQLdb
from scipy import optimize,exp


i2c_address = 0x76
bus_number  = 1
bus = smbus.SMBus(bus_number)
digT = []
digP = []
digH = []

sensor_data = {'TEMP':'0.0', 'PRESSURE':'0.0','humidity':'0.0'}

def get_calib_param():
    calib = []
     
    for i in range (0x88,0x88+24):
        calib.append(bus.read_byte_data(i2c_address,i))
    calib.append(bus.read_byte_data(i2c_address,0xA1))
    for i in range (0xE1,0xE1+7):
         calib.append(bus.read_byte_data(i2c_address,i))

    digT.append((calib[1] << 8) | calib[0])
    digT.append((calib[3] << 8) | calib[2])
    digT.append((calib[5] << 8) | calib[4])
    digP.append((calib[7] << 8) | calib[6])
    digP.append((calib[9] << 8) | calib[8])
    digP.append((calib[11]<< 8) | calib[10])
    digP.append((calib[13]<< 8) | calib[12])
    digP.append((calib[15]<< 8) | calib[14])
    digP.append((calib[17]<< 8) | calib[16])
    digP.append((calib[19]<< 8) | calib[18])
    digP.append((calib[21]<< 8) | calib[20])
    digP.append((calib[23]<< 8) | calib[22])
    digH.append( calib[24] )
    digH.append((calib[26]<< 8) | calib[25])
    digH.append( calib[27] )
    digH.append((calib[28]<< 4) | (0x0F & calib[29]))
    digH.append((calib[30]<< 4) | ((calib[29] >> 4) & 0x0F))
    digH.append( calib[31] )

    for i in range(1,2):
         if digT[i] & 0x8000: digT[i] = (-digT[i] ^ 0xFFFF) + 1

    for i in range(1,8):
         if digP[i] & 0x8000: digP[i] = (-digP[i] ^ 0xFFFF) + 1

    for i in range(0,6):
        if digH[i] & 0x8000: digH[i] = (-digH[i] ^ 0xFFFF) + 1  

def  get_data_bme280():
    setup()
    get_calib_param()
    data = []
    for i in range (0xF7, 0xF7+8):
        data.append(bus.read_byte_data(i2c_address,i))
    pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    TEMP_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    hum_raw  = (data[6] << 8)  |  data[7]
     
    TEMP, t_fine = get_TEMP(TEMP_raw)
    PRESSURE = get_pressure(pres_raw,  t_fine )
    HUMI = get_humid(hum_raw,  t_fine )

    return TEMP, HUMI, PRESSURE
    
def get_pressure(adc_P,  t_fine ):
    PRESSURE = 0.0
    
    v1 = (t_fine / 2.0) - 64000.0
    v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * digP[5]
    v2 = v2 + ((v1 * digP[4]) * 2.0)
    v2 = (v2 / 4.0) + (digP[3] * 65536.0)
    v1 = (((digP[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8)  + ((digP[1] * v1) / 2.0)) / 262144
    v1 = ((32768 + v1) * digP[0]) / 32768
     
    if v1 == 0: return 0
    PRESSURE = ((1048576 - adc_P) - (v2 / 4096)) * 3125
    if PRESSURE < 0x80000000: PRESSURE = (PRESSURE * 2.0) / v1
    else: PRESSURE = (PRESSURE / v1) * 2
    v1 = (digP[8] * (((PRESSURE / 8.0) * (PRESSURE / 8.0)) / 8192.0)) / 4096
    v2 = ((PRESSURE / 4.0) * digP[7]) / 8192.0
    PRESSURE = PRESSURE + ((v1 + v2 + digP[6]) / 16.0)  
    return PRESSURE/100

def get_TEMP(adc_T):
    t_fine = 0.0
    v1 = (adc_T / 16384.0 - digT[0] / 1024.0) * digT[1]
    v2 = (adc_T / 131072.0 - digT[0] / 8192.0) * (adc_T / 131072.0 - digT[0] / 8192.0) * digT[2]
    t_fine = v1 + v2
    return t_fine / 5120.0,  t_fine 

def get_humid(adc_H,  t_fine ):
    var_h =   t_fine  - 76800.0
    if var_h != 0:
         var_h = (adc_H - (digH[3] * 64.0 + digH[4]/16384.0 * var_h)) * (digH[1] / 65536.0 * (1.0 + digH[5] / 67108864.0 * var_h * (1.0 + digH[2] / 67108864.0 * var_h)))
    else:
         return 0
    var_h = var_h * (1.0 - digH[0] * var_h / 524288.0)
    if var_h > 100.0:
         var_h = 100.0
    elif var_h < 0.0:
         var_h = 0.0
         
    return var_h

def setup():
    osrs_t = 1                
    osrs_p = 1                
    osrs_h = 1                
    mode   = 3                
    t_sb   = 5                
    filter = 0                
    spi3w_en = 0              

    ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
    config_reg    = (t_sb << 5) | (filter << 2) | spi3w_en
    ctrl_hum_reg  = osrs_h
    bus.write_byte_data(i2c_address, 0xF2,ctrl_hum_reg)
    bus.write_byte_data(i2c_address, 0xF4,ctrl_meas_reg)
    bus.write_byte_data(i2c_address, 0xF5,config_reg)

def f(x,TEMP):
    PsTw=6.11*(10**((7.5*x)/(x+273.15)))
    return PsTw-0.00062*1013.25*(TEMP-x)

def g(x,HUMI):
    a=1-((x+273.15)/647.3)    
    Ps=221200*exp((-7.765*a+1.45*(a**1.5)-2.776*(a**3)-1.233*(a**6))/(1-a))
    return (HUMI/100)*Ps

def h(x,TEMP,HUMI):
    return f(x,TEMP)-g(x,HUMI)

def main(): 
    
    ID=0
    #print("Date time , ID , TEMP , HUMI, PRESSURE , DI , WBGT\n")
    while True:
            
            data_list=[]
            ID=ID+1
            DATETIME=datetime.datetime.now()
            #yardstick_time=DATETIME.hour
            #if (yardstick_time+1)%24==DATETIME.hour:
              

            while 1:    
                TEMP, HUMI, PRESSURE = get_data_bme280() 
                gpio_seri=serial.Serial('/dev/ttyACM0',9600)    
            
                data = gpio_seri.readline()

                if len(data)==30:
                    break
                
            #print(HUMI,TEMP)
            data_list =data.split(b",")
            #print(data)
            #print(data_list)
            b_TEMP=float(data_list[1])
            #print(b_TEMP)

            args_data=(TEMP,HUMI)
            #print(args_data)
            Twet=optimize.fsolve(h,0,args=args_data)
            #print(Twet)                   
            DI=0.81*TEMP+0.01*HUMI*((0.99*TEMP)-14.3)+46.3
            
            WBGT=float(0.7*Twet+0.2*b_TEMP+0.1*TEMP)
            #print(TEMP,HUMI,PRESSURE,DI,WBGT)
            json_data = { "TEMP":TEMP,"HUMI":HUMI,"PRESSURE":PRESSURE,"DI":DI,"WBGT":WBGT}

            try:
                
                url = "URL" 
                method = "POST"
                headers = {"Content-Type" : "application/json"}

                
                store_data = json.dumps(json_data).encode("utf-8")

                #res=requests.post(url,data=store_data,headers=headers)
                request = urllib.request.Request(url, data=store_data, method=method, headers=headers)
                with urllib.request.urlopen(request) as response:
                    response_body = response.read().decode("utf-8")
                #print(response_body)

                time.sleep(900)

            except Exception as e:
                print(e)
                print("failed\n\n")
                time.sleep(900)            


    
if __name__ == '__main__':
    main()