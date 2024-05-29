_T='x-cross'
_S='arcr'
_R='l3'
_Q='l'
_P='crsr'
_O='mswp'
_N='ast'
_M='right'
_L='left'
_K='down'
_J='up'
_I='vt'
_H='sbne'
_G='l9'
_F='txt'
_E=False
_D='l6'
_C='y'
_B='x'
_A=True
tCD=20
fieldSizeX=5
fieldSizeY=5
import random,time,microbit
class Field:
	xFieldSize=5;yFieldSize=5
	def __init__(A):A.field={};A.field['layer0']=[];A.field[_R]=[];A.field[_D]=[];A.field[_G]=[]
	def addShip(A,ship):A.field[_D].append(ship)
	def aRSl(A,type):
		B=1 if type==_O else 2 if type==_H else 3 if type==_P else 4;D=20
		while D>0:
			D-=1;C=_I if random.randint(0,1)==0 else'hori';E=gTc(A.xFieldSize,B,C)[_B];F=gTc(A.yFieldSize,B,C)[_C];G=Ship(E,F,B,C)
			if A.checkShipConstraint(G)==_A:continue
			A.addShip(G);return{_B:E,_C:F,'rot':C,'size':B}
		raise Exception('h')
	def checkShipConstraint(E,ship):
		B=ship;C=cS(B)
		for A in C:
			if A[_B]<1 or A[_B]>fieldSizeX or A[_C]<1 or A[_C]>fieldSizeY:return _A
		F=E.field[_D];D=[]
		for B in F:D+=cS(B)
		for A in C:
			if A in D:print('overlap');return _A
		return _E
	def addPlayer(A,player):
		B=player
		if len(A.field[_G])>0:raise AssertionError('h')
		A.field[_G].append(B)
	def removeShip(B,ship,layer=6):A=layer;B.field[_Q+str(A)].remove(ship)
	def changeObjectLayer(C,object,fromLayer,toLayer):B=toLayer;A=fromLayer;C.field[_Q+str(B)].append(object);C.field[_Q+str(A)].remove(object)
class Ship:
	def __init__(A,xPos,yPos,size,rot):D=rot;C=yPos;B=xPos;A.xPos=B;A.yPos=C;A.size=size;A.rot=D
class Player:
	def __init__(A):A.xPos=1;A.yPos=1
	def move(A,direction):
		B=direction
		if B==_J:A.yPos-=1
		elif B==_K:A.yPos+=1
		elif B==_L:A.xPos-=1
		elif B==_M:A.xPos+=1
		if A.xPos<1:A.xPos=1
		elif A.xPos>fieldSizeX:A.xPos=fieldSizeX
		if A.yPos<1:A.yPos=1
		elif A.yPos>fieldSizeY:A.yPos=fieldSizeX
	def setPosition(A,x,y):A.xPos=x;A.yPos=y
	def getPosition(A):return{_B:A.xPos,_C:A.yPos}
class Render:
	def __init__(B,field):A=field;B.field=A
	def __gpx(K,layers):
		C=layers;B=[[0]*fieldSizeX for A in range(fieldSizeY)];D=K.field.field;G=D[_R];H=D[_D];I=D[_G]
		if not 3 in C:G=[]
		if not 6 in C:H=[]
		if not 9 in C:I=[]
		for E in G:
			F=cS(E)
			for A in F:B[A[_C]-1][A[_B]-1]=3
		for E in H:
			F=cS(E)
			for A in F:B[A[_C]-1][A[_B]-1]=6
		for J in I:B[J.yPos-1][J.xPos-1]=9
		return B
	def rM(E,layers):
		A=E.__gpx(layers);print(A)
		for(B,F)in enumerate(A):
			for(C,D)in enumerate(F):
				G=microbit.display.get_pixel(C,B)
				if D==G:continue
				microbit.display.set_pixel(C,B,D)
	def rO(A,type,input=None):
		if type==_T:microbit.display.show(microbit.Image.NO,delay=500,clear=_A,wait=_A)
		elif type=='skull':microbit.display.show(microbit.Image.SKULL,delay=500,clear=_A,wait=_A)
		elif type=='win':microbit.display.show(microbit.Image.HAPPY,delay=500,clear=_A,wait=_A)
		elif type==_F:microbit.display.scroll(str(input),delay=100,wait=_A)
		else:raise AssertionError('h')
def cS(ship):
	A=ship;B=[]
	for C in range(A.size):
		if A.rot==_I:B.append({_B:A.xPos,_C:A.yPos+C})
		else:B.append({_B:A.xPos+C,_C:A.yPos})
	return B
def gT():return{_B:random.randint(1,5),_C:random.randint(1,5)}
def gTc(max,length,rot):
	A=max-length+1
	if rot==_I:return{_B:random.randint(1,max),_C:random.randint(1,A)}
	else:return{_B:random.randint(1,A),_C:random.randint(1,max)}
def gTF(field,x,y):
	C=field.field[_D]
	for A in C:
		D=cS(A)
		for B in D:
			if B[_B]==x and B[_C]==y:return A
def fr(field,x,y):
	A=field;B=gTF(A,x,y)
	if B!=None:
		if B in A.field[_D]:return _A
	return _E
while _A:
	field=Field()
	try:field.aRSl(_O);field.aRSl(_H);field.aRSl(_H);field.aRSl(_P);field.aRSl(_S)
	except:continue
	player=Player();field.addPlayer(player);renderer=Render(field);attempts=0;cDu=0;cRDIN=_A
	while _A:
		dR=_E;dSRk=_E
		if cRDIN==_A:dR=_A;cRDIN=_E
		if cDu>0:cDu-=1
		gesture=microbit.accelerometer.current_gesture()
		if gesture==_J:
			if not cDu>0:player.move(_J);dR=_A;cDu=tCD
		elif gesture==_K:
			if not cDu>0:player.move(_K);dR=_A;cDu=tCD
		elif gesture==_L:
			if not cDu>0:player.move(_L);dR=_A;cDu=tCD
		elif gesture==_M:
			if not cDu>0:player.move(_M);dR=_A;cDu=tCD
		elif gesture=='shake':break
		bAP=microbit.button_a.get_presses();bBPs=microbit.button_b.get_presses();bBPd=microbit.button_b.is_pressed()
		if bAP>0:
			attempts+=1;hit=fr(field,player.xPos,player.yPos)
			if hit==_A:
				field.changeObjectLayer(gTF(field,player.xPos,player.yPos),6,3);renderer.rO('skull');time.sleep(.1);renderer.rO(_F,'HIT');time.sleep(.1);cRDIN=_A
				if len(field.field[_D])<1:renderer.rO('win');time.sleep(.1);renderer.rO(_F,'WIN!');time.sleep(.1);renderer.rO(_F,'Attempts: '+str(attempts));cRDIN=_A;break
			else:renderer.rO(_T);time.sleep(.1);renderer.rO(_F,'MISS');time.sleep(.1);cRDIN=_A
		if bBPs>0 or bBPd==_A:dR=_A;dSRk=_A;cRDIN=_A
		if dR:renderer.rM([3,9])
		if dR and dSRk:renderer.rM([3,6,9])
		time.sleep(.05)