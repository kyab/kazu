#!/usr/bin/python 

import RPi.GPIO as G
import time
import os
import signal
import sys
import threading
import subprocess

print "switchhello started."

COUNT = 5
# PIN_LED = 17
PIN_LED = 21

SWITCH_SOUND = 13

# SWITCH_MAP = {
# 	18:1,
# 	27:2,
# 	22:3,
# 	23:4
# }
# SWITCH_MAP = {
# 	24:5,
# 	10:6,
# 	9:7,
# 	25:8
# }

#SWITCH_MAP = {
#	11:9,
#	8 :10,
#	7 :0
#}

SWITCH_MAP = {
        11:1,
        8 :2,
        7 :3
}



sound_process = 0

def signal_handler(signal, frame):
	G.cleanup()
	print "GPIO cleanup done."
	sys.exit(0)

def play_voice(index):
	G.output(PIN_LED,True)
	os.system("aplay -q -D hw:0 /home/pi/voices/{0}.wav &".format(index))
	time.sleep(0.1)
	G.output(PIN_LED,False)

def voice_pushed(channel):
	time.sleep(0.1)
	if G.input(channel):
		print "pushed", channel,SWITCH_MAP[channel]
		t = threading.Thread(target=play_voice, args=(SWITCH_MAP[channel],))
		t.start()
	else:
		print "upped", channel, SWITCH_MAP[channel]

def sound_pushed(channel):
	global sound_process
	if G.input(channel):
		if sound_process:
			sound_process.kill()
		command = "aplay -q -D hw:0 /home/pi/voices/BRIDGE.wav"
		sound_process = subprocess.Popen(command.split(" "))
	else:
		sound_process.kill()


G.setmode(G.BCM)
G.setup(PIN_LED, G.OUT)

signal.signal(signal.SIGINT, signal_handler)

for c in SWITCH_MAP.iterkeys():
	G.setup(c, G.IN, pull_up_down = G.PUD_DOWN)
	# I only wanto to catch RISING only , but use BOTH to avoide chattering
	G.add_event_detect(c, G.BOTH, callback=voice_pushed, bouncetime=180)

G.setup(SWITCH_SOUND, G.IN, pull_up_down=G.PUD_DOWN)
G.add_event_detect(SWITCH_SOUND, G.BOTH, callback=sound_pushed, bouncetime=200)

# Now we are get ready!
subprocess.Popen("aplay -q -D hw:0 /home/pi/voices/start_jingle.wav".split(" "))
for _ in xrange(3):
	G.output(PIN_LED,True)
	time.sleep(0.3)
	G.output(PIN_LED,False)
	time.sleep(0.3)


while True:
	time.sleep(1.0)
		
G.cleanup()
	


