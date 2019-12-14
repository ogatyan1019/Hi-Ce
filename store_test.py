import MySQLdb
import datetime
import urllib.request, json

DATETIME = datetime.datetime.now()
ID = 1
TEMP = 30.5
HUMI = 50.3
PRESSURE = 1013.5
DI = 70.0
WBGT = 20.5
json_data = { "TEMP":TEMP,"HUMI":HUMI,"PRESSURE":PRESSURE,"DI":DI,"WBGT":WBGT}

try:
    
    url = "URL" 
    method = "POST"
    headers = {"Content-Type" : "application/json"}

    #jsonファイルをエンコードする
    store_data = json.dumps(json_data).encode("utf-8")

    # httpリクエストを準備してPOST
    request = urllib.request.Request(url, data=store_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
    print(response_body)

except Exception as e:
    print(e)
    print("failed\n\n")