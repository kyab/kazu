import RPi.GPIO as G
import time
import os

print "switchhello_initial"

COUNT = 5
PIN_LED = 17
PIN_SWITCH = 23


def wait_and_shout():
	G.wait_for_edge(PIN_SWITCH, G.RISING)
	print "SWITCH PUSHED"
	
	if G.input(PIN_SWITCH):
		print "HIGH"
	else:
		print "LOW"
	G.output(PIN_LED,True)
	os.system("aplay -q -D hw:0 ./hello2.wav &")
	time.sleep(0.1)
	G.output(PIN_LED,False)
	return True

		
G.setmode(G.BCM)
G.setup(PIN_LED, G.OUT)
G.setup(PIN_SWITCH, G.IN)

#time.sleep(0.5)

while True:
	if not wait_and_shout():
		break
		
G.cleanup()
	


