import machine
from time import sleep_ms

import microbit

from neopixel import NeoPixel


class MaqueenPlusV2:

    # Microbit I2C secondary, in our case the Maqueen robot
    _I2C_ROBOT_ADDR = 0x10

    # Robot version length and location
    _VER_SIZE_REG = 0x32
    _VER_DATA_REG = 0x33

    # LEDs
    _LED_LEFT_REG = 0x0B
    _LED_RIGHT_REG = 0x0C

    # Motors
    _MOTOR_LEFT_REG = 0x00
    _MOTOR_RIGHT_REG = 0x02

    # Line Tracking Sensors
    _LINE_TRACK_REG = 0x1D
    _LINE_TRACK_ANALOG_REG = 0x1E

    # Front Headlights
    HEADLIGHT_LEFT = 1
    HEADLIGHT_RIGHT = 2
    HEADLIGHT_BOTH = 3

    # State for the LEDs
    LED_OFF = 0
    LED_ON = 1

    # Main motors
    MOTOR_LEFT = 1
    MOTOR_RIGHT = 2
    MOTOR_BOTH = 3

    # Directions for the main motors
    MOTOR_DIR_STOP = 0
    MOTOR_DIR_FORWARD = 0
    MOTOR_DIR_BACKWARD = 1

    # Servo motors
    SERVO_P0 = 0
    SERVO_P1 = 1
    SERVO_P2 = 2

    # Ultrasonic range
    _MAX_DIST_CM = 500

    # Colors in rainbow order
    COLOR_RED = (255, 0, 0)
    COLOR_ORANGE_RED = (255, 64, 0)
    COLOR_ORANGE = (255, 128, 0)
    COLOR_YELLOW_ORANGE = (255, 191, 0)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_YELLOW_GREEN = (191, 255, 0)
    COLOR_GREEN = (128, 255, 0)
    COLOR_SPRING_GREEN = (64, 255, 0)
    COLOR_CYAN = (0, 255, 255)
    COLOR_SKY_BLUE = (0, 191, 255)
    COLOR_BLUE = (0, 128, 255)
    COLOR_VIOLET_BLUE = (0, 64, 255)
    COLOR_INDIGO = (0, 0, 255)
    COLOR_VIOLET = (64, 0, 255)
    COLOR_MAGENTA = (128, 0, 255)
    COLOR_ROSE = (191, 0, 255)

    COLOR_LIST_RAINBOW = [
        COLOR_RED,
        COLOR_ORANGE_RED,
        COLOR_ORANGE,
        COLOR_YELLOW_ORANGE,
        COLOR_YELLOW,
        COLOR_YELLOW_GREEN,
        COLOR_GREEN,
        COLOR_SPRING_GREEN,
        COLOR_CYAN,
        COLOR_SKY_BLUE,
        COLOR_BLUE,
        COLOR_VIOLET_BLUE,
        COLOR_INDIGO,
        COLOR_VIOLET,
        COLOR_MAGENTA,
        COLOR_ROSE,
    ]

    # NeoPixel / underglow
    _NEO_PIXEL_COUNT = 4

    def __init__(
        self,
        ultrasonic_trigger_pin: microbit.MicroBitDigitalPin = microbit.pin13,
        ultrasonic_echo_pin: microbit.MicroBitDigitalPin = microbit.pin14,
    ):
        # """Checks we can communicate with the robot.
        # Proceeds if the version number is one that is supported by this driver.
        # """
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
            if self._version_major == 2 and self._version_minor == 1:
                valid_version = True
            if valid_version == False:
                if __debug__:
                    print(
                        "Version %d.%d is not supported"
                        % (self._version_major, self._version_minor)
                    )
                microbit.display.show(microbit.Image.NO)
                sleep_ms(1000)

        # print("Version " + str(_version_major) + "." + str(_version_minor) + " is supported!")
        self._ultrasonic_trigger_pin = ultrasonic_trigger_pin
        self._ultrasonic_echo_pin = ultrasonic_echo_pin

        self._neo_pixel = NeoPixel(microbit.pin15, self._NEO_PIXEL_COUNT)
        self.motor_stop(self.MOTOR_BOTH)
        self.set_headlight(self.HEADLIGHT_BOTH, self.LED_OFF)
        self.set_underglow_off()

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

    def set_headlight(self, light: int, state: int):
        if light == self.HEADLIGHT_LEFT:
            self._i2c_write([self._LED_LEFT_REG, state])
        elif light == self.HEADLIGHT_RIGHT:
            self._i2c_write([self._LED_RIGHT_REG, state])
        elif light == self.HEADLIGHT_BOTH:
            self._i2c_write([self._LED_LEFT_REG, state, state])

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

    def servo(self, servo_id, angle) -> None:
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180

        if servo_id == self.SERVO_P0:
            microbit.pin0.write_analog(angle)
        elif servo_id == self.SERVO_P1:
            microbit.pin1.write_analog(angle)
        elif servo_id == self.SERVO_P2:
            microbit.pin2.write_analog(angle)

    def line_track(self):
        self._i2c_write([self._LINE_TRACK_REG])
        bits = int.from_bytes(self._i2c_read(1), "big")
        if self._version_minor == 0:
            return (
                ((bits >> 0) & 1) == 1,
                ((bits >> 1) & 1) == 1,
                ((bits >> 2) & 1) == 1,
                ((bits >> 3) & 1) == 1,
                ((bits >> 4) & 1) == 1,
            )
        else:
            return (
                ((bits >> 4) & 1) == 1,
                ((bits >> 3) & 1) == 1,
                ((bits >> 2) & 1) == 1,
                ((bits >> 1) & 1) == 1,
                ((bits >> 0) & 1) == 1,
            )

    def line_track_analog(self):
        self._i2c_write([self._LINE_TRACK_ANALOG_REG])

        # we read 10 bytes, 16 bits per line tracking sensor
        all_sensor_values = self._i2c_read(10)

        return (
            all_sensor_values[0] << 8 | all_sensor_values[1],
            all_sensor_values[2] << 8 | all_sensor_values[3],
            all_sensor_values[4] << 8 | all_sensor_values[5],
            all_sensor_values[6] << 8 | all_sensor_values[7],
            all_sensor_values[8] << 8 | all_sensor_values[9],
        )

    def hsl_to_rgb(self, h, s, l):
        # """
        # Convert HSL (Hue, Saturation, Lightness) to RGB (Red, Green, Blue).
        # :param h: Hue (0 - 360). 0° is red, 120° is green, 240° is blue.
        # :param s: Saturation (0 - 1). 0 is gray, 1 is the full color.
        # :param l: Lightness (0 - 1). 0 is black, 1 is white, and 0.5 is the pure color.
        # :return: Tuple of (R, G, B) where each component is in the range 0 - 255
        # """
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        elif 300 <= h < 360:
            r, g, b = c, 0, x
        else:
            r, g, b = 0, 0, 0

        r = (r + m) * 255
        g = (g + m) * 255
        b = (b + m) * 255

        return int(r), int(g), int(b)

    def set_underglow_light(self, light, rgb_tuple) -> None:
        if light >= 0 and light < self._NEO_PIXEL_COUNT:
            self._neo_pixel[light] = rgb_tuple
            self._neo_pixel.show()

    def set_underglow(self, rgb_tuple) -> None:
        for i in range(self._NEO_PIXEL_COUNT):
            self._neo_pixel[i] = rgb_tuple
        self._neo_pixel.show()

    def set_underglow_off(self) -> None:
        self.set_underglow((0, 0, 0))
