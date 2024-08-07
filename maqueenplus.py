import machine
from time import sleep_ms

import microbit


class MaqueenPlus:

    # Microbit I2C secondary, in our case the Maqueen robot
    _I2C_ROBOT_ADDR = 0x10

    # Robot version length and location
    _VER_SIZE_REG = 0x32
    _VER_DATA_REG = 0x33

    # RGB LEDs
    _RGB_LEFT_REG = 0x0B
    _RGB_RIGHT_REG = 0x0C

    # Motors
    _MOTOR_LEFT_REG = 0x00
    _MOTOR_RIGHT_REG = 0x02

    # Line Tracking Sensors
    _LINE_TRACK_REG = 0x1D

    # RGB LEDs aka headlights
    RGB_LEFT = 1
    RGB_RIGHT = 2
    RGB_BOTH = 3

    # Colors for the RGB LEDs
    COLOR_RED = 1
    COLOR_GREEN = 2
    COLOR_YELLOW = 3
    COLOR_BLUE = 4
    COLOR_PINK = 5
    COLOR_CYAN = 6
    COLOR_WHITE = 7
    COLOR_OFF = 8

    # Main motors
    MOTOR_LEFT = 1
    MOTOR_RIGHT = 2
    MOTOR_BOTH = 3

    # Directions for the main motors
    MOTOR_DIR_STOP = 0
    MOTOR_DIR_FORWARD = 1
    MOTOR_DIR_BACKWARD = 2

    # Servo motors
    SERVO_S1 = 0x14
    SERVO_S2 = 0x15
    SERVO_S3 = 0x16

    # Ultrasonic distance
    _MAX_DIST_CM = 500

    def __init__(
        self,
        ultrasonic_green_pin: microbit.MicroBitDigitalPin,
        ultrasonic_blue_pin: microbit.MicroBitDigitalPin,
    ):
        # """Checks we can communicate with the robot.
        # Proceeds if the version number is one that is supported by this driver.
        # """
        while self._I2C_ROBOT_ADDR not in microbit.i2c.scan():
            print("Could not find Maqueen on I2C")
            microbit.display.show(microbit.Image.NO)
            sleep_ms(1000)

        valid_version = False
        while valid_version == False:
            version = self._get_board_version()
            # print("Found Maqueen Board " + version)
            version_num = version[-3:]
            microbit.display.scroll(version_num)
            self._version_major = int(version_num[0])
            self._version_minor = int(version_num[2])
            if self._version_major == 1 and self._version_minor == 4:
                valid_version = True
            if valid_version == False:
                print(
                    "Version %d.%d is not supported"
                    % (self._version_major, self._version_minor)
                )
                microbit.display.show(microbit.Image.NO)
                sleep_ms(1000)
        self._ultrasonic_state = 0
        self._ultrasonic_trigger_pin = ultrasonic_green_pin
        self._ultrasonic_echo_pin = ultrasonic_blue_pin
        self.set_rgb_light(self.RGB_BOTH, self.COLOR_OFF)
        self.motor_stop(self.MOTOR_BOTH)

        microbit.display.show(microbit.Image.YES)
        sleep_ms(500)
        microbit.display.clear()

    def _i2c_write(self, buf):
        microbit.i2c.write(self._I2C_ROBOT_ADDR, bytes(buf))

    def _i2c_read(self, count):
        return microbit.i2c.read(self._I2C_ROBOT_ADDR, count)

    def _get_board_version(self):
        # """Return the Maqueen board version as a string. The last 3 characters are the version."""
        self._i2c_write([self._VER_SIZE_REG])
        count = int.from_bytes(self._i2c_read(1), "big")
        self._i2c_write([self._VER_DATA_REG])
        version_bytes = self._i2c_read(count)
        version_str = "".join([chr(b) for b in version_bytes])
        return version_str

    def set_rgb_light(self, light, color):
        if light == self.RGB_LEFT:
            self._i2c_write([self._RGB_LEFT_REG, color])
        elif light == self.RGB_RIGHT:
            self._i2c_write([self._RGB_RIGHT_REG, color])
        elif light == self.RGB_BOTH:
            self._i2c_write([self._RGB_LEFT_REG, color, color])

    def motor_run(self, motor, dir, speed):
        if speed > 240:
            speed = 240

        if motor == self.MOTOR_LEFT:
            self._i2c_write([self._MOTOR_LEFT_REG, dir, speed])
        elif motor == self.MOTOR_RIGHT:
            self._i2c_write([self._MOTOR_RIGHT_REG, dir, speed])
        elif motor == self.MOTOR_BOTH:
            self._i2c_write([self._MOTOR_LEFT_REG, dir, speed, dir, speed])

    def motor_stop(self, motor):
        self.motor_run(motor, self.MOTOR_DIR_STOP, 0)

    def get_range(self):
        # """Returns a range in cm from 2 to 500"""

        data = self._read_ultrasonic()
        if self._ultrasonic_state == 1 and data != 0:
            self._ultrasonic_state = 0
        tries = 0

        if self._ultrasonic_state == 0:
            while data == 0:
                data = self._read_ultrasonic()
                tries += 1
                if tries > 3:
                    self._ultrasonic_state = 1
                    data = self._MAX_DIST_CM

        if data == 0:
            data = self._MAX_DIST_CM

        return data

    def _read_ultrasonic(self):
        self._ultrasonic_trigger_pin.write_digital(0)
        if self._ultrasonic_echo_pin.read_digital() == 0:
            self._ultrasonic_trigger_pin.write_digital(0)
            self._ultrasonic_trigger_pin.write_digital(1)
            sleep_ms(20)
            self._ultrasonic_trigger_pin.write_digital(0)
            d = machine.time_pulse_us(
                self._ultrasonic_echo_pin, 1, self._MAX_DIST_CM * 58
            )
        else:
            self._ultrasonic_trigger_pin.write_digital(1)
            self._ultrasonic_trigger_pin.write_digital(0)
            sleep_ms(20)
            self._ultrasonic_trigger_pin.write_digital(0)
            d = machine.time_pulse_us(
                self._ultrasonic_echo_pin, 0, self._MAX_DIST_CM * 58
            )
        x = d / 59
        return round(x)

    def servo(self, servo, angle):
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        self._i2c_write([servo, angle])

    def line_track(self):
        self._i2c_write([self._LINE_TRACK_REG])
        sensor_bits = int.from_bytes(self._i2c_read(1), "big")
        return [
            (sensor_bits >> 0) & 1,
            (sensor_bits >> 1) & 1,
            (sensor_bits >> 2) & 1,
            (sensor_bits >> 3) & 1,
            (sensor_bits >> 4) & 1,
            (sensor_bits >> 5) & 1,
        ]
