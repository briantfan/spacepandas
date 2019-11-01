import time
# Use this code library to control the Raspberry PI
import RPi.GPIO as GPIO
# Use the web server that's included in Python.
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# This is where the web browser needs to go.
PORT_NUMBER = 8080

# Setup which pins on the Raspberry PI we should connect to.
GPIO.setmode(GPIO.BCM)
TRIG = 18
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Initialize the ultrasonic sensor. Make sure the trigger is off.
GPIO.output(TRIG, 0)
time.sleep(0.1)

# Setup the web server.
class WebHandler(BaseHTTPRequestHandler):

    # Give the web browser a response when it asks for information.
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.message())

    # Create the web page that the web browser will see.
    def message(self):
		file = open('/home/pi/page.html')
		text = file.read()
		file.close()
		distance = self.measure_distance()
		distance = round(distance) / 100
		color = self.make_color(distance)
		text = text.format(color, distance)
		return text

    # Figure out the background color to show.
	def make_color(self, distance):
		if distance < 0.5:
			return "FF0000"  # red
		elif distance < 1:
			return "FF4500"  # orange-red
		elif distance < 1.5:
			return "FFA500"  # orange
		elif distance < 2:
			return "FFAE42"  # yellow-orange
		elif distance < 3:
			return "FFFF00"  # yellow
		elif distance < 4:
			return "ADFF2F"  # green-yellow
		else:
			return "0ACC00"  # green

    # Use the ultrasonic sensor to figure out the distance.
	def measure_distance(self):
        # Send out an ultrasonic pulse.
		GPIO.output(TRIG, 1)
		time.sleep(0.0001)
		GPIO.output(TRIG, 0)
        # Reset our ultrasonic sensor to get ready to listen.
		counter = 0
		while GPIO.input(ECHO) == 0 and counter < 1000:
			counter = counter + 1
        # Listen for the ultrasonic echo.
		counter = 0
		start = time.time()
		while GPIO.input(ECHO) == 1 and counter < 40000:
			counter = counter + 1
		if counter == 40000:
			return self.average_distance()
		stop = time.time()
        # Calculate the distance from the time it took.
		distance = (stop - start) * 17000
        return distance

print "Starting server on port ", PORT_NUMBER
server = HTTPServer(("", PORT_NUMBER), WebHandler)
try:
    # Start the server
	server.serve_forever()
except KeyboardInterrupt:
        print "Stopping Server"
except:
        print "Unexpected Server Error"
finally:
        GPIO.cleanup()
        server.socket.close()
