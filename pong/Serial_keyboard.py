import keyboard
import serial


encoder = serial.Serial('/dev/ttyACM0',9600) # check the port before running
encoder.flushInput()

while True:
	try:
		if encoder.inWaiting:
			if ord(encoder.read(1))==1:
				keyboard.press_and_release('up')
			if ord(encoder.read(1))==2:
				keyboard.press('down')
	except KeyboardInterrupt:
		break

