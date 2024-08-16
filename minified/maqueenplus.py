_A=None
import machine,math
from time import sleep_ms
import microbit
class MaqueenPlus:
	HEADLIGHT_LEFT=1;HEADLIGHT_RIGHT=2;HEADLIGHT_BOTH=3;COLOR_RED=1;COLOR_GREEN=2;COLOR_YELLOW=3;COLOR_BLUE=4;COLOR_PINK=5;COLOR_CYAN=6;COLOR_WHITE=7;COLOR_OFF=8;MOTOR_LEFT=1;MOTOR_RIGHT=2;MOTOR_BOTH=3;MOTOR_DIR_STOP=0;MOTOR_DIR_FORWARD=1;MOTOR_DIR_BACKWARD=2;SERVO_S1=20;SERVO_S2=21;SERVO_S3=22
	def __init__(A,ultrasonic_trigger_pin=_A,ultrasonic_echo_pin=_A,ultrasonic_sensor_model='URM10'):
		D=ultrasonic_sensor_model;C=False
		while 16 not in microbit.i2c.scan():microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		B=C
		while B==C:
			F=A._a();E=F[-3:];A._k=int(E[0]);A._l=int(E[2])
			if A._k==1 and A._l==4:B=True
			if B==C:microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		A._i=0;A._j=ultrasonic_trigger_pin;A._g=ultrasonic_echo_pin
		if D=='URM10':A._h=1
		elif D.endswith('SRO4'):A._h=2
		else:A._h=-1
		A._m=42;A.set_headlight_rgb(3,8);A.motor_stop(3);A.clear_wheel_rotations(3);microbit.display.show(microbit.Image.YES);microbit.display.clear()
	def _e(A,buf):microbit.i2c.write(16,bytes(buf))
	def _d(A,count):return microbit.i2c.read(16,count)
	def _a(A):A._e([50]);B=int.from_bytes(A._d(1),'big');A._e([51]);C=A._d(B);D=''.join([chr(A)for A in C]);return D
	def set_headlight_rgb(B,light,color):
		C=light;A=color
		if C==1:B._e([11,A])
		elif C==2:B._e([12,A])
		elif C==3:B._e([11,A,A])
	def motor_run(B,motor,dir,speed):
		C=motor;A=speed
		if A>240:A=240
		if C==1:B._e(buf=[0,dir,A])
		elif C==2:B._e([2,dir,A])
		elif C==3:B._e([0,dir,A,dir,A])
	def motor_stop(A,motor):A.motor_run(motor,0,0)
	def drive_foward(A,speed):A.motor_run(3,1,speed)
	def drive_backward(A,speed):A.motor_run(3,2,speed)
	def spin_left(A,speed):B=speed;A.motor_run(1,2,B);A.motor_run(2,1,B)
	def spin_right(A,speed):B=speed;A.motor_run(1,1,B);A.motor_run(2,2,B)
	def get_range_cm(A):
		if A._j is _A or A._g is _A:return-1
		if A._h==1:return A._b()
		elif A._h==2:return A._c()
		else:return-1
	def _b(B):
		A=B._f()
		if B._i==1 and A!=0:B._i=0
		C=0
		if B._i==0:
			while A==0:
				A=B._f();C+=1
				if C>3:B._i=1;A=500
		if A==0:A=500
		return A
	def _f(A):
		A._j.write_digital(0)
		if A._g.read_digital()==0:A._j.write_digital(0);A._j.write_digital(1);sleep_ms(20);A._j.write_digital(0);B=machine.time_pulse_us(A._g,1,500*58)
		else:A._j.write_digital(1);A._j.write_digital(0);sleep_ms(20);A._j.write_digital(0);B=machine.time_pulse_us(A._g,0,500*58)
		C=B/59;return round(C)
	def _c(A):
		A._j.write_digital(1);sleep_ms(1);A._j.write_digital(0)
		if A._g.read_digital()==0:A._j.write_digital(0);A._j.write_digital(1);sleep_ms(20);A._j.write_digital(0);C=machine.time_pulse_us(A._g,1,500*58)
		else:A._j.write_digital(1);A._j.write_digital(0);sleep_ms(20);A._j.write_digital(0);C=machine.time_pulse_us(A._g,0,500*58)
		B=C/59
		if B<=0:return 0
		if B>=500:return 500
		return round(B)
	def servo(B,servo,angle):
		A=angle
		if A<0:A=0
		elif A>180:A=180
		B._e([servo,A])
	def line_track(B):B._e([29]);A=int.from_bytes(B._d(1),'big');return A>>0&1==1,A>>1&1==1,A>>2&1==1,A>>3&1==1,A>>4&1==1,A>>5&1==1
	def get_wheel_rotations(B):B._e([4]);A=B._d(4);C=(A[0]<<8|A[1])*10/900;D=(A[2]<<8|A[3])*10/900;return C,D
	def clear_wheel_rotations(A,motor):
		B=motor
		if B==1:A._e(buf=[4,0,0])
		elif B==2:A._e(buf=[6,0,0])
		elif B==3:A._e(buf=[4,0,0,0,0])
	def set_wheel_diameter_mm(A,new_diameter_mm):A._m=new_diameter_mm
	def get_wheel_distance_cm(A):B,C=A.get_wheel_rotations();D=B*math.pi*A._m/10;E=C*math.pi*A._m/10;return D,E