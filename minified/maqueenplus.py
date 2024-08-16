_A=None
import machine,math
from time import sleep_ms
import microbit
class MaqueenPlus:
	_g=16;_q=50;_p=51;_n=11;_o=12;_k=0;_m=2;_j=4;_l=6;_h=29;_r=42;HEADLIGHT_LEFT=1;HEADLIGHT_RIGHT=2;HEADLIGHT_BOTH=3;COLOR_RED=1;COLOR_GREEN=2;COLOR_YELLOW=3;COLOR_BLUE=4;COLOR_PINK=5;COLOR_CYAN=6;COLOR_WHITE=7;COLOR_OFF=8;MOTOR_LEFT=1;MOTOR_RIGHT=2;MOTOR_BOTH=3;MOTOR_DIR_STOP=0;MOTOR_DIR_FORWARD=1;MOTOR_DIR_BACKWARD=2;SERVO_S1=20;SERVO_S2=21;SERVO_S3=22;_i=500
	def __init__(A,ultrasonic_trigger_pin=_A,ultrasonic_echo_pin=_A,ultrasonic_sensor_model='URM10'):
		D=ultrasonic_sensor_model;C=False
		while A._g not in microbit.i2c.scan():microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		B=C
		while B==C:
			F=A._a();E=F[-3:];A._w=int(E[0]);A._x=int(E[2])
			if A._w==1 and A._x==4:B=True
			if B==C:microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		A._u=0;A._v=ultrasonic_trigger_pin;A._s=ultrasonic_echo_pin
		if D=='URM10':A._t=1
		elif D.endswith('SRO4'):A._t=2
		else:A._t=-1
		A._y=A._r;A.set_headlight_rgb(A.HEADLIGHT_BOTH,A.COLOR_OFF);A.motor_stop(A.MOTOR_BOTH);A.clear_wheel_rotations(A.MOTOR_BOTH);microbit.display.show(microbit.Image.YES);microbit.display.clear()
	def _e(A,buf):microbit.i2c.write(A._g,bytes(buf))
	def _d(A,count):return microbit.i2c.read(A._g,count)
	def _a(A):A._e([A._q]);B=int.from_bytes(A._d(1),'big');A._e([A._p]);C=A._d(B);D=''.join([chr(A)for A in C]);return D
	def set_headlight_rgb(A,light,color):
		C=light;B=color
		if C==A.HEADLIGHT_LEFT:A._e([A._n,B])
		elif C==A.HEADLIGHT_RIGHT:A._e([A._o,B])
		elif C==A.HEADLIGHT_BOTH:A._e([A._n,B,B])
	def motor_run(A,motor,dir,speed):
		C=motor;B=speed
		if B>240:B=240
		if C==A.MOTOR_LEFT:A._e(buf=[A._k,dir,B])
		elif C==A.MOTOR_RIGHT:A._e([A._m,dir,B])
		elif C==A.MOTOR_BOTH:A._e([A._k,dir,B,dir,B])
	def motor_stop(A,motor):A.motor_run(motor,A.MOTOR_DIR_STOP,0)
	def drive_foward(A,speed):A.motor_run(A.MOTOR_BOTH,A.MOTOR_DIR_FORWARD,speed)
	def drive_backward(A,speed):A.motor_run(A.MOTOR_BOTH,A.MOTOR_DIR_BACKWARD,speed)
	def spin_left(A,speed):B=speed;A.motor_run(A.MOTOR_LEFT,A.MOTOR_DIR_BACKWARD,B);A.motor_run(A.MOTOR_RIGHT,A.MOTOR_DIR_FORWARD,B)
	def spin_right(A,speed):B=speed;A.motor_run(A.MOTOR_LEFT,A.MOTOR_DIR_FORWARD,B);A.motor_run(A.MOTOR_RIGHT,A.MOTOR_DIR_BACKWARD,B)
	def get_range_cm(A):
		if A._v is _A or A._s is _A:return-1
		if A._t==1:return A._b()
		elif A._t==2:return A._c()
		else:return-1
	def _b(A):
		B=A._f()
		if A._u==1 and B!=0:A._u=0
		C=0
		if A._u==0:
			while B==0:
				B=A._f();C+=1
				if C>3:A._u=1;B=A._i
		if B==0:B=A._i
		return B
	def _f(A):
		A._v.write_digital(0)
		if A._s.read_digital()==0:A._v.write_digital(0);A._v.write_digital(1);sleep_ms(20);A._v.write_digital(0);B=machine.time_pulse_us(A._s,1,A._i*58)
		else:A._v.write_digital(1);A._v.write_digital(0);sleep_ms(20);A._v.write_digital(0);B=machine.time_pulse_us(A._s,0,A._i*58)
		C=B/59;return round(C)
	def _c(A):
		A._v.write_digital(1);sleep_ms(1);A._v.write_digital(0)
		if A._s.read_digital()==0:A._v.write_digital(0);A._v.write_digital(1);sleep_ms(20);A._v.write_digital(0);C=machine.time_pulse_us(A._s,1,A._i*58)
		else:A._v.write_digital(1);A._v.write_digital(0);sleep_ms(20);A._v.write_digital(0);C=machine.time_pulse_us(A._s,0,A._i*58)
		B=C/59
		if B<=0:return 0
		if B>=A._i:return A._i
		return round(B)
	def servo(B,servo,angle):
		A=angle
		if A<0:A=0
		elif A>180:A=180
		B._e([servo,A])
	def line_track(B):B._e([B._h]);A=int.from_bytes(B._d(1),'big');return A>>0&1==1,A>>1&1==1,A>>2&1==1,A>>3&1==1,A>>4&1==1,A>>5&1==1
	def get_wheel_rotations(B):B._e([B._j]);A=B._d(4);C=(A[0]<<8|A[1])*10/900;D=(A[2]<<8|A[3])*10/900;return C,D
	def clear_wheel_rotations(A,motor):
		B=motor
		if B==A.MOTOR_LEFT:A._e(buf=[A._j,0,0])
		elif B==A.MOTOR_RIGHT:A._e(buf=[A._l,0,0])
		elif B==A.MOTOR_BOTH:A._e(buf=[A._j,0,0,0,0])
	def set_wheel_diameter_mm(A,new_diameter_mm):A._y=new_diameter_mm
	def get_wheel_distance_cm(A):B,C=A.get_wheel_rotations();D=B*math.pi*A._y/10;E=C*math.pi*A._y/10;return D,E