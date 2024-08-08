# maqueenplus
Python driver/library for the DFRobot Maqueen Plus V1 and V2 robots

# Quick Start
 - Open Microbit's MicroPython environment at https://python.microbit.org/v/3
 - Under Project, select 'Open'
 - Select the driver file for your robot, maqueenplus.py or maqueenplus_v2.py
 - IMPORTANT - At the next dialog, change the option from 'Replace main code ...' to 'Add file ...'
 - Paste the following as your main.py code:

```python
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
```
or
```python
from micropython import const
import maqueenplus_v2
from time import sleep_ms

_MOTOR_SPEED = const(50)

mq = maqueenplus_v2.MaqueenPlusV2()

mq.set_underglow(*mq.COLOR_GREEN)
mq.motor_run(mq.MOTOR_BOTH, mq.MOTOR_DIR_FORWARD, _MOTOR_SPEED)
sleep_ms(1000)
mq.set_underglow(*mq.COLOR_RED)
mq.motor_stop(mq.MOTOR_BOTH)
```
 - Click 'Send to micro:bit'
