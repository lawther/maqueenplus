_B=True
_A=False
import microbit,time
class Box:
	def __init__(A,raw_array):B=raw_array;A.centre_x=B[1];A.centre_y=B[2];A.width=B[3];A.height=B[4];A.id=B[5]
	def __str__(A):return'Box %d: centre(%d,%d) w,h(%d,%d)'%(A.id,A.centre_x,A.centre_y,A.width,A.height)
class Arrow:
	def __init__(A,raw_array):B=raw_array;A.start_x=B[1];A.start_y=B[2];A.end_x=B[3];A.end_y=B[4];A.id=B[5]
	def __str__(A):return'Arrow %d: start(%d,%d) end(%d,%d)'%(A.id,A.start_x,A.start_y,A.end_x,A.end_y)
class HuskyLens:
	ALGORITHM_FACE_RECOGNITION=0;ALGORITHM_OBJECT_TRACKING=1;ALGORITHM_OBJECT_RECOGNITION=2;ALGORITHM_LINE_TRACKING=3;ALGORITHM_COLOR_RECOGNITION=4;ALGORITHM_TAG_RECOGNITION=5
	def __init__(A):
		microbit.display.show(microbit.Image.NO)
		while 50 not in microbit.i2c.scan():microbit.display.show(microbit.Image.NO);time.sleep_ms(1000)
		A._z=16;A._y=[];A._H=_A;A._F=0;A._D=bytearray(128);A._G=bytearray(128);A._I=0;A._A=[0 for A in range(6)];A._C=[[0 for A in range(6)]for A in range(10)];A._B=0;A._v=0;A._w=0;A._x=_A
		while not A._c():microbit.display.show(microbit.Image.NO);time.sleep_ms(1000)
		A.clear_text();microbit.display.show(microbit.Image.YES)
	def set_mode(A,algorithm_mode):A._u(algorithm_mode,45);B=A._t(46);return B
	def set_text(A,text,x=0,y=0):
		C=A._m(52);B=text.encode('utf-8');A._G[A._I]=len(B);A._I+=1
		if x>255:A._G[A._I]=255;A._G[A._I+1]=x&255
		else:A._G[A._I]=0;A._G[A._I+1]=x
		A._I+=2;A._G[A._I]=y;A._I+=1
		for D in B:A._G[A._I]=D;A._I+=1
		E=A._o();A._l(C[:E])
	def clear_text(A):A._u(69,53)
	def get_all_boxes(A):
		B=[]
		if not A._r():return B
		for C in range(A._B):
			if A._C[C][0]==42:B.append(Box(A._C[C]))
		return B
	def get_boxes_by_id(A,id):
		B=[]
		if not A._r():return B
		for C in range(A._B):
			if A._C[C][0]==42 and A._C[C][5]==id:B.append(Box(A._C[C]))
		return B
	def get_all_arrows(A):
		B=[]
		if not A._r():return B
		for C in range(A._B):
			if A._C[C][0]==43:B.append(Arrow(A._C[C]))
		return B
	def _b(A,buf):microbit.i2c.write(50,bytes(buf))
	def _a(B,count):A=microbit.i2c.read(50,count);return A
	def _u(A,algorithm_mode,command=0):A._q(algorithm_mode,command)
	def _m(A,command=0):A._H=_A;A._G[0]=85;A._G[1]=170;A._G[2]=17;A._G[4]=command;A._I=5;return A._G
	def _q(A,mode,command):B=A._m(command);A._p(mode);C=A._o();A._l(B[:C])
	def _p(A,content=0):
		B=content
		if A._I+2>=128:A._H=_B;return
		A._G[A._I]=B&255;A._G[A._I+1]=B>>8&255;A._I+=2
	def _o(A):
		if A._H:return 0
		if A._I+1>=128:return 0
		A._G[3]=A._I-5;B=0
		for C in range(A._I):B+=A._G[C]
		B=B&255;A._G[A._I]=B;A._I+=1;return A._I
	def _l(A,buffer):A._b(buffer);time.sleep_ms(50)
	def _n(A,command):B=command;A._A[0]=B;C=A._m(B);D=A._o();A._l(C[:D])
	def _c(A):
		for B in range(5):
			A._n(44)
			if A._t(46):return _B
		return _A
	def _r(A):A._n(32);return A._d()
	def _d(A):
		if not A._t(41):A._B=0;return _A
		A._h(41);A._B=A._A[1]
		for B in range(A._B):
			if not A._t():return _A
			if A._i(B,42):continue
			elif A._i(B,43):continue
			else:return _A
		return _B
	def _s(B):
		C=B._D[3]+5;A=0
		for D in range(C):A+=B._D[D]
		A=A&255;return A==B._D[C]
	def _k(A,data):
		B=data
		if A._F==0:
			if B!=85:A._F=0;return _A
			A._D[0]=85
		elif A._F==1:
			if B!=170:A._F=0;return _A
			A._D[1]=170
		elif A._F==2:A._D[2]=B
		elif A._F==3:
			if B>=128-6:A._F=0;return _A
			A._D[3]=B
		else:
			A._D[A._F]=B
			if A._F==A._D[3]+5:A._w=A._F;A._F=0;return A._s()
		A._F+=1;return _A
	def _e(A):
		B=bytearray(16)
		if A._z==16:B=A._a(16);A._z=0
		for C in range(A._z,16):
			if A._k(B[C]):A._z+=1;return _B
			A._z+=1
		return _A
	def _f(A,command=0):
		if command==A._D[4]:A._v=5;A._x=_A;A._E=_A;return _B
		return _A
	def _h(A,command=0):
		B=command
		if not A._f(B):return _A
		A._A[0]=B;A._A[1]=A._j();A._A[2]=A._j();A._A[3]=A._j();A._A[4]=A._j();A._A[5]=A._j();return A._g()
	def _i(A,i,command=0):
		B=command
		if not A._f(B):return _A
		A._C[i][0]=B;A._C[i][1]=A._j();A._C[i][2]=A._j();A._C[i][3]=A._j();A._C[i][4]=A._j();A._C[i][5]=A._j();return A._g()
	def _j(A):
		if A._v>=A._w or A._x:A._E=_B;return 0
		B=A._D[A._v+1]<<8|A._D[A._v];A._v+=2;return B
	def _g(A):
		if A._E:A._E=_A;return _A
		return A._v==A._w
	def _t(A,command=0):
		B=command;C=time.ticks_ms()
		while time.ticks_ms()-C<100:
			if A._e():
				if B!=0:
					if A._f(B):return _B
				else:return _B
		return _A