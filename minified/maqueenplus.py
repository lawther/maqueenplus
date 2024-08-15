import machine,math
from time import sleep_ms
import microbit
class MaqueenPlus:
	_e=16;_o=50;_n=51;_l=11;_m=12;_i=0;_k=2;_h=4;_j=6;_f=29;_p=42;HEADLIGHT_LEFT=1;HEADLIGHT_RIGHT=2;HEADLIGHT_BOTH=3;COLOR_RED=1;COLOR_GREEN=2;COLOR_YELLOW=3;COLOR_BLUE=4;COLOR_PINK=5;COLOR_CYAN=6;COLOR_WHITE=7;COLOR_OFF=8;MOTOR_LEFT=1;MOTOR_RIGHT=2;MOTOR_BOTH=3;MOTOR_DIR_STOP=0;MOTOR_DIR_FORWARD=1;MOTOR_DIR_BACKWARD=2;SERVO_S1=20;SERVO_S2=21;SERVO_S3=22;_g=500
	def __init__(A,ultrasonic_trigger_pin,ultrasonic_echo_pin):
		C=False
		while A._e not in microbit.i2c.scan():microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		B=C
		while B==C:
			E=A._a();D=E[-3:];A._t=int(D[0]);A._u=int(D[2])
			if A._t==1 and A._u==4:B=True
			if B==C:microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		A._r=0;A._s=ultrasonic_trigger_pin;A._q=ultrasonic_echo_pin;A._v=A._p;A.set_headlight_rgb(A.HEADLIGHT_BOTH,A.COLOR_OFF);A.motor_stop(A.MOTOR_BOTH);A.clear_wheel_rotations(A.MOTOR_BOTH);microbit.display.show(microbit.Image.YES);microbit.display.clear()
	def _c(A,buf):microbit.i2c.write(A._e,bytes(buf))
	def _b(A,count):return microbit.i2c.read(A._e,count)
	def _a(A):A._c([A._o]);B=int.from_bytes(A._b(1),'big');A._c([A._n]);C=A._b(B);D=''.join([chr(A)for A in C]);return D
	def set_headlight_rgb(A,light,color):
		C=light;B=color
		if C==A.HEADLIGHT_LEFT:A._c([A._l,B])
		elif C==A.HEADLIGHT_RIGHT:A._c([A._m,B])
		elif C==A.HEADLIGHT_BOTH:A._c([A._l,B,B])
	def motor_run(A,motor,dir,speed):
		C=motor;B=speed
		if B>240:B=240
		if C==A.MOTOR_LEFT:A._c(buf=[A._i,dir,B])
		elif C==A.MOTOR_RIGHT:A._c([A._k,dir,B])
		elif C==A.MOTOR_BOTH:A._c([A._i,dir,B,dir,B])
	def motor_stop(A,motor):A.motor_run(motor,A.MOTOR_DIR_STOP,0)
	def drive_foward(A,speed):A.motor_run(A.MOTOR_BOTH,A.MOTOR_DIR_FORWARD,speed)
	def drive_backward(A,speed):A.motor_run(A.MOTOR_BOTH,A.MOTOR_DIR_BACKWARD,speed)
	def spin_left(A,speed):B=speed;A.motor_run(A.MOTOR_LEFT,A.MOTOR_DIR_BACKWARD,B);A.motor_run(A.MOTOR_RIGHT,A.MOTOR_DIR_FORWARD,B)
	def spin_right(A,speed):B=speed;A.motor_run(A.MOTOR_LEFT,A.MOTOR_DIR_FORWARD,B);A.motor_run(A.MOTOR_RIGHT,A.MOTOR_DIR_BACKWARD,B)
	def get_range_cm(A):
		B=A._d()
		if A._r==1 and B!=0:A._r=0
		C=0
		if A._r==0:
			while B==0:
				B=A._d();C+=1
				if C>3:A._r=1;B=A._g
		if B==0:B=A._g
		return B
	def _d(A):
		A._s.write_digital(0)
		if A._q.read_digital()==0:A._s.write_digital(0);A._s.write_digital(1);sleep_ms(20);A._s.write_digital(0);B=machine.time_pulse_us(A._q,1,A._g*58)
		else:A._s.write_digital(1);A._s.write_digital(0);sleep_ms(20);A._s.write_digital(0);B=machine.time_pulse_us(A._q,0,A._g*58)
		C=B/59;return round(C)
	def servo(B,servo,angle):
		A=angle
		if A<0:A=0
		elif A>180:A=180
		B._c([servo,A])
	def line_track(B):B._c([B._f]);A=int.from_bytes(B._b(1),'big');return A>>0&1==1,A>>1&1==1,A>>2&1==1,A>>3&1==1,A>>4&1==1,A>>5&1==1
	def get_wheel_rotations(B):B._c([B._h]);A=B._b(4);C=(A[0]<<8|A[1])*10/900;D=(A[2]<<8|A[3])*10/900;return C,D
	def clear_wheel_rotations(A,motor):
		B=motor
		if B==A.MOTOR_LEFT:A._c(buf=[A._h,0,0])
		elif B==A.MOTOR_RIGHT:A._c(buf=[A._j,0,0])
		elif B==A.MOTOR_BOTH:A._c(buf=[A._h,0,0,0,0])
	def set_wheel_diameter_mm(A,new_diameter_mm):A._v=new_diameter_mm
	def get_wheel_distance_cm(A):B,C=A.get_wheel_rotations();D=B*math.pi*A._v/10;E=C*math.pi*A._v/10;return D,E