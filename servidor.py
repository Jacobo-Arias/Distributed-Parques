import socket
import select
import sys
from thread import *
import datetime

seguros=[1,6,13,18,23,30,35,40,47,52,57,64]
#Aqui va las reglas del parques
class Tablero():
	def __init__(self):
		#Todas las fichas empiezan el la carcel
		self.jugador1=[0,0,0,0] #Verdes
		self.jugador2=[0,0,0,0] #Azules
		self.jugador3=[0,0,0,0] #Rojas
		self.jugador4=[0,0,0,0] #Amarillas
		#0 significa carcel
		#-1 significa cielo
		#en otro caso es el numero de la casilla

	def mover(self,jugador, jugadas):
		#De quien hablamos
		quien=self.quien(jugador)
		if quien.count(0)!=0 and self.presadas(jugadas):
			self.sacar(jugador)
			jugadas=['0','0','0','0']
		for n in range(4):
			if quien[n]>0:
				jugadas=self.cielo(jugador, jugadas)
				quien[n]+=int(jugadas[n])
				self.comer(quien,jugador)
				print("aqui")
				self.ganadas(jugador)
				print("salio")

#---------------------------------------------------------------------------------------CORREGIR
	def ganadas(self,jugador):
		for n in range(4):
			if jugador=="1" and self.jugador1[n]>75:
				self.jugador1[n]=-1
			if jugador=="2" and self.jugador2[n]>82:
				self.jugador2[n]=-1
			if jugador=="3" and self.jugador3[n]>89:
				self.jugador3[n]=-1
			if jugador=="4" and self.jugador4[n]>96:
				self.jugador4[n]=-1

	def comer(self,jugador, numero):
		for n in range(4):
			for m in range (4):
				if numero!="1":
					if jugador[n]==self.jugador1[m] and (jugador[n] not in seguros):#no seguros
						self.jugador1[m]=0
				if numero!="2":
					if jugador[n]==self.jugador2[m] and (jugador[n] not in seguros):#no seguros
						self.jugador2[m]=0
				if numero!="3":
					if jugador[n]==self.jugador3[m] and (jugador[n] not in seguros):#no seguros
						self.jugador3[m]=0
				if numero!="4":
					if jugador[n]==self.jugador4[m] and (jugador[n] not in seguros):#no seguros
						self.jugador4[m]=0

	def cielo(self,jugador, jugadas):
		if jugador=="1":
			for n in range(4):
				if self.jugador1[n]<69 and self.jugador1[n]+int(jugadas[n])>68: #Poner en la entrada al cielo
					jugadas[n]=str(int(jugadas[n])-(69-self.jugador1[n]))
					self.jugador1[n]=1
				print self.jugador1[n], jugadas[n]
				if self.jugador1[n]==1 and int(jugadas[n])>=1: #entrar al cielo
					print("aqui que")
					self.jugador1[n]= 69 #numero del cielo verde
					jugadas[n]= str(int(jugadas[n])-1)
		if jugador=="2":
			for n in range(4):
				if self.jugador2[n]<18 and self.jugador2[n]+int(jugadas[n])>17:
					jugadas[n]=str(int(jugadas[n])-(18-self.jugador2[n]))
					self.jugador2[n]=18
				if self.jugador2[n]==18 and int(jugadas[n])>=1:
					self.jugador2[n]= 76 #numero del cielo azul
					jugadas[n]= str(int(jugadas[n])-1)
		if jugador=="3":
			for n in range(4):
				if self.jugador3[n]<35 and self.jugador3[n]+int(jugadas[n])>34: #Poner en la entrada al cielo
					jugadas[n]=str(int(jugadas[n])-(35-self.jugador3[n]))
					self.jugador3[n]=35
				if self.jugador3[n]==35 and int(jugadas[n])>=1: #entrar al cielo
					self.jugador3[n]= 83 #numero del cielo rojo
					jugadas[n]= str(int(jugadas[n])-1)
		if jugador=="4":
			for n in range(4):
				if self.jugador4[n]<52 and self.jugador4[n]+int(jugadas[n])>51: #Poner en la entrada al cielo
					jugadas[n]=str(int(jugadas[n])-(52-self.jugador4[n]))
					self.jugador4[n]=52
				if self.jugador4[n]==52 and int(jugadas[n])>=1: #entrar al cielo
					self.jugador4[n]= 90 #numero del cielo amarillo
					jugadas[n]= str(int(jugadas[n])-1)
		return jugadas

	def sacar(self,jugador):
		if jugador=="1":
			for n, i in enumerate(self.jugador1):
				if i == 0:
					self.jugador1[n] = 6
	#Salida de las verdes
		if jugador=="2":
			for n, i in enumerate(self.jugador2):
				if i == 0:
					self.jugador2[n] = 23
	#Salida de las azules
		if jugador=="3":
			for n, i in enumerate(self.jugador3):
				if i == 0:
					self.jugador3[n] = 40
	#Salida de las rojas
		if jugador=="4":
			for n, i in enumerate(self.jugador4):
				if i == 0:
					self.jugador4[n] = 57
	#Salida de las amarillas

