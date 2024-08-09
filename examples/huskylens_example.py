import huskylens
from time import sleep_ms

hl = huskylens.HuskyLens()

hl.set_text("hello", 10, 10)
hl.set_mode(hl.ALGORITHM_COLOR_RECOGNITION)

while True:
    boxes = hl.get_all_boxes()
    for b in boxes:
        print(b)
    sleep_ms(50)
