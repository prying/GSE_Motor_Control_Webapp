#!/usr/bin/env python3
from flask import Flask, render_template, request
import serial
import logging

logging.basicConfig(filename = 'webapp.log', level=logging.INFO, format = '%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

ser = serial.Serial(
        port='/dev/serial0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5
)

rx = "na"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	rx = '1'
	if request.method == 'POST':
		if request.form.get('event_button') in ['0','1', '2', '3', '4', '5', '6', '7', '8']:
			msg = request.form.get('event_button')
			msg = msg.encode('ascii', errors='backslashreplace')
			print("intput", msg)
			app.logger.info(msg)
			ret = UART_write(msg)
			if type(ret) == str:
				rx = ret + UART_recive().decode('UTF-8')
			elif ret == 1:
				rx = UART_recive().decode('UTF-8')
			print(rx)
			return render_template("index.html", UART_RX=rx)
		else:
			rx = UART_recive().decode('UTF-8')
			return render_template("index.html", UART_RX=rx)
	elif request.method == 'GET':
		print("No post back call")

	return render_template("index.html", UART_RX=rx)

def UART_write(msg):
	ser.write(msg)
	echo = ser.readline().decode('UTF-8')
	msg = msg.decode('UTF-8')
	if msg.strip() != echo.strip():
		if not echo:
			echo = "nothing"
		ret = f"Command {msg} was not recived, recived {echo}"
		print(ret)
		return ret
	return 1

def UART_recive():
	# todo prevent getting stuck here
	return ser.readline()


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
