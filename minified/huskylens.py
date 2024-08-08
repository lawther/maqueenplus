_C='0x%02X'
_B=True
_A=False
import microbit,time
class Box:
	def __init__(A,raw_bytes):B=raw_bytes;A.centre_x=B[1];A.centre_y=B[2];A.width=B[3];A.height=B[4];A.id=B[5]
	def __str__(A):return'Box %d: centre(%d,%d) w,h(%d,%d)'%(A.id,A.centre_x,A.centre_y,A.width,A.height)
class Arrow:
	def __init__(A,raw_bytes):B=raw_bytes;A.start_x=B[1];A.start_y=B[2];A.end_x=B[3];A.end_y=B[4];A.id=B[5]
	def __str__(A):return'Arrow %d: start(%d,%d) end(%d,%d)'%(A.id,A.start_x,A.start_y,A.end_x,A.end_y)
class HuskyLens:
	ALGORITHM_FACE_RECOGNITION=0;ALGORITHM_OBJECT_TRACKING=1;ALGORITHM_OBJECT_RECOGNITION=2;ALGORITHM_LINE_TRACKING=3;ALGORITHM_COLOR_RECOGNITION=4;ALGORITHM_TAG_RECOGNITION=5;_I2C_HUSKYLENS_ADDR=50;_FRAME_BUFFER_SIZE=128;_PROTOCOL_SIZE=6;_PROTOCOL_OBJECT_SIZE=6;_PROTOCOL_HEADER_0_INDEX=0;_PROTOCOL_HEADER_1_INDEX=1;_PROTOCOL_ADDRESS_INDEX=2;_PROTOCOL_CONTENT_SIZE_INDEX=3;_PROTOCOL_COMMAND_INDEX=4;_PROTOCOL_CONTENT_INDEX=5;_PROTOCOL_SIZE_INDEX=6;_PROTOCOL_HEADER_0=85;_PROTOCOL_HEADER_1=170;_PROTOCOL_ADDRESS=17;_COMMAND_REQUEST=32;_COMMAND_REQUEST_BLOCKS=33;_COMMAND_REQUEST_ARROWS=34;_COMMAND_REQUEST_LEARNED=35;_COMMAND_REQUEST_BLOCKS_LEARNED=36;_COMMAND_REQUEST_ARROWS_LEARNED=37;_COMMAND_REQUEST_BY_ID=38;_COMMAND_REQUEST_BLOCKS_BY_ID=39;_COMMAND_REQUEST_ARROWS_BY_ID=40;_COMMAND_RETURN_INFO=41;_COMMAND_RETURN_BLOCK=42;_COMMAND_RETURN_ARROW=43;_COMMAND_REQUEST_KNOCK=44;_COMMAND_REQUEST_ALGORITHM=45;_COMMAND_RETURN_OK=46;_COMMAND_REQUEST_LEARN=47;_COMMAND_REQUEST_FORGET=48;_COMMAND_REQUEST_SENSOR=49;_COMMAND_REQUEST_SET_TEXT=52;_COMMAND_REQUEST_CLEAR_TEXT=53;_COMMAND_TIMEOUT_MS=100
	def __init__(A):
		microbit.display.show(microbit.Image.NO)
		while A._I2C_HUSKYLENS_ADDR not in microbit.i2c.scan():microbit.display.show(microbit.Image.NO);time.sleep_ms(1000)
		A._m_i=16;A._last_cmd_sent=[];A._send_fail=_A;A._receive_index=0;A._receive_buffer=bytearray(A._FRAME_BUFFER_SIZE);A._send_buffer=bytearray(A._FRAME_BUFFER_SIZE);A._send_index=0;A._protocol_buffer=bytearray(A._PROTOCOL_SIZE);A._protocol_objects=[bytearray(A._PROTOCOL_OBJECT_SIZE)for B in range(10)];A._protocol_object_count=0;A._content_current=0;A._content_end=0;A._content_read_end=_A
		while not A._knock():microbit.display.show(microbit.Image.NO);time.sleep_ms(1000)
		A.clear_text();microbit.display.show(microbit.Image.YES)
	def set_mode(A,algorithm_mode):A._write_algorithm(algorithm_mode,A._COMMAND_REQUEST_ALGORITHM);B=A._wait(A._COMMAND_RETURN_OK);return B
	def set_text(A,text,x=0,y=0):
		C=A._protocol_write_begin(A._COMMAND_REQUEST_SET_TEXT);B=text.encode('utf-8');A._send_buffer[A._send_index]=len(B);A._send_index+=1
		if x>255:A._send_buffer[A._send_index]=255;A._send_buffer[A._send_index+1]=x&255
		else:A._send_buffer[A._send_index]=0;A._send_buffer[A._send_index+1]=x
		A._send_index+=2;A._send_buffer[A._send_index]=y;A._send_index+=1
		for D in B:A._send_buffer[A._send_index]=D;A._send_index+=1
		E=A._protocol_write_end();A._protocol_write(C[:E])
	def clear_text(A):A._write_algorithm(69,A._COMMAND_REQUEST_CLEAR_TEXT)
	def get_all_boxes(A):
		B=[]
		if not A._request():return B
		for C in range(A._protocol_object_count):
			if A._protocol_objects[C][0]==A._COMMAND_RETURN_BLOCK:B.append(Box(A._protocol_objects[C]))
		return B
	def get_boxes_by_id(A,id):
		B=[]
		if not A._request():return B
		for C in range(A._protocol_object_count):
			if A._protocol_objects[C][0]==A._COMMAND_RETURN_BLOCK and A._protocol_objects[C][5]==id:B.append(Box(A._protocol_objects[C]))
		return B
	def get_all_arrows(A):
		B=[]
		if not A._request():return B
		for C in range(A._protocol_object_count):
			if A._protocol_objects[C][0]==A._COMMAND_RETURN_ARROW:B.append(Arrow(A._protocol_objects[C]))
		return B
	def _i2c_write(A,buf):print('I2C Write: ');print(' '.join(_C%A for A in buf));microbit.i2c.write(A._I2C_HUSKYLENS_ADDR,bytes(buf))
	def _i2c_read(B,count):A=microbit.i2c.read(B._I2C_HUSKYLENS_ADDR,count);print('I2C Read: ');print(' '.join(_C%A for A in A));return A
	def _write_algorithm(A,algorithm_mode,command=0):A._protocol_write_one_int16(algorithm_mode,command)
	def _protocol_write_begin(A,command=0):A._send_fail=_A;A._send_buffer[A._PROTOCOL_HEADER_0_INDEX]=A._PROTOCOL_HEADER_0;A._send_buffer[A._PROTOCOL_HEADER_1_INDEX]=A._PROTOCOL_HEADER_1;A._send_buffer[A._PROTOCOL_ADDRESS_INDEX]=A._PROTOCOL_ADDRESS;A._send_buffer[A._PROTOCOL_COMMAND_INDEX]=command;A._send_index=A._PROTOCOL_CONTENT_INDEX;return A._send_buffer
	def _protocol_write_one_int16(A,mode,command):B=A._protocol_write_begin(command);A._protocol_write_int16(mode);C=A._protocol_write_end();A._protocol_write(B[:C])
	def _protocol_write_int16(A,content=0):
		B=content
		if A._send_index+2>=A._FRAME_BUFFER_SIZE:A._send_fail=_B;return
		A._send_buffer[A._send_index]=B&255;A._send_buffer[A._send_index+1]=B>>8&255;A._send_index+=2
	def _protocol_write_end(A):
		if A._send_fail:return 0
		if A._send_index+1>=A._FRAME_BUFFER_SIZE:return 0
		A._send_buffer[A._PROTOCOL_CONTENT_SIZE_INDEX]=A._send_index-A._PROTOCOL_CONTENT_INDEX;B=0
		for C in range(A._send_index):B+=A._send_buffer[C]
		B=B&255;A._send_buffer[A._send_index]=B;A._send_index+=1;return A._send_index
	def _protocol_write(A,buffer):A._i2c_write(buffer);time.sleep_ms(50)
	def _protocol_write_command(A,command):B=command;A._protocol_buffer[0]=B;C=A._protocol_write_begin(B);D=A._protocol_write_end();A._protocol_write(C[:D])
	def _knock(A):
		for B in range(5):
			A._protocol_write_command(A._COMMAND_REQUEST_KNOCK)
			if A._wait(A._COMMAND_RETURN_OK):return _B
		return _A
	def _request(A):A._protocol_write_command(A._COMMAND_REQUEST);return A._process_return()
	def _process_return(A):
		print('Process Return')
		if not A._wait(A._COMMAND_RETURN_INFO):A._protocol_object_count=0;return _A
		print('Got _COMMAND_RETURN_INFO');A._protocol_read_five_int16(A._COMMAND_RETURN_INFO);A._protocol_object_count=A._protocol_buffer[1];print('Got %d things to read back'%A._protocol_object_count)
		for B in range(A._protocol_object_count):
			if not A._wait():return _A
			if A._protocol_read_five_int161(B,A._COMMAND_RETURN_BLOCK):print('Got a block');continue
			elif A._protocol_read_five_int161(B,A._COMMAND_RETURN_ARROW):print('Got an arrow');continue
			else:return _A
		return _B
	def _validate_checksum(A):
		C=A._receive_buffer[A._PROTOCOL_CONTENT_SIZE_INDEX]+A._PROTOCOL_CONTENT_INDEX;B=0
		for D in range(C):B+=A._receive_buffer[D]
		B=B&255;return B==A._receive_buffer[C]
	def _protocol_receive(A,data):
		B=data
		if A._receive_index==A._PROTOCOL_HEADER_0_INDEX:
			if B!=A._PROTOCOL_HEADER_0:A._receive_index=0;return _A
			A._receive_buffer[A._PROTOCOL_HEADER_0_INDEX]=A._PROTOCOL_HEADER_0
		elif A._receive_index==A._PROTOCOL_HEADER_1_INDEX:
			if B!=A._PROTOCOL_HEADER_1:A._receive_index=0;return _A
			A._receive_buffer[A._PROTOCOL_HEADER_1_INDEX]=A._PROTOCOL_HEADER_1
		elif A._receive_index==A._PROTOCOL_ADDRESS_INDEX:A._receive_buffer[A._PROTOCOL_ADDRESS_INDEX]=B
		elif A._receive_index==A._PROTOCOL_CONTENT_SIZE_INDEX:
			if B>=A._FRAME_BUFFER_SIZE-A._PROTOCOL_SIZE:A._receive_index=0;return _A
			A._receive_buffer[A._PROTOCOL_CONTENT_SIZE_INDEX]=B
		else:
			A._receive_buffer[A._receive_index]=B
			if A._receive_index==A._receive_buffer[A._PROTOCOL_CONTENT_SIZE_INDEX]+A._PROTOCOL_CONTENT_INDEX:A._content_end=A._receive_index;A._receive_index=0;return A._validate_checksum()
		A._receive_index+=1;return _A
	def _protocol_available(A):
		print('Protocol Available, self._m_i = %d'%A._m_i);B=bytearray(16)
		if A._m_i==16:B=A._i2c_read(16);A._m_i=0
		for C in range(A._m_i,16):
			if A._protocol_receive(B[C]):A._m_i+=1;return _B
			A._m_i+=1
		return _A
	def _protocol_read_begin(A,command=0):
		if command==A._receive_buffer[A._PROTOCOL_COMMAND_INDEX]:A._content_current=A._PROTOCOL_CONTENT_INDEX;A._content_read_end=_A;A._receive_fail=_A;return _B
		return _A
	def _protocol_read_five_int16(A,command=0):
		B=command;print('Reading 5 int16')
		if not A._protocol_read_begin(B):return _A
		A._protocol_buffer[0]=B;A._protocol_buffer[1]=A._protocol_read_int16();A._protocol_buffer[2]=A._protocol_read_int16();A._protocol_buffer[3]=A._protocol_read_int16();A._protocol_buffer[4]=A._protocol_read_int16();A._protocol_buffer[5]=A._protocol_read_int16();return A._protocol_read_end()
	def _protocol_read_five_int161(A,i,command=0):
		B=command;print('Reading 5 int16 into slot %d'%i)
		if not A._protocol_read_begin(B):return _A
		A._protocol_objects[i][0]=B;A._protocol_objects[i][1]=A._protocol_read_int16();A._protocol_objects[i][2]=A._protocol_read_int16();A._protocol_objects[i][3]=A._protocol_read_int16();A._protocol_objects[i][4]=A._protocol_read_int16();A._protocol_objects[i][5]=A._protocol_read_int16();return A._protocol_read_end()
	def _protocol_read_int16(A):
		if A._content_current>=A._content_end or A._content_read_end:A._receive_fail=_B;return 0
		B=A._receive_buffer[A._content_current+1]<<8|A._receive_buffer[A._content_current];A._content_current+=2;print('Read int16: %04x'%B);return B
	def _protocol_read_end(A):
		if A._receive_fail:A._receive_fail=_A;return _A
		return A._content_current==A._content_end
	def _wait(A,command=0):
		B=command;print('Wait, command=%d'%B);C=time.ticks_ms()
		while time.ticks_ms()-C<A._COMMAND_TIMEOUT_MS:
			if A._protocol_available():
				if B!=0:
					if A._protocol_read_begin(B):return _B
				else:return _B
		return _A