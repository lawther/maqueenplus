import machine
import math
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
    _MOTOR_LEFT_DISTANCE_REG = 0x04
    _MOTOR_RIGHT_DISTANCE_REG = 0x06

    # Line Tracking Sensors
    _LINE_TRACK_REG = 0x1D

    # Wheel diameter
    _WHEEL_DIAMETER_MM = 42

    # RGB Headlights
    HEADLIGHT_LEFT = 1
    HEADLIGHT_RIGHT = 2
    HEADLIGHT_BOTH = 3

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
        ultrasonic_trigger_pin: microbit.MicroBitDigitalPin = None,
        ultrasonic_echo_pin: microbit.MicroBitDigitalPin = None,
        ultrasonic_sensor_model: str = "URM10",
    ):
        """Initialises MaqueenPlus robot. Checks we can communicate
        with the robot. Only proceeds if the board version number is
        one that is supported by this driver.

        This driver also supports the ultrasonic sensors shipped with
        the MaqueenPlus V1 and V2 robots. The default is the "URM10"
        that came with the V1. You can also configure it with "HC-SRO4"
        that comes with the MaqueenPlus V2.
        """
        while self._I2C_ROBOT_ADDR not in microbit.i2c.scan():
            if __debug__:
                print("Could not find Maqueen on I2C")
            microbit.display.show(microbit.Image.NO)
            sleep_ms(1000)

        valid_version = False
        while valid_version == False:
            version = self._get_board_version()
            version_num = version[-3:]
            if __debug__:
                print("Found Maqueen Board " + version)
                microbit.display.scroll(version_num)
            self._version_major = int(version_num[0])
            self._version_minor = int(version_num[2])
            if self._version_major == 1 and self._version_minor == 4:
                valid_version = True
            if valid_version == False:
                if __debug__:
                    print(
                        "Version %d.%d is not supported"
                        % (self._version_major, self._version_minor)
                    )
                microbit.display.show(microbit.Image.NO)
                sleep_ms(1000)
        self._ultrasonic_state = 0
        self._ultrasonic_trigger_pin = ultrasonic_trigger_pin
        self._ultrasonic_echo_pin = ultrasonic_echo_pin
        if ultrasonic_sensor_model == "URM10":
            self._ultrasonic_sensor_version = 1
            if __debug__:
                print("Seting ultrasonic sensor to v1")
        elif ultrasonic_sensor_model.endswith("SRO4"):
            self._ultrasonic_sensor_version = 2
            if __debug__:
                print("Seting ultrasonic sensor to v2")
        else:
            self._ultrasonic_sensor_version = -1
            if __debug__:
                print(
                    "Ultrasonic sensor %s is not supported" % (ultrasonic_sensor_model)
                )
        self._wheel_diameter_mm = self._WHEEL_DIAMETER_MM
        self.set_headlight_rgb(self.HEADLIGHT_BOTH, self.COLOR_OFF)
        self.motor_stop(self.MOTOR_BOTH)
        self.clear_wheel_rotations(self.MOTOR_BOTH)

        microbit.display.show(microbit.Image.YES)
        if __debug__:
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

    def set_headlight_rgb(self, light, color):
        if light == self.HEADLIGHT_LEFT:
            self._i2c_write([self._RGB_LEFT_REG, color])
        elif light == self.HEADLIGHT_RIGHT:
            self._i2c_write([self._RGB_RIGHT_REG, color])
        elif light == self.HEADLIGHT_BOTH:
            self._i2c_write([self._RGB_LEFT_REG, color, color])

    def motor_run(self, motor, dir, speed):
        if speed > 240:
            speed = 240

        if motor == self.MOTOR_LEFT:
            self._i2c_write(buf=[self._MOTOR_LEFT_REG, dir, speed])
        elif motor == self.MOTOR_RIGHT:
            self._i2c_write([self._MOTOR_RIGHT_REG, dir, speed])
        elif motor == self.MOTOR_BOTH:
            self._i2c_write([self._MOTOR_LEFT_REG, dir, speed, dir, speed])

    def motor_stop(self, motor):
        self.motor_run(motor, self.MOTOR_DIR_STOP, 0)

    def drive_forward(self, speed):
        self.motor_run(self.MOTOR_BOTH, self.MOTOR_DIR_FORWARD, speed)

    def drive_backward(self, speed):
        self.motor_run(self.MOTOR_BOTH, self.MOTOR_DIR_BACKWARD, speed)

    def drive_stop(self):
        self.motor_stop(self.MOTOR_BOTH)

    def drive_spin_left(self, speed):
        self.motor_run(self.MOTOR_LEFT, self.MOTOR_DIR_BACKWARD, speed)
        self.motor_run(self.MOTOR_RIGHT, self.MOTOR_DIR_FORWARD, speed)

    def drive_spin_right(self, speed):
        self.motor_run(self.MOTOR_LEFT, self.MOTOR_DIR_FORWARD, speed)
        self.motor_run(self.MOTOR_RIGHT, self.MOTOR_DIR_BACKWARD, speed)

    def get_range_cm(self) -> int:

        if self._ultrasonic_trigger_pin is None or self._ultrasonic_echo_pin is None:
            if __debug__:
                print("Ultrasonic pins are not set!")
            return -1

        if self._ultrasonic_sensor_version == 1:
            return self._get_range_cm_v1()
        elif self._ultrasonic_sensor_version == 2:
            return self._get_range_cm_v2()
        else:
            return -1

    def _get_range_cm_v1(self):
        # """Returns a range in cm from 2 to 500"""

        data = self._read_ultrasonic_v1()
        if self._ultrasonic_state == 1 and data != 0:
            self._ultrasonic_state = 0
        tries = 0

        if self._ultrasonic_state == 0:
            while data == 0:
                data = self._read_ultrasonic_v1()
                tries += 1
                if tries > 3:
                    self._ultrasonic_state = 1
                    data = self._MAX_DIST_CM

        if data == 0:
            data = self._MAX_DIST_CM

        return data

    def _read_ultrasonic_v1(self):
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

    def _get_range_cm_v2(self):

        self._ultrasonic_trigger_pin.write_digital(1)
        sleep_ms(1)
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

        if x <= 0:
            return 0

        if x >= self._MAX_DIST_CM:
            return self._MAX_DIST_CM

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
        return (
            ((sensor_bits >> 0) & 1) == 1,
            ((sensor_bits >> 1) & 1) == 1,
            ((sensor_bits >> 2) & 1) == 1,
            ((sensor_bits >> 3) & 1) == 1,
            ((sensor_bits >> 4) & 1) == 1,
            ((sensor_bits >> 5) & 1) == 1,
        )

    def get_wheel_rotations(self):
        self._i2c_write([self._MOTOR_LEFT_DISTANCE_REG])
        raw_rotations = self._i2c_read(4)
        rotation_left = ((raw_rotations[0] << 8 | raw_rotations[1]) * 10) / 900
        rotation_right = ((raw_rotations[2] << 8 | raw_rotations[3]) * 10) / 900
        return (rotation_left, rotation_right)

    def clear_wheel_rotations(self, motor):
        if motor == self.MOTOR_LEFT:
            self._i2c_write(buf=[self._MOTOR_LEFT_DISTANCE_REG, 0, 0])
        elif motor == self.MOTOR_RIGHT:
            self._i2c_write(buf=[self._MOTOR_RIGHT_DISTANCE_REG, 0, 0])
        elif motor == self.MOTOR_BOTH:
            self._i2c_write(buf=[self._MOTOR_LEFT_DISTANCE_REG, 0, 0, 0, 0])

    def set_wheel_diameter_mm(self, new_diameter_mm: int):
        self._wheel_diameter_mm = new_diameter_mm

    def get_wheel_distance_cm(self):
        rotation_left, rotation_right = self.get_wheel_rotations()
        distance_left_cm = (rotation_left * math.pi * self._wheel_diameter_mm) / 10
        distance_right_cm = (rotation_right * math.pi * self._wheel_diameter_mm) / 10

        return (distance_left_cm, distance_right_cm)
