import machine
from time import sleep_ms
import microbit
from neopixel import NeoPixel
class MaqueenPlusV2:
	_I2C_ROBOT_ADDR=16;_VER_SIZE_REG=50;_VER_DATA_REG=51;_LED_LEFT_REG=11;_LED_RIGHT_REG=12;_MOTOR_LEFT_REG=0;_MOTOR_RIGHT_REG=2;_LINE_TRACK_REG=29;LED_LEFT=1;LED_RIGHT=2;LED_BOTH=3;LED_OFF=0;LED_ON=1;MOTOR_LEFT=1;MOTOR_RIGHT=2;MOTOR_BOTH=3;MOTOR_DIR_STOP=0;MOTOR_DIR_FORWARD=0;MOTOR_DIR_BACKWARD=1;SERVO_P0=0;SERVO_P1=1;SERVO_P2=2;_MAX_DIST_CM=500;COLOR_RED=255,0,0;COLOR_ORANGE_RED=255,64,0;COLOR_ORANGE=255,128,0;COLOR_YELLOW_ORANGE=255,191,0;COLOR_YELLOW=255,255,0;COLOR_YELLOW_GREEN=191,255,0;COLOR_GREEN=128,255,0;COLOR_SPRING_GREEN=64,255,0;COLOR_CYAN=0,255,255;COLOR_SKY_BLUE=0,191,255;COLOR_BLUE=0,128,255;COLOR_VIOLET_BLUE=0,64,255;COLOR_INDIGO=0,0,255;COLOR_VIOLET=64,0,255;COLOR_MAGENTA=128,0,255;COLOR_ROSE=191,0,255;COLOR_LIST_RAINBOW=[COLOR_RED,COLOR_ORANGE_RED,COLOR_ORANGE,COLOR_YELLOW_ORANGE,COLOR_YELLOW,COLOR_YELLOW_GREEN,COLOR_GREEN,COLOR_SPRING_GREEN,COLOR_CYAN,COLOR_SKY_BLUE,COLOR_BLUE,COLOR_VIOLET_BLUE,COLOR_INDIGO,COLOR_VIOLET,COLOR_MAGENTA,COLOR_ROSE];_NEO_PIXEL_COUNT=4
	def __init__(A):
		C=False
		while A._I2C_ROBOT_ADDR not in microbit.i2c.scan():microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		B=C
		while B==C:
			E=A._get_board_version();D=E[-3:];A._version_major=int(D[0]);A._version_minor=int(D[2])
			if A._version_major==2 and A._version_minor==1:B=True
			if B==C:microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		A._neo_pixel=NeoPixel(microbit.pin15,A._NEO_PIXEL_COUNT);A.motor_stop(A.MOTOR_BOTH);A.set_led_light(A.LED_BOTH,A.LED_OFF);A.set_underglow_off();microbit.display.show(microbit.Image.YES);microbit.display.clear()
	def _i2c_write(A,buf):microbit.i2c.write(A._I2C_ROBOT_ADDR,bytes(buf))
	def _i2c_read(A,count):return microbit.i2c.read(A._I2C_ROBOT_ADDR,count)
	def _get_board_version(A):A._i2c_write([A._VER_SIZE_REG]);B=int.from_bytes(A._i2c_read(1),'big');A._i2c_write([A._VER_DATA_REG]);C=A._i2c_read(B);D=''.join([chr(A)for A in C]);return D
	def set_led_light(A,light,state):
		C=light;B=state
		if C==A.LED_LEFT:A._i2c_write([A._LED_LEFT_REG,B])
		elif C==A.LED_RIGHT:A._i2c_write([A._LED_RIGHT_REG,B])
		elif C==A.LED_BOTH:A._i2c_write([A._LED_LEFT_REG,B,B])
	def motor_run(A,motor,dir,speed):
		C=motor;B=speed
		if B>240:B=240
		if C==A.MOTOR_LEFT:A._i2c_write([A._MOTOR_LEFT_REG,dir,B])
		elif C==A.MOTOR_RIGHT:A._i2c_write([A._MOTOR_RIGHT_REG,dir,B])
		elif C==A.MOTOR_BOTH:A._i2c_write([A._MOTOR_LEFT_REG,dir,B,dir,B])
	def motor_stop(A,motor):A.motor_run(motor,A.MOTOR_DIR_STOP,0)
	def get_range(B):
		A=microbit.pin13;C=microbit.pin14;A.write_digital(1);sleep_ms(1);A.write_digital(0)
		if C.read_digital()==0:A.write_digital(0);A.write_digital(1);sleep_ms(20);A.write_digital(0);E=machine.time_pulse_us(C,1,B._MAX_DIST_CM*58)
		else:A.write_digital(1);A.write_digital(0);sleep_ms(20);A.write_digital(0);E=machine.time_pulse_us(C,0,B._MAX_DIST_CM*58)
		D=E/59
		if D<=0:return 0
		if D>=B._MAX_DIST_CM:return B._MAX_DIST_CM
		return round(D)
	def servo(B,servo_id,angle):
		C=servo_id;A=angle
		if A<0:A=0
		elif A>180:A=180
		if C==B.SERVO_P0:microbit.pin0.write_analog(A)
		elif C==B.SERVO_P1:microbit.pin1.write_analog(A)
		elif C==B.SERVO_P2:microbit.pin2.write_analog(A)
	def line_track(B):
		B._i2c_write([B._LINE_TRACK_REG]);A=int.from_bytes(B._i2c_read(1),'big')
		if B._version_minor==0:return A>>0&1==1,A>>1&1==1,A>>2&1==1,A>>3&1==1,A>>4&1==1
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
	def set_underglow_light(A,light,r,g,b):
		B=light
		if B>0 and B<A._NEO_PIXEL_COUNT:A._neo_pixel[B]=r,g,b;A._neo_pixel.show()
	def set_underglow(A,r,g,b):
		for B in range(A._NEO_PIXEL_COUNT):A._neo_pixel[B]=r,g,b
		A._neo_pixel.show()
	def set_underglow_off(A):A.set_underglow(0,0,0)