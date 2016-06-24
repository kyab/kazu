import RPi.GPIO as G
import time
import os
import signal
import sys

print "switchhello_pd started."

COUNT = 5
PIN_LED = 17
PIN_SWITCH = 27

def signal_handler(signal, frame):
	G.cleanup()
	print "GPIO cleanup done."
	sys.exit(0)

def wait_and_shout():
	G.wait_for_edge(PIN_SWITCH, G.RISING)
	print "SWITCH PUSHED"
	
	if G.input(PIN_SWITCH):
		print "HIGH"
	else:
		print "LOW"
	G.output(PIN_LED,True)
	os.system("aplay -q -D hw:0 ./one.wav &")
	time.sleep(0.1)
	G.output(PIN_LED,False)
		
G.setmode(G.BCM)
G.setup(PIN_LED, G.OUT)
G.setup(PIN_SWITCH, G.IN, pull_up_down = G.PUD_DOWN)

signal.signal(signal.SIGINT, signal_handler)

while True:
	try:
		wait_and_shout()
	except:
		pass
		
G.cleanup()
	


