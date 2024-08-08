import microbit
import time


class Box:
    def __init__(self, raw_bytes):
        self.centre_x = raw_bytes[1]
        self.centre_y = raw_bytes[2]
        self.width = raw_bytes[3]
        self.height = raw_bytes[4]
        self.id = raw_bytes[5]

    def __str__(self):
        return "Box %d: centre(%d,%d) w,h(%d,%d)" % (
            self.id,
            self.centre_x,
            self.centre_y,
            self.width,
            self.height,
        )


class Arrow:
    def __init__(self, raw_bytes):
        self.start_x = raw_bytes[1]
        self.start_y = raw_bytes[2]
        self.end_x = raw_bytes[3]
        self.end_y = raw_bytes[4]
        self.id = raw_bytes[5]

    def __str__(self):
        return "Arrow %d: start(%d,%d) end(%d,%d)" % (
            self.id,
            self.start_x,
            self.start_y,
            self.end_x,
            self.end_y,
        )


class HuskyLens:

    ALGORITHM_FACE_RECOGNITION = 0
    ALGORITHM_OBJECT_TRACKING = 1
    ALGORITHM_OBJECT_RECOGNITION = 2
    ALGORITHM_LINE_TRACKING = 3
    ALGORITHM_COLOR_RECOGNITION = 4
    ALGORITHM_TAG_RECOGNITION = 5

    _I2C_HUSKYLENS_ADDR = 0x32

    _FRAME_BUFFER_SIZE = 128
    _PROTOCOL_SIZE = 6
    _PROTOCOL_OBJECT_SIZE = 6

    _PROTOCOL_HEADER_0_INDEX = 0
    _PROTOCOL_HEADER_1_INDEX = 1
    _PROTOCOL_ADDRESS_INDEX = 2
    _PROTOCOL_CONTENT_SIZE_INDEX = 3
    _PROTOCOL_COMMAND_INDEX = 4
    _PROTOCOL_CONTENT_INDEX = 5
    _PROTOCOL_SIZE_INDEX = 6

    _PROTOCOL_HEADER_0 = 0x55
    _PROTOCOL_HEADER_1 = 0xAA
    _PROTOCOL_ADDRESS = 0x11

    _COMMAND_REQUEST = 0x20
    _COMMAND_REQUEST_BLOCKS = 0x21
    _COMMAND_REQUEST_ARROWS = 0x22
    _COMMAND_REQUEST_LEARNED = 0x23
    _COMMAND_REQUEST_BLOCKS_LEARNED = 0x24
    _COMMAND_REQUEST_ARROWS_LEARNED = 0x25
    _COMMAND_REQUEST_BY_ID = 0x26
    _COMMAND_REQUEST_BLOCKS_BY_ID = 0x27
    _COMMAND_REQUEST_ARROWS_BY_ID = 0x28
    _COMMAND_RETURN_INFO = 0x29
    _COMMAND_RETURN_BLOCK = 0x2A
    _COMMAND_RETURN_ARROW = 0x2B
    _COMMAND_REQUEST_KNOCK = 0x2C
    _COMMAND_REQUEST_ALGORITHM = 0x2D
    _COMMAND_RETURN_OK = 0x2E
    _COMMAND_REQUEST_LEARN = 0x2F
    _COMMAND_REQUEST_FORGET = 0x30
    _COMMAND_REQUEST_SENSOR = 0x31
    _COMMAND_REQUEST_SET_TEXT = 0x34
    _COMMAND_REQUEST_CLEAR_TEXT = 0x35

    _COMMAND_TIMEOUT_MS = 100

    def __init__(self):
        microbit.display.show(microbit.Image.NO)
        while self._I2C_HUSKYLENS_ADDR not in microbit.i2c.scan():
            if __debug__:
                print("Could not find HuskyLens on I2c")
            microbit.display.show(microbit.Image.NO)
            time.sleep_ms(1000)

        self._m_i = 16
        self._last_cmd_sent = []
        self._send_fail = False
        self._receive_index = 0
        self._receive_buffer = bytearray(self._FRAME_BUFFER_SIZE)
        self._send_buffer = bytearray(self._FRAME_BUFFER_SIZE)
        self._send_index = 0
        self._protocol_buffer = bytearray(self._PROTOCOL_SIZE)
        self._protocol_objects = [
            bytearray(self._PROTOCOL_OBJECT_SIZE) for i in range(10)
        ]
        self._protocol_object_count = 0
        self._content_current = 0
        self._content_end = 0
        self._content_read_end = False

        while not self._knock():
            if __debug__:
                print("Could not communicate with HuskyLens")
            microbit.display.show(microbit.Image.NO)
            time.sleep_ms(1000)

        self.clear_text()
        microbit.display.show(microbit.Image.YES)

    def set_mode(self, algorithm_mode):
        self._write_algorithm(algorithm_mode, self._COMMAND_REQUEST_ALGORITHM)
        result = self._wait(self._COMMAND_RETURN_OK)
        return result

    def set_text(self, text, x=0, y=0):
        buffer = self._protocol_write_begin(self._COMMAND_REQUEST_SET_TEXT)
        text_utf8 = text.encode("utf-8")
        self._send_buffer[self._send_index] = len(text_utf8)
        self._send_index += 1

        if x > 255:
            self._send_buffer[self._send_index] = 0xFF
            self._send_buffer[self._send_index + 1] = x & 0xFF
        else:
            self._send_buffer[self._send_index] = 0
            self._send_buffer[self._send_index + 1] = x
        self._send_index += 2

        self._send_buffer[self._send_index] = y
        self._send_index += 1

        for b in text_utf8:
            self._send_buffer[self._send_index] = b
            self._send_index += 1

        length = self._protocol_write_end()
        self._protocol_write(buffer[:length])

        # self._wait(self._COMMAND_RETURN_OK)

    def clear_text(self):
        self._write_algorithm(0x45, self._COMMAND_REQUEST_CLEAR_TEXT)

    def get_all_boxes(self):
        ret = []
        if not self._request():
            return ret
        for i in range(self._protocol_object_count):
            if self._protocol_objects[i][0] == self._COMMAND_RETURN_BLOCK:
                ret.append(Box(self._protocol_objects[i]))
        return ret

    def get_boxes_by_id(self, id):
        ret = []
        if not self._request():
            return ret
        for i in range(self._protocol_object_count):
            if (
                self._protocol_objects[i][0] == self._COMMAND_RETURN_BLOCK
                and self._protocol_objects[i][5] == id
            ):
                ret.append(Box(self._protocol_objects[i]))
        return ret

    def get_all_arrows(self):
        ret = []
        if not self._request():
            return ret
        for i in range(self._protocol_object_count):
            if self._protocol_objects[i][0] == self._COMMAND_RETURN_ARROW:
                ret.append(Arrow(self._protocol_objects[i]))
        return ret

    def _i2c_write(self, buf):
        print("I2C Write: ")
        print(" ".join("0x%02X" % (byte) for byte in buf))
        microbit.i2c.write(self._I2C_HUSKYLENS_ADDR, bytes(buf))

    def _i2c_read(self, count):
        buf = microbit.i2c.read(self._I2C_HUSKYLENS_ADDR, count)
        print("I2C Read: ")
        print(" ".join("0x%02X" % (byte) for byte in buf))
        return buf

    def _write_algorithm(self, algorithm_mode, command=0):
        self._protocol_write_one_int16(algorithm_mode, command)

    def _protocol_write_begin(self, command=0):
        self._send_fail = False
        self._send_buffer[self._PROTOCOL_HEADER_0_INDEX] = self._PROTOCOL_HEADER_0
        self._send_buffer[self._PROTOCOL_HEADER_1_INDEX] = self._PROTOCOL_HEADER_1
        self._send_buffer[self._PROTOCOL_ADDRESS_INDEX] = self._PROTOCOL_ADDRESS
        self._send_buffer[self._PROTOCOL_COMMAND_INDEX] = command
        self._send_index = self._PROTOCOL_CONTENT_INDEX
        return self._send_buffer

    def _protocol_write_one_int16(self, mode, command):
        buffer = self._protocol_write_begin(command)
        self._protocol_write_int16(mode)
        length = self._protocol_write_end()
        self._protocol_write(buffer[:length])

    def _protocol_write_int16(self, content=0):
        if self._send_index + 2 >= self._FRAME_BUFFER_SIZE:
            self._send_fail = True
            return

        self._send_buffer[self._send_index] = content & 0xFF
        self._send_buffer[self._send_index + 1] = (content >> 8) & 0xFF
        self._send_index += 2

    def _protocol_write_end(self):
        if self._send_fail:
            return 0

        if self._send_index + 1 >= self._FRAME_BUFFER_SIZE:
            return 0

        self._send_buffer[self._PROTOCOL_CONTENT_SIZE_INDEX] = (
            self._send_index - self._PROTOCOL_CONTENT_INDEX
        )

        hk_sum = 0
        for i in range(self._send_index):
            hk_sum += self._send_buffer[i]
        hk_sum = hk_sum & 0xFF

        self._send_buffer[self._send_index] = hk_sum
        self._send_index += 1

        return self._send_index

    def _protocol_write(self, buffer):
        self._i2c_write(buffer)
        time.sleep_ms(50)

    def _protocol_write_command(self, command):
        self._protocol_buffer[0] = command
        buffer = self._protocol_write_begin(command)
        length = self._protocol_write_end()
        self._protocol_write(buffer[:length])

    def _knock(self):
        for i in range(5):
            self._protocol_write_command(self._COMMAND_REQUEST_KNOCK)
            if self._wait(self._COMMAND_RETURN_OK):
                return True
        return False

    def _request(self):
        self._protocol_write_command(self._COMMAND_REQUEST)
        return self._process_return()

    def _process_return(self):
        print("Process Return")
        if not self._wait(self._COMMAND_RETURN_INFO):
            self._protocol_object_count = 0
            return False
        print("Got _COMMAND_RETURN_INFO")
        self._protocol_read_five_int16(self._COMMAND_RETURN_INFO)
        self._protocol_object_count = self._protocol_buffer[1]
        print("Got %d things to read back" % (self._protocol_object_count))
        for i in range(self._protocol_object_count):
            if not self._wait():
                return False
            if self._protocol_read_five_int161(i, self._COMMAND_RETURN_BLOCK):
                print("Got a block")
                continue
            elif self._protocol_read_five_int161(i, self._COMMAND_RETURN_ARROW):
                print("Got an arrow")
                continue
            else:
                return False
        return True

    def _validate_checksum(self):

        stack_sum_index = (
            self._receive_buffer[self._PROTOCOL_CONTENT_SIZE_INDEX]
            + self._PROTOCOL_CONTENT_INDEX
        )
        hk_sum = 0
        for i in range(stack_sum_index):
            hk_sum += self._receive_buffer[i]
        hk_sum = hk_sum & 0xFF

        return hk_sum == self._receive_buffer[stack_sum_index]

    def _protocol_receive(self, data):
        if self._receive_index == self._PROTOCOL_HEADER_0_INDEX:
            if data != self._PROTOCOL_HEADER_0:
                self._receive_index = 0
                return False
            self._receive_buffer[self._PROTOCOL_HEADER_0_INDEX] = (
                self._PROTOCOL_HEADER_0
            )
        elif self._receive_index == self._PROTOCOL_HEADER_1_INDEX:
            if data != self._PROTOCOL_HEADER_1:
                self._receive_index = 0
                return False
            self._receive_buffer[self._PROTOCOL_HEADER_1_INDEX] = (
                self._PROTOCOL_HEADER_1
            )
        elif self._receive_index == self._PROTOCOL_ADDRESS_INDEX:
            self._receive_buffer[self._PROTOCOL_ADDRESS_INDEX] = data
        elif self._receive_index == self._PROTOCOL_CONTENT_SIZE_INDEX:
            if data >= (self._FRAME_BUFFER_SIZE - self._PROTOCOL_SIZE):
                self._receive_index = 0
                return False
            self._receive_buffer[self._PROTOCOL_CONTENT_SIZE_INDEX] = data
        else:
            self._receive_buffer[self._receive_index] = data

            if (
                self._receive_index
                == self._receive_buffer[self._PROTOCOL_CONTENT_SIZE_INDEX]
                + self._PROTOCOL_CONTENT_INDEX
            ):
                self._content_end = self._receive_index
                self._receive_index = 0
                return self._validate_checksum()
        self._receive_index += 1
        return False

    def _protocol_available(self):
        print("Protocol Available, self._m_i = %d" % (self._m_i))
        buf = bytearray(16)
        if self._m_i == 16:
            buf = self._i2c_read(16)
            self._m_i = 0

        for i in range(self._m_i, 16):
            if self._protocol_receive(buf[i]):
                self._m_i += 1
                return True
            self._m_i += 1
        return False

    def _protocol_read_begin(self, command=0):
        if command == self._receive_buffer[self._PROTOCOL_COMMAND_INDEX]:
            self._content_current = self._PROTOCOL_CONTENT_INDEX
            self._content_read_end = False
            self._receive_fail = False
            return True
        return False

    def _protocol_read_five_int16(self, command=0):
        print("Reading 5 int16")
        if not self._protocol_read_begin(command):
            return False

        self._protocol_buffer[0] = command
        self._protocol_buffer[1] = self._protocol_read_int16()
        self._protocol_buffer[2] = self._protocol_read_int16()
        self._protocol_buffer[3] = self._protocol_read_int16()
        self._protocol_buffer[4] = self._protocol_read_int16()
        self._protocol_buffer[5] = self._protocol_read_int16()
        return self._protocol_read_end()

    def _protocol_read_five_int161(self, i, command=0):
        print("Reading 5 int16 into slot %d" % (i))
        if not self._protocol_read_begin(command):
            return False

        self._protocol_objects[i][0] = command
        self._protocol_objects[i][1] = self._protocol_read_int16()
        self._protocol_objects[i][2] = self._protocol_read_int16()
        self._protocol_objects[i][3] = self._protocol_read_int16()
        self._protocol_objects[i][4] = self._protocol_read_int16()
        self._protocol_objects[i][5] = self._protocol_read_int16()
        return self._protocol_read_end()

    def _protocol_read_int16(self):
        if (self._content_current >= self._content_end) or self._content_read_end:
            self._receive_fail = True
            return 0
        result = (
            self._receive_buffer[self._content_current + 1] << 8
            | self._receive_buffer[self._content_current]
        )
        self._content_current += 2
        print("Read int16: %04x" % (result))
        return result

    def _protocol_read_end(self):
        if self._receive_fail:
            self._receive_fail = False
            return False
        return self._content_current == self._content_end

    def _wait(self, command=0):
        print("Wait, command=%d" % (command))
        start_time = time.ticks_ms()
        while (time.ticks_ms() - start_time) < self._COMMAND_TIMEOUT_MS:
            if self._protocol_available():
                if command != 0:
                    if self._protocol_read_begin(command):
                        return True
                else:
                    return True
        return False
