# IMPORTANT:please run setup.py in terminal before the first time you use this!
import serial
import logging
import time
from sqlite_helper import create_connection, create_record

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Initiate serial connection
# Ultrasonic sensors
us = serial.Serial('/dev/ttyUSB0',9600)
us.flushInput()

# NFC reader
# nfc = serial.Serial()
# nfc.flushInput()

# Initiate sqlite database
conn = create_connection('database.sqlite')

def read_ID():
    try:
        ID = input("ID: ")
        return int(ID)
    except:
        return False 
    
def read_sensor():
    if us.inWaiting:
        if ord(us.read(1))==1:
            return True
    return False

def display(number):
    print(number)

def main():
    while True:
        count = 0
        while read_ID():
            ID = read_ID()
            if read_sensor():
                count +=1
                display(count)
        print(ID, count)
            
if __name__ == "__main__":
    main()
    