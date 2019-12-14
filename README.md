# Hi-Ce
Raspberry PiとArduinoで測定したデータをDBに送り込むやつ  
第8回気象衛星観測機器コンテスト(2019/12/23)用  

内容
=========================================
BME280_black：Arduinoで動かすもの  
Rpi-Arduino-serial.py：ラズパイとArduinoをシリアル接続してデータがラズパイに送れているかの確認用  
store_test.py:データベースに成型したデータが遅れているかの確認用  
calculation_test.py:計算の確認用  
server.php:サーバー内で動かすもの  
Raspi.py:ラズパイ実機で動かすもの  

開発環境
==========================================
PC側  
使用IDE：Visual Studio Code,Arduino IDE(1.8.10.0)  
ライブラリ管理:Anaconda3(4.7.10)  
Tera Term  
WinSCP  
Cyberduck  
  
Raspberry Pi側  
Raspberry Pi3 b+  
使用OS：Raspbian Buster with desktop(ver.July-2019だったと記憶)  

使用言語
==================================================
Python 3.7.4  

その他
===================================================
server.phpは専攻科生が作成したものをいただきました。  
Paspi.pi上のBME280制御部はhttps://github.com/PrinzEugen7/Lesson/blob/master/Python/raspi3/gpio/sensor/bem280/bme280.py  
Rasoi.pyは15分に1回DBへデータを送信(time.sleepで調整可能)  