#---------------------------------------------------------------------------------------CORREGIR
	def quien(self,jugador):
		if jugador=="1":
			return self.jugador1
		if jugador=="2":
			return self.jugador2
		if jugador=="3":
			return self.jugador3
		if jugador=="4":
			return self.jugador4

	def presadas(self,jugada):
		if jugada.count('1')==2:
			return True
		if jugada.count('2')==2:
			return True
		if jugada.count('3')==2:
			return True
		if jugada.count('4')==2:
			return True
		if jugada.count('5')==2:
			return True
		if jugada.count('6')==2:
			return True
		return False
#---------------------------------

#metemos jugadores hasta que no halla cupo
def iniciar_jugador(nombre, direccion):
	for n in range(len(listaNombres)):
		if listaNombres[n] is None:
			listaNombres[n]=[nombre,direccion]
			break

#Vemos quienes faltan
def incompletos():
	for n in listaNombres:
		if n is None:
			return True
	return False

#Sala de espera
def armar_estado():
	mensaje=""
	for n in listaNombres:
		if n is not None:
			mensaje+= n[0]+"\n"
	return mensaje

def estado_tablero():
	mensaje=""
	for n in Game.jugador1:
		mensaje+= str(n)+" "
	for n in Game.jugador2:
		mensaje+= str(n)+" "
	for n in Game.jugador3:
		mensaje+= str(n)+" "
	for n in Game.jugador4:
		mensaje+= str(n)+" "
	mensaje=mensaje[:-1]
	print mensaje
	return mensaje

#Si tenes todas las fichas en el cielo ganas
def ganador():
	if Game.jugador3==[-1,-1,-1,-1]:
		return "Rojas"
	if Game.jugador4==[-1,-1,-1,-1]:
		return "Amarillas"
	if Game.jugador1==[-1,-1,-1,-1]:
		return "Verdes"
	if Game.jugador2==[-1,-1,-1,-1]:
		return "Azules"
	return "nadie"

def clienteHilo(conn, addr):
	conn.send("Bienvenido a Parchis Stars <3\n")
	#O estamos todos o no empezamos
	mensaje = conn.recv(1024)
	if mensaje[0]==":":
		iniciar_jugador(mensaje, addr[0])
		envio = mensaje + " se ha unido\n" + armar_estado()
		broadcast(envio)
		if not incompletos():
			asignar()
	else:
		remove(conn)

	while incompletos():
		continue

	print "cupo lleno\n"

	global turno
	global uso

	while True:
		if ganador()!="nadie":
			broadcast("Ganan las fichas "+ganador())
			break
		try:
			#El mensaje tendra la siguiente estructura
			#Njugador:cuanto la quiere mover ficha de posicion
			#Las fichas que no se mueven tienen 0 en el segundo campo
			mensaje = conn.recv(1024)
			print mensaje,turno,uso
			#Semaforo por turnos
			if mensaje[0]=="1" and turno==1 and uso:
				#Descifro el mensaje
				uso=False
				move = mensaje.split(":")[1].split(" ")
				if not Game.presadas(move):
					turno=2
				Game.mover(mensaje[0], move)
				uso=True
				print estado_tablero()
				broadcast(estado_tablero())
				print "enviado"
			if mensaje[0]=="2" and turno==2 and uso:
				#Descifro el mensaje
				print "aqui"
				uso=False
				move = mensaje.split(":")[1].split(" ")
				if not Game.presadas(move):
					turno=3
				Game.mover(mensaje[0], move)
				uso=True
				broadcast(estado_tablero())
			if mensaje[0]=="3" and turno==3 and uso:
				#Descifro el mensaje
				uso=False
				move = mensaje.split(":")[1].split(" ")
				if not Game.presadas(move):
					turno=4
				Game.mover(mensaje[0], move)
				uso=True
				broadcast(estado_tablero())
			if mensaje[0]=="4" and turno==4 and uso:
				#Descifro el mensaje
				uso=False
				move = mensaje.split(":")[1].split(" ")
				if not Game.presadas(move):
					turno=1
				Game.mover(mensaje[0], move)
				uso=True
				broadcast(estado_tablero())
		except:
			continue

def asignar():
	mensaje=1
	for cliente in clientes:
		try:
			cliente.send("#"+str(mensaje))
			mensaje+=1
		except:
			cliente.close()
			remove(cliente)

def broadcast(mensaje):
	for cliente in clientes:
		try:
			cliente.send(mensaje)
		except:
			cliente.close()
			remove(cliente)

def remove(conexion):
	if conexion in clientes:
		clientes.remove(conexion)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(("localhost", 8000))
server.listen(5)
clientes = []
listaNombres = [None,None,None,None]
Game=Tablero()
finalserver=False
turno=1
uso=True

while not finalserver:
	conn, addr = server.accept()
	clientes.append(conn)
	print addr[0] + " se ha conectado"
	start_new_thread(clienteHilo,(conn,addr))
conn.close()
server.close()