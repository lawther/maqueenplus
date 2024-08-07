import machine
from time import sleep_ms
import microbit
class MaqueenPlus:
	_I2C_ROBOT_ADDR=16;_VER_SIZE_REG=50;_VER_DATA_REG=51;_RGB_LEFT_REG=11;_RGB_RIGHT_REG=12;_MOTOR_LEFT_REG=0;_MOTOR_RIGHT_REG=2;_LINE_TRACK_REG=29;RGB_LEFT=1;RGB_RIGHT=2;RGB_BOTH=3;COLOR_RED=1;COLOR_GREEN=2;COLOR_YELLOW=3;COLOR_BLUE=4;COLOR_PINK=5;COLOR_CYAN=6;COLOR_WHITE=7;COLOR_OFF=8;MOTOR_LEFT=1;MOTOR_RIGHT=2;MOTOR_BOTH=3;MOTOR_DIR_STOP=0;MOTOR_DIR_FORWARD=1;MOTOR_DIR_BACKWARD=2;SERVO_S1=20;SERVO_S2=21;SERVO_S3=22;_MAX_DIST_CM=500
	def __init__(A,ultrasonic_green_pin,ultrasonic_blue_pin):
		D=False
		while A._I2C_ROBOT_ADDR not in microbit.i2c.scan():print('Could not find Maqueen on I2C');microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		B=D
		while B==D:
			E=A._get_board_version();C=E[-3:];microbit.display.scroll(C);A._version_major=int(C[0]);A._version_minor=int(C[2])
			if A._version_major==1 and A._version_minor==4:B=True
			if B==D:print('Version %d.%d is not supported'%(A._version_major,A._version_minor));microbit.display.show(microbit.Image.NO);sleep_ms(1000)
		A._ultrasonic_state=0;A._ultrasonic_trigger_pin=ultrasonic_green_pin;A._ultrasonic_echo_pin=ultrasonic_blue_pin;A.set_rgb_light(A.RGB_BOTH,A.COLOR_OFF);A.motor_stop(A.MOTOR_BOTH);microbit.display.show(microbit.Image.YES);sleep_ms(500);microbit.display.clear()
	def _i2c_write(A,buf):microbit.i2c.write(A._I2C_ROBOT_ADDR,bytes(buf))
	def _i2c_read(A,count):return microbit.i2c.read(A._I2C_ROBOT_ADDR,count)
	def _get_board_version(A):A._i2c_write([A._VER_SIZE_REG]);B=int.from_bytes(A._i2c_read(1),'big');A._i2c_write([A._VER_DATA_REG]);C=A._i2c_read(B);D=''.join([chr(A)for A in C]);return D
	def set_rgb_light(A,light,color):
		C=light;B=color
		if C==A.RGB_LEFT:A._i2c_write([A._RGB_LEFT_REG,B])
		elif C==A.RGB_RIGHT:A._i2c_write([A._RGB_RIGHT_REG,B])
		elif C==A.RGB_BOTH:A._i2c_write([A._RGB_LEFT_REG,B,B])
	def motor_run(A,motor,dir,speed):
		C=motor;B=speed
		if B>240:B=240
		if C==A.MOTOR_LEFT:A._i2c_write([A._MOTOR_LEFT_REG,dir,B])
		elif C==A.MOTOR_RIGHT:A._i2c_write([A._MOTOR_RIGHT_REG,dir,B])
		elif C==A.MOTOR_BOTH:A._i2c_write([A._MOTOR_LEFT_REG,dir,B,dir,B])
	def motor_stop(A,motor):A.motor_run(motor,A.MOTOR_DIR_STOP,0)
	def get_range(A):
		B=A._read_ultrasonic()
		if A._ultrasonic_state==1 and B!=0:A._ultrasonic_state=0
		C=0
		if A._ultrasonic_state==0:
			while B==0:
				B=A._read_ultrasonic();C+=1
				if C>3:A._ultrasonic_state=1;B=A._MAX_DIST_CM
		if B==0:B=A._MAX_DIST_CM
		return B
	def _read_ultrasonic(A):
		A._ultrasonic_trigger_pin.write_digital(0)
		if A._ultrasonic_echo_pin.read_digital()==0:A._ultrasonic_trigger_pin.write_digital(0);A._ultrasonic_trigger_pin.write_digital(1);sleep_ms(20);A._ultrasonic_trigger_pin.write_digital(0);B=machine.time_pulse_us(A._ultrasonic_echo_pin,1,A._MAX_DIST_CM*58)
		else:A._ultrasonic_trigger_pin.write_digital(1);A._ultrasonic_trigger_pin.write_digital(0);sleep_ms(20);A._ultrasonic_trigger_pin.write_digital(0);B=machine.time_pulse_us(A._ultrasonic_echo_pin,0,A._MAX_DIST_CM*58)
		C=B/59;return round(C)
	def servo(B,servo,angle):
		A=angle
		if A<0:A=0
		elif A>180:A=180
		B._i2c_write([servo,A])
	def line_track(B):B._i2c_write([B._LINE_TRACK_REG]);A=int.from_bytes(B._i2c_read(1),'big');return[A>>0&1,A>>1&1,A>>2&1,A>>3&1,A>>4&1,A>>5&1]