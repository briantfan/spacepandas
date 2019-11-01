import RPi.GPIO as GPIO
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 8080

GPIO.setmode(GPIO.BCM)

TRIG = 18
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, 0)
time.sleep(0.1)

distances = [0,0,0,0]

class WebHandler(BaseHTTPRequestHandler):

        def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(self.message())

        def message(self):
		file = open('/home/pi/page.html')
		text = file.read()
		file.close()
		distance = self.measure_distance()
		distance = round(distance) / 100
		color = self.make_color(distance)
		text = text.format(color, distance)
		return text

	def make_color(self, distance):
		if distance < 0.5:
			return "FF0000"
		elif distance < 1:
			return "FF4500"
		elif distance < 1.5:
			return "FFA500"
		elif distance < 2:
			return "FFAE42"
		elif distance < 3:
			return "FFFF00"
		elif distance < 4:
			return "ADFF2F"
		else:
			return "0ACC00"

	def measure_distance(self):
		GPIO.output(TRIG, 1)
		time.sleep(0.0001)
		GPIO.output(TRIG, 0)
		counter = 0
		while GPIO.input(ECHO) == 0 and counter < 1000:
			counter = counter + 1
		counter = 0
		start = time.time()
		while GPIO.input(ECHO) == 1 and counter < 40000:
			counter = counter + 1
		if counter == 40000:
			return self.average_distance()
		stop = time.time()
		distance = (stop - start) * 17000
		self.add_distance(distance)
		return self.average_distance()

	def average_distance(self):
		total = 0
		for dist in distances:
			total = total + dist
		return total / len(distances)

	def add_distance(self, distance):
		idx = 1
		while idx < len(distances):
			distances[idx - 1] = distances[idx]
			idx = idx + 1
		distances[len(distances) - 1] = distance

print "Starting server on port ", PORT_NUMBER
server = HTTPServer(("", PORT_NUMBER), WebHandler)
try:
	server.serve_forever()
except KeyboardInterrupt:
        print "Stopping Server"
except:
        print "Unexpected Server Error"
finally:
        GPIO.cleanup()
        server.socket.close()
