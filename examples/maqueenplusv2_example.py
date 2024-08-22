from micropython import const
import maqueenplusv2
from time import sleep_ms

_MOTOR_SPEED = const(50)

mq = maqueenplusv2.MaqueenPlusV2()

mq.set_underglow_all(mq.COLOR_GREEN)
mq.motor_run(mq.MOTOR_BOTH, mq.MOTOR_DIR_FORWARD, _MOTOR_SPEED)
sleep_ms(1000)
mq.set_underglow_all(mq.COLOR_RED)
mq.motor_stop(mq.MOTOR_BOTH)
