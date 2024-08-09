import microbit
from micropython import const
import maqueenplus
from time import sleep_ms

_MOTOR_SPEED = const(50)

# Change the pin numbers for however you've plugged in your ultrasonic sensor
mq = maqueenplus.MaqueenPlus(microbit.pin1, microbit.pin2)

mq.set_rgb_light(mq.RGB_BOTH, mq.COLOR_GREEN)
mq.motor_run(mq.MOTOR_BOTH, mq.MOTOR_DIR_FORWARD, _MOTOR_SPEED)
sleep_ms(1000)
mq.set_rgb_light(mq.RGB_BOTH, mq.COLOR_RED)
mq.motor_stop(mq.MOTOR_BOTH)
