import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print "Measuring distance..."

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

print "Waiting for sensor to settle"
time.sleep(2)

def on_connect(client, userdata, rc):
	print("Connected with result code " + str(rc))

def on_log(pahoClient, obj, level, string):
	print string

username = "005e04fe-deb5-4520-ae2d-6d54b3aa57ff"
password = "b4ec9ccb-e5b9-4a68-ba47-b144b7e3eff4"

mqttc = mqtt.Client("390EdA9dEC364bcBb673")
mqttc.username_pw_set(username, password)
mqttc.tls_set("/etc/ssl/certs/ca-certificates.crt")
mqttc.on_connect = on_connect
mqttc.on_log = on_log
mqttc.connect("mqtt.covapp.io",8883, 60)
mqttc.loop_start()



while True:
	num_measurements = 0
	sum = 0
	while num_measurements < 10:
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO)==0:
		  pulse_start = time.time()
		while GPIO.input(ECHO)==1:
		  pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)
		
		if distance < 20:
			num_measurements = num_measurements + 1
			sum = sum + distance

		print "Distance:",distance,"cm"
		time.sleep(2)
		mqttc.publish("4c7489ed-92c0-4e05-a23d-12cdf514fc6a", distance)
	average_measurement = sum / num_measurements
	mqttc.publish("4c7489ed-92c0-4e05-a23d-12cdf514fc6a", average_measurement)
	print "Average Distance: ",average_measurement
GPIO.cleanup()
