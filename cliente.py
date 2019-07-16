import socket
import select
import sys
import os
from thread import *
import random

def armar(jugada):
	mensaje=numero+":"
	for n in jugada:
		mensaje+=str(n)+" "
	return mensaje[:-1]

def lanzar():
	global uso
	if not uso:
		uso=True
		x=raw_input("Desea lanzar los dados? y/n")
		if x=="y":
			jugada=[0,0,0,0]
			d1=random.randint(1,6)
			d2=random.randint(1,6)
			print d1,d2
			for n in range(4):
				jugada[n]=input("Cuanto quiere mover la ficha {}".format(n+1))
			mensaje=armar(jugada)
			server.send(mensaje)
		uso=False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", 8000))

os.system('cls' if os.name == 'nt' else 'clear')
nombre = raw_input("Ingresa tu nombre:")
server.send(":"+nombre)
numero="0"
juego=False
uso=False

while not juego:
	sockets= [sys.stdin, server]
	leidos,escrito, error = select.select(sockets,[],[])
	for socks in leidos:
		if socks == server:
			mensaje = socks.recv(1024)
			os.system('cls' if os.name == 'nt' else 'clear')
			if mensaje.count("#")>0:
				print("Mi numero es #"+mensaje[-1])
				numero=mensaje[-1]
				juego=True
				break
			print mensaje
while juego:
	start_new_thread(lanzar,())
	sockets= [sys.stdin, server]
	leidos,escrito, error = select.select(sockets,[],[])
	for socks in leidos:
		if socks == server:
			print("recv")
			mensaje = socks.recv(1024)
			print mensaje
			if mensaje[0]=="G":	
				print(mensaje)
				juego=False
				break

server.close()