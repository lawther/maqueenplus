# maqueenplus
Python driver/library for the DFRobot Maqueen Plus V1 and V2 robots. And also the HuskyLens camera.

# Quick Start
 - Open Microbit's MicroPython environment at https://python.microbit.org/v/3
 - Under Project, select 'Open'
 - Select the driver file for your robot, maqueenplus.py or maqueenplus_v2.py
 - IMPORTANT - At the next dialog, change the option from 'Replace main code ...' to 'Add file ...'
 - Open a file from the examples directory
 - This time, leave the option of 'Replace main code ...'
 - Click 'Send to micro:bit'

 # Minified versions
 The Microbit is very limited on storage and RAM. A decent sized Python program can cause problems. It can could be too large to fit on the device's Micropython filesystem. Particularly on the Microbit V1 you can cause the Micropython compiler to run out of RAM.

 If you see errors like this, then you will need to use the versions in the 'minified' directory. Simply substitute the minified file for the original file.

 The minified files were produced with https://github.com/dflook/python-minifier. They are functionally identical, except they have had any code wrapped in `__debug__` stripped out.
