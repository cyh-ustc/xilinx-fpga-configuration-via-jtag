import RPi.GPIO as GPIO
import time

tms_pin = 19
tck_pin = 13
tdo_pin = 5
tdi_pin = 12

bitstream = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(tck_pin, GPIO.OUT)
GPIO.setup(tms_pin, GPIO.OUT)
GPIO.setup(tdi_pin, GPIO.OUT)
GPIO.setup(tdo_pin, GPIO.IN)

def load_bitstream():
	f = open('top.bin','r')
	s = f.read(-1)
	print len(s)
	l = [ord(i) for i in s]
	for i in l:
		x = 0x80
		for j in range(8):
			bitstream.append(i/x)
			i%=x
			x/=2
	f.close()

def JTAG_Period():
	pass

def JTAG_SetPins(tdi_s,tms_s):
	GPIO.output(tdi_pin,tdi_s)
	GPIO.output(tms_pin,tms_s)
	GPIO.output(tck_pin,0)
	JTAG_Period()
	GPIO.output(tck_pin,1)
	JTAG_Period()
	
def JTAG_TLR():
	for i in range(5):
		JTAG_SetPins(1,1)

def JTAG_RTI(times):
	for i in range(times):
		JTAG_SetPins(1,0)


def JTAG_IR(instr):
	JTAG_SetPins(1,1)
	JTAG_SetPins(1,1)
	JTAG_SetPins(1,0)
	JTAG_SetPins(1,0)
	for i in range(len(instr)-1):
		JTAG_SetPins(instr[i],0)
	JTAG_SetPins(instr[-1],1)
	JTAG_SetPins(1,1)
	JTAG_SetPins(1,0)

def JTAG_getDR(size):
	data = []
	JTAG_SetPins(1,1)
	JTAG_SetPins(1,0)
	JTAG_SetPins(1,0)
	for i in range(size-1):
		JTAG_SetPins(0,0)
		data.append(GPIO.input(tdo_pin))
	JTAG_SetPins(0,1)
	data.append(GPIO.input(tdo_pin))
	JTAG_SetPins(1,1)
	JTAG_SetPins(1,0)
	return data

def JTAG_DR(data):
	JTAG_SetPins(1,1)
	JTAG_SetPins(1,0)
	JTAG_SetPins(1,0)
	for i in range(len(data)-1):
		JTAG_SetPins(data[i],0)
	JTAG_SetPins(data[-1],1)
	JTAG_SetPins(1,1)
	JTAG_SetPins(1,0)

def FPGA_GetID():
	JTAG_RTI(5)
	JTAG_IR([1,0,0,1,0,0])
	print JTAG_getDR(31)
	
def FPGA_Config():
	JTAG_RTI(5)
	print 'RTI Mode'
	JTAG_IR([1,1,0,1,0,0])   #JPROGRAM
	print 'JPROGRAM'
	JTAG_RTI(50000)
	print 'RTI Mode'
	JTAG_IR([1,0,1,0,0,0])   #CFG_IN
	print 'CFG_IN'
	JTAG_DR(bitstream)
	print 'Bitstream'
	JTAG_IR([0,0,1,1,0,0])   #JSTART
	print 'JSTART'
	JTAG_RTI(10000)
	print 'RTI'
	JTAG_TLR()
	print 'TLR'
	
load_bitstream()
FPGA_Config()
GPIO.cleanup()





	