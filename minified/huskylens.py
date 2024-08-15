_A0=False
import microbit,time
class Box:
	def __init__(A,raw_array):B=raw_array;A.centre_x=B[1];A.centre_y=B[2];A.width=B[3];A.height=B[4];A.id=B[5]
	def __str__(A):return'Box %d: centre(%d,%d) w,h(%d,%d)'%(A.id,A.centre_x,A.centre_y,A.width,A.height)
class Arrow:
	def __init__(A,raw_array):B=raw_array;A.start_x=B[1];A.start_y=B[2];A.end_x=B[3];A.end_y=B[4];A.id=B[5]
	def __str__(A):return'Arrow %d: start(%d,%d) end(%d,%d)'%(A.id,A.start_x,A.start_y,A.end_x,A.end_y)
class HuskyLens:
	ALGORITHM_FACE_RECOGNITION=0;ALGORITHM_OBJECT_TRACKING=1;ALGORITHM_OBJECT_RECOGNITION=2;ALGORITHM_LINE_TRACKING=3;ALGORITHM_COLOR_RECOGNITION=4;ALGORITHM_TAG_RECOGNITION=5;_R=50;_Q=128;_4=6;_3=6;_Z=0;_2=1;_U=2;_X=3;_V=4;_W=5;_5=6;_Y=85;_1=170;_T=17;_v=32;_A=33;_x=34;_I=35;_C=36;_z=37;_D=38;_B=39;_y=40;_N=41;_M=42;_L=43;_G=44;_w=45;_O=46;_H=47;_F=48;_J=49;_K=52;_E=53;_P=100;_S=10
	def __init__(A):
		microbit.display.show(microbit.Image.NO)
		while A._R not in microbit.i2c.scan():microbit.display.show(microbit.Image.NO);time.sleep_ms(1000)
		A._0=16;A._9=[];A._ah=_A0;A._af=0;A._ad=bytearray(A._Q);A._ag=bytearray(A._Q);A._ai=0;A._aa=[0 for A in range(A._4)];A._ac=[[0 for A in range(A._3)]for B in range(A._S)];A._ab=0;A._6=0;A._7=0;A._8=_A0
		while not A._c():microbit.display.show(microbit.Image.NO);time.sleep_ms(1000)
		A.clear_text();microbit.display.show(microbit.Image.YES)
	def set_mode(A,algorithm_mode):A._u(algorithm_mode,A._w);B=A._t(A._O);return B
	def set_text(A,text,x=0,y=0):
		C=A._m(A._K);B=text.encode('utf-8');A._ag[A._ai]=len(B);A._ai+=1
		if x>255:A._ag[A._ai]=255;A._ag[A._ai+1]=x&255
		else:A._ag[A._ai]=0;A._ag[A._ai+1]=x
		A._ai+=2;A._ag[A._ai]=y;A._ai+=1
		for D in B:A._ag[A._ai]=D;A._ai+=1
		E=A._o();A._l(C[:E])
	def clear_text(A):A._u(69,A._E)
	def get_all_boxes(A):
		B=[]
		if not A._r():return B
		for C in range(A._ab):
			if A._ac[C][0]==A._M:B.append(Box(A._ac[C]))
		return B
	def get_boxes_by_id(A,id):
		B=[]
		if not A._r():return B
		for C in range(A._ab):
			if A._ac[C][0]==A._M and A._ac[C][5]==id:B.append(Box(A._ac[C]))
		return B
	def get_all_arrows(A):
		B=[]
		if not A._r():return B
		for C in range(A._ab):
			if A._ac[C][0]==A._L:B.append(Arrow(A._ac[C]))
		return B
	def _b(A,buf):microbit.i2c.write(A._R,bytes(buf))
	def _a(A,count):B=microbit.i2c.read(A._R,count);return B
	def _u(A,algorithm_mode,command=0):A._q(algorithm_mode,command)
	def _m(A,command=0):A._ah=_A0;A._ag[A._Z]=A._Y;A._ag[A._2]=A._1;A._ag[A._U]=A._T;A._ag[A._V]=command;A._ai=A._W;return A._ag
	def _q(A,mode,command):B=A._m(command);A._p(mode);C=A._o();A._l(B[:C])
	def _p(A,content=0):
		B=content
		if A._ai+2>=A._Q:A._ah=True;return
		A._ag[A._ai]=B&255;A._ag[A._ai+1]=B>>8&255;A._ai+=2
	def _o(A):
		if A._ah:return 0
		if A._ai+1>=A._Q:return 0
		A._ag[A._X]=A._ai-A._W;B=0
		for C in range(A._ai):B+=A._ag[C]
		B=B&255;A._ag[A._ai]=B;A._ai+=1;return A._ai
	def _l(A,buffer):A._b(buffer);time.sleep_ms(50)
	def _n(A,command):B=command;A._aa[0]=B;C=A._m(B);D=A._o();A._l(C[:D])
	def _c(A):
		for B in range(5):
			A._n(A._G)
			if A._t(A._O):return True
		return _A0
	def _r(A):A._n(A._v);return A._d()
	def _d(A):
		if not A._t(A._N):A._ab=0;return _A0
		A._h(A._N);A._ab=A._aa[1]
		for B in range(A._ab):
			if not A._t():return _A0
			if A._i(B,A._M):continue
			elif A._i(B,A._L):continue
			else:return _A0
		return True
	def _s(A):
		C=A._ad[A._X]+A._W;B=0
		for D in range(C):B+=A._ad[D]
		B=B&255;return B==A._ad[C]
	def _k(A,data):
		B=data
		if A._af==A._Z:
			if B!=A._Y:A._af=0;return _A0
			A._ad[A._Z]=A._Y
		elif A._af==A._2:
			if B!=A._1:A._af=0;return _A0
			A._ad[A._2]=A._1
		elif A._af==A._U:A._ad[A._U]=B
		elif A._af==A._X:
			if B>=A._Q-A._4:A._af=0;return _A0
			A._ad[A._X]=B
		else:
			A._ad[A._af]=B
			if A._af==A._ad[A._X]+A._W:A._7=A._af;A._af=0;return A._s()
		A._af+=1;return _A0
	def _e(A):
		B=bytearray(16)
		if A._0==16:B=A._a(16);A._0=0
		for C in range(A._0,16):
			if A._k(B[C]):A._0+=1;return True
			A._0+=1
		return _A0
	def _f(A,command=0):
		if command==A._ad[A._V]:A._6=A._W;A._8=_A0;A._ae=_A0;return True
		return _A0
	def _h(A,command=0):
		B=command
		if not A._f(B):return _A0
		A._aa[0]=B;A._aa[1]=A._j();A._aa[2]=A._j();A._aa[3]=A._j();A._aa[4]=A._j();A._aa[5]=A._j();return A._g()
	def _i(A,i,command=0):
		B=command
		if not A._f(B):return _A0
		A._ac[i][0]=B;A._ac[i][1]=A._j();A._ac[i][2]=A._j();A._ac[i][3]=A._j();A._ac[i][4]=A._j();A._ac[i][5]=A._j();return A._g()
	def _j(A):
		if A._6>=A._7 or A._8:A._ae=True;return 0
		B=A._ad[A._6+1]<<8|A._ad[A._6];A._6+=2;return B
	def _g(A):
		if A._ae:A._ae=_A0;return _A0
		return A._6==A._7
	def _t(A,command=0):
		B=command;C=time.ticks_ms()
		while time.ticks_ms()-C<A._P:
			if A._e():
				if B!=0:
					if A._f(B):return True
				else:return True
		return _A0