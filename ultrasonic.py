import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print "Measuring distance..."

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

print "Waiting for sensor to settle"
time.sleep(2)

num_measurements = 0


while True:
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
	average_measurement = sum / num_measurements
	print average_measurement
GPIO.cleanup()