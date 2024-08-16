import machine
from time import sleep_ms
import microbit
from neopixel import NeoPixel
class MaqueenPlusV2:
	HEADLIGHT_LEFT=1;HEADLIGHT_RIGHT=2;HEADLIGHT_BOTH=3;LED_OFF=0;LED_ON=1;MOTOR_LEFT=1;MOTOR_RIGHT=2;MOTOR_BOTH=3;MOTOR_DIR_STOP=0;MOTOR_DIR_FORWARD=0;MOTOR_DIR_BACKWARD=1;SERVO_P0=0;SERVO_P1=1;SERVO_P2=2;COLOR_RED=255,0,0;COLOR_ORANGE_RED=255,64,0;COLOR_ORANGE=255,128,0;COLOR_YELLOW_ORANGE=255,191,0;COLOR_YELLOW=255,255,0;COLOR_YELLOW_GREEN=191,255,0;COLOR_GREEN=128,255,0;COLOR_SPRING_GREEN=64,255,0;COLOR_CYAN=0,255,255;COLOR_SKY_BLUE=0,191,255;COLOR_BLUE=0,128,255;COLOR_VIOLET_BLUE=0,64,255;COLOR_INDIGO=0,0,255;COLOR_VIOLET=64,0,255;COLOR_MAGENTA=128,0,255;COLOR_ROSE=191,0,255;COLOR_LIST_RAINBOW=[COLOR_RED,COLOR_ORANGE_RED,COLOR_ORANGE,COLOR_YELLOW_ORANGE,COLOR_YELLOW,COLOR_YELLOW_GREEN,COLOR_GREEN,COLOR_SPRING_GREEN,COLOR_CYAN,COLOR_SKY_BLUE,COLOR_BLUE,COLOR_VIOLET_BLUE,COLOR_INDIGO,COLOR_VIOLET,COLOR_MAGENTA,COLOR_ROSE]
	def __init__(A,ultrasonic_trigger_pin=microbit.pin13,ultrasonic_echo_pin=microbit.pin14):
		C=False
		while 16 not in microbit.i2c.scan():microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		B=C
		while B==C:
			E=A._a();D=E[-3:];A._g=int(D[0]);A._h=int(D[2])
			if A._g==2 and A._h==1:B=True
			if B==C:microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		A._f=ultrasonic_trigger_pin;A._e=ultrasonic_echo_pin;A._d=NeoPixel(microbit.pin15,4);A.motor_stop(3);A.set_headlight(3,0);A.set_underglow_off();microbit.display.show(microbit.Image.YES);microbit.display.clear()
	def _c(A,buf):microbit.i2c.write(16,bytes(buf))
	def _b(A,count):return microbit.i2c.read(16,count)
	def _a(A):A._c([50]);B=int.from_bytes(A._b(1),'big');A._c([51]);C=A._b(B);D=''.join([chr(A)for A in C]);return D
	def set_headlight(B,light,state):
		C=light;A=state
		if C==1:B._c([11,A])
		elif C==2:B._c([12,A])
		elif C==3:B._c([11,A,A])
	def motor_run(B,motor,dir,speed):
		C=motor;A=speed
		if A>240:A=240
		if C==1:B._c([0,dir,A])
		elif C==2:B._c([2,dir,A])
		elif C==3:B._c([0,dir,A,dir,A])
	def motor_stop(A,motor):A.motor_run(motor,0,0)
	def drive_forward(A,speed):A.motor_run(3,0,speed)
	def drive_backward(A,speed):A.motor_run(3,1,speed)
	def drive_stop(A):A.motor_stop(3)
	def drive_spin_left(A,speed):B=speed;A.motor_run(1,1,B);A.motor_run(2,0,B)
	def drive_spin_right(A,speed):B=speed;A.motor_run(1,0,B);A.motor_run(2,1,B)
	def get_range_cm(A):
		A._f.write_digital(1);sleep_ms(1);A._f.write_digital(0)
		if A._e.read_digital()==0:A._f.write_digital(0);A._f.write_digital(1);sleep_ms(20);A._f.write_digital(0);C=machine.time_pulse_us(A._e,1,500*58)
		else:A._f.write_digital(1);A._f.write_digital(0);sleep_ms(20);A._f.write_digital(0);C=machine.time_pulse_us(A._e,0,500*58)
		B=C/59
		if B<=0:return 0
		if B>=500:return 500
		return round(B)
	def servo(C,servo_id,angle):
		B=servo_id;A=angle
		if A<0:A=0
		elif A>180:A=180
		if B==0:microbit.pin0.write_analog(A)
		elif B==1:microbit.pin1.write_analog(A)
		elif B==2:microbit.pin2.write_analog(A)
	def line_track(B):
		B._c([29]);A=int.from_bytes(B._b(1),'big')
		if B._h==0:return A>>0&1==1,A>>1&1==1,A>>2&1==1,A>>3&1==1,A>>4&1==1
		else:return A>>4&1==1,A>>3&1==1,A>>2&1==1,A>>1&1==1,A>>0&1==1
	def hsl_to_rgb(G,h,s,l):
		D=(1-abs(2*l-1))*s;E=D*(1-abs(h/60%2-1));F=l-D/2
		if 0<=h<60:A,B,C=D,E,0
		elif 60<=h<120:A,B,C=E,D,0
		elif 120<=h<180:A,B,C=0,D,E
		elif 180<=h<240:A,B,C=0,E,D
		elif 240<=h<300:A,B,C=E,0,D
		elif 300<=h<360:A,B,C=D,0,E
		else:A,B,C=0,0,0
		A=(A+F)*255;B=(B+F)*255;C=(C+F)*255;return int(A),int(B),int(C)
	def set_underglow_light(B,light,rgb_tuple):
		A=light
		if A>=0 and A<4:B._d[A]=rgb_tuple;B._d.show()
	def set_underglow(A,rgb_tuple):
		for B in range(4):A._d[B]=rgb_tuple
		A._d.show()
	def set_underglow_off(A):A.set_underglow((0,0,0))