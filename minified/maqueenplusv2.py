import machine
from time import sleep_ms
import microbit
from neopixel import NeoPixel
class MaqueenPlusV2:
	_d=16;_m=50;_l=51;_e=11;_f=12;_i=0;_j=2;_g=29;HEADLIGHT_LEFT=1;HEADLIGHT_RIGHT=2;HEADLIGHT_BOTH=3;LED_OFF=0;LED_ON=1;MOTOR_LEFT=1;MOTOR_RIGHT=2;MOTOR_BOTH=3;MOTOR_DIR_STOP=0;MOTOR_DIR_FORWARD=0;MOTOR_DIR_BACKWARD=1;SERVO_P0=0;SERVO_P1=1;SERVO_P2=2;_h=500;COLOR_RED=255,0,0;COLOR_ORANGE_RED=255,64,0;COLOR_ORANGE=255,128,0;COLOR_YELLOW_ORANGE=255,191,0;COLOR_YELLOW=255,255,0;COLOR_YELLOW_GREEN=191,255,0;COLOR_GREEN=128,255,0;COLOR_SPRING_GREEN=64,255,0;COLOR_CYAN=0,255,255;COLOR_SKY_BLUE=0,191,255;COLOR_BLUE=0,128,255;COLOR_VIOLET_BLUE=0,64,255;COLOR_INDIGO=0,0,255;COLOR_VIOLET=64,0,255;COLOR_MAGENTA=128,0,255;COLOR_ROSE=191,0,255;COLOR_LIST_RAINBOW=[COLOR_RED,COLOR_ORANGE_RED,COLOR_ORANGE,COLOR_YELLOW_ORANGE,COLOR_YELLOW,COLOR_YELLOW_GREEN,COLOR_GREEN,COLOR_SPRING_GREEN,COLOR_CYAN,COLOR_SKY_BLUE,COLOR_BLUE,COLOR_VIOLET_BLUE,COLOR_INDIGO,COLOR_VIOLET,COLOR_MAGENTA,COLOR_ROSE];_k=4
	def __init__(A,ultrasonic_trigger_pin=microbit.pin13,ultrasonic_echo_pin=microbit.pin14):
		C=False
		while A._d not in microbit.i2c.scan():microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		B=C
		while B==C:
			E=A._a();D=E[-3:];A._q=int(D[0]);A._r=int(D[2])
			if A._q==2 and A._r==1:B=True
			if B==C:microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		A._p=ultrasonic_trigger_pin;A._o=ultrasonic_echo_pin;A._n=NeoPixel(microbit.pin15,A._k);A.motor_stop(A.MOTOR_BOTH);A.set_headlight(A.HEADLIGHT_BOTH,A.LED_OFF);A.set_underglow_off();microbit.display.show(microbit.Image.YES);microbit.display.clear()
	def _c(A,buf):microbit.i2c.write(A._d,bytes(buf))
	def _b(A,count):return microbit.i2c.read(A._d,count)
	def _a(A):A._c([A._m]);B=int.from_bytes(A._b(1),'big');A._c([A._l]);C=A._b(B);D=''.join([chr(A)for A in C]);return D
	def set_headlight(A,light,state):
		C=light;B=state
		if C==A.HEADLIGHT_LEFT:A._c([A._e,B])
		elif C==A.HEADLIGHT_RIGHT:A._c([A._f,B])
		elif C==A.HEADLIGHT_BOTH:A._c([A._e,B,B])
	def motor_run(A,motor,dir,speed):
		C=motor;B=speed
		if B>240:B=240
		if C==A.MOTOR_LEFT:A._c([A._i,dir,B])
		elif C==A.MOTOR_RIGHT:A._c([A._j,dir,B])
		elif C==A.MOTOR_BOTH:A._c([A._i,dir,B,dir,B])
	def motor_stop(A,motor):A.motor_run(motor,A.MOTOR_DIR_STOP,0)
	def drive_foward(A,speed):A.motor_run(A.MOTOR_BOTH,A.MOTOR_DIR_FORWARD,speed)
	def drive_backward(A,speed):A.motor_run(A.MOTOR_BOTH,A.MOTOR_DIR_BACKWARD,speed)
	def spin_left(A,speed):B=speed;A.motor_run(A.MOTOR_LEFT,A.MOTOR_DIR_BACKWARD,B);A.motor_run(A.MOTOR_RIGHT,A.MOTOR_DIR_FORWARD,B)
	def spin_right(A,speed):B=speed;A.motor_run(A.MOTOR_LEFT,A.MOTOR_DIR_FORWARD,B);A.motor_run(A.MOTOR_RIGHT,A.MOTOR_DIR_BACKWARD,B)
	def get_range_cm(A):
		A._p.write_digital(1);sleep_ms(1);A._p.write_digital(0)
		if A._o.read_digital()==0:A._p.write_digital(0);A._p.write_digital(1);sleep_ms(20);A._p.write_digital(0);C=machine.time_pulse_us(A._o,1,A._h*58)
		else:A._p.write_digital(1);A._p.write_digital(0);sleep_ms(20);A._p.write_digital(0);C=machine.time_pulse_us(A._o,0,A._h*58)
		B=C/59
		if B<=0:return 0
		if B>=A._h:return A._h
		return round(B)
	def servo(B,servo_id,angle):
		C=servo_id;A=angle
		if A<0:A=0
		elif A>180:A=180
		if C==B.SERVO_P0:microbit.pin0.write_analog(A)
		elif C==B.SERVO_P1:microbit.pin1.write_analog(A)
		elif C==B.SERVO_P2:microbit.pin2.write_analog(A)
	def line_track(B):
		B._c([B._g]);A=int.from_bytes(B._b(1),'big')
		if B._r==0:return A>>0&1==1,A>>1&1==1,A>>2&1==1,A>>3&1==1,A>>4&1==1
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
	def set_underglow_light(A,light,rgb_tuple):
		B=light
		if B>=0 and B<A._k:A._n[B]=rgb_tuple;A._n.show()
	def set_underglow(A,rgb_tuple):
		for B in range(A._k):A._n[B]=rgb_tuple
		A._n.show()
	def set_underglow_off(A):A.set_underglow((0,0,0))