import serial
import time

if __name__=='__main__':
  gpio_seri=serial.Serial('/dev/ttyACM0',9600)
  print(gpio_seri.portstr)
  time.sleep(3)
  while 1:
   gpio_seri.write('get')
   time.sleep(1)
   data = gpio_seri.readline()
   print(data)
