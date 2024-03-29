import pygame
import random
import datetime
import socket
import select
import sys
import os
import thread
from thread import *
import random

#juego de parques distribuido

Ancho=650
Alto=650
VERDE=[0,255,0]
AZUL=[0,0,255]
ROJO=[255,0,0]
BLANCO=[255,255,255]
AMARILLO=[253,232,15]
colores=[VERDE,AZUL,AMARILLO,ROJO,[150,150,250]]
contador = [1]
centros = [[105,105],[105,Alto-105],[Ancho-105,105],[Ancho-105,Alto-105],[Ancho/2,Alto/2]]

class Bloque (pygame.sprite.Sprite):
    def __init__(self,dimen,cont=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dimen)
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.id_obj = cont

class Ficho(pygame.sprite.Sprite):
    def __init__(self,nume = [0,1],cielo = [0,0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,10])
        self.color = [nume[0][0]/6*4,nume[0][1]/6*4,nume[0][2]/6*4]
        self.id = nume
        self.rect = self.image.get_rect()
        self.nume = nume
        self.safe = True
        self.pos = 0
        self.cielo = cielo

class botonFicha (pygame.sprite.Sprite):
    def __init__(self, numFicho):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50, 50])
        self.image.fill([220, 220, 220])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.presionado = False
        self.ficha = numFicho
        self.texto = 0
        self.carcel = True
        self.cielo = False
        self.seleccionado = False
        self.valorAMover = 0

	def reiniciarSeleccion(self):
		if self.seleccionado:
			self.image.fill([220, 220, 220])
			self.seleccionado = False

    def estaSeleccionado (self):
        if self.seleccionado == False:
            self.seleccionado = True
            self.image.fill([30, 200, 30])
        else:
            self.seleccionado = False
            self.image.fill([220, 220, 220])
'''
class botonDado (pygame.sprite.Sprite):
    def __init__(self, dado):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50, 50])
        self.image.fill([220, 220, 220])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.valor = 0
        self.dado = dado
        self.seleccionado = False
'''
class Dado (pygame.sprite.Sprite):
    def __init__(self, numeroDado):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([150, 150])
        self.image.fill([220, 220, 220])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.valor = 0
        self.carcel = False
        self.lanzamientoTurno = 1
        self.numeroDado = numeroDado
        self.seleccionado = False

    def updateValor (self, v):
        self.valor = v

    def estaSeleccionado (self):
        if self.seleccionado == False:
            self.seleccionado = True
            self.image.fill([30, 200, 30])
        else:
            self.seleccionado = False
            self.image.fill([220, 220, 220])

class botonLanzamiento (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([150, 50])
        self.image.fill([63, 122, 77])
        self.rect = self.image.get_rect()
        self.rect.x = 770
        self.rect.y = 200
        self.presionado = False
        self.texto = "Lanzar"

    def presionarBoton(self):
        if self.presionado:
            pass

class botonMovimiento (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([150, 50])
        self.image.fill([63, 122, 77])
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 350
        self.presionado = False
        self.texto = "Mover"

    def presionarBoton(self):
        if self.presionado:
            pass

def lanzamientoDados (inicioJuego, fichasRestantes):
    lanzamientos = 1
    if inicioJuego:
        lanzamientos = 3
        for i in range (0, lanzamientos):
            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)
    else:
        for i in range (0, lanzamientos):
            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)
        if fichasRestantes == 1:
            dado2 = 0
    return dado1, dado2

def CreacionFichos():
    aux = [[1,69,75],[18,76,82],[52,90,96],[35,83,89]]
    completa = []
    for j in range (4):
		lista = []
		for i in range (4):
			ficha = Ficho([colores[j],i+1],aux[j])
			ficha.rect.center = [j*50+50,i*50+50]
			lista.append(ficha)
		completa.append(lista)
    print (len(lista))
    return completa

def torre(este): #creacion base torres cielo
    if este == 0:
        usuario = Bloque([77,25])
        usuario.image.fill(VERDE)
        usuario.rect.x = Ancho/2 - 77/2
        usuario.rect.y = 0
    if este == 2:
        usuario = Bloque([25,77])
        usuario.image.fill(AZUL)
        usuario.rect.x = 0
        usuario.rect.y = Alto/2 - 77 /2
    elif este == 4:
        usuario = Bloque([77,25])
        usuario.image.fill(ROJO)
        usuario.rect.x = Ancho/2 - 77/2
        usuario.rect.y = Alto - 24
    elif este == 6:
        usuario = Bloque([25,77])
        usuario.image.fill(AMARILLO)
        usuario.rect.x = Ancho-25
        usuario.rect.y = Alto/2 - 77 /2
    return usuario

def cuadros():
    lista =[]
    bases =[]
    blancos=[]
    for i in range(5): #Se crean las bases
        usuario = Bloque([210,210],200*(i+1))
        usuario.image.fill(colores[i])
        usuario.rect.center = centros[i]
        if i == 4:
            usuario.image = pygame.image.load("cielo.png")
        lista.append(usuario)
        bases.append(usuario)

    for j in range (8):  #Creacion cuadros
        if j in [0,2,4,6]:
            aux = torre(j)
            blancos.append(aux)
            lista.append(aux)
        if j in [0,3,4,7]: size = [77,25]
        else: size = [25,77]
        for i in range (8):
            k = 0
            usuario = Bloque(size)

            if j == 0: #**arriba izquierda
                k = 0
                usuario.rect.x = 210
                usuario.rect.y = i*27

            elif j == 1: #**izquierda arriba
                k = 0
                usuario.rect.y = 210
                usuario.rect.x = 189-i*27

            elif j == 2: #?izquierda abajo
                k = 1
                usuario.rect.y = Ancho-287
                usuario.rect.x = i*27

            elif j == 3:#?abajo izquierda
                k = 1
                usuario.rect.x = 210
                usuario.rect.y = 436+(i*27)

            elif j == 4:#!abajo derecha
                k = 3
                usuario.rect.x = Ancho-287
                usuario.rect.y = Alto-(i*27+25)

            elif j == 5:#!derecha abajo
                k = 3
                usuario.rect.y = Alto-287
                usuario.rect.x = 436+(i*27)

            elif j == 6:#TODO: derecha arriba
                k = 2
                usuario.rect.y = 210
                usuario.rect.x = Alto-(i*27+25)

            else:#TODO:arriba derecha
                k = 2
                usuario.rect.x = Ancho-287
                usuario.rect.y = 189-i*27

            if j in [0,2,4,6]:
                if i == 4: usuario.image.fill(colores[k])
                else: usuario.image.fill(BLANCO)
            else:
                if i == 3: usuario.image.fill(colores[k])
                else: usuario.image.fill(BLANCO)

            lista.append(usuario)
            blancos.append(usuario)

    for j in range(4): #creacion torres al cielo
        if j in [0,2]: size = [77,25]
        else: size = [25,77]
        for i in range(7):
            usuario = Bloque(size)

            if j == 0: #*arriba
                usuario.image.fill(VERDE)
                usuario.rect.x = 287
                usuario.rect.y = i*27+27

            elif j == 1: #?izquierda
                usuario.image.fill(AZUL)
                usuario.rect.y = 287
                usuario.rect.x = 27+i*27

            elif j == 2:#!abajo
                usuario.image.fill(ROJO)
                usuario.rect.x = 287
                usuario.rect.y = Alto-(i*27)-52

            elif j == 3:#TODO: derecha arriba
                usuario.image.fill(AMARILLO)
                usuario.rect.y = 287
                usuario.rect.x = Alto-(i*27+52)

            lista.append(usuario)
            blancos.append(usuario)

    for i in blancos:
        i.id_obj = contador[0]
        contador[0] += 1

    return lista,bases,blancos

def creadados():
    result = []
    for i in range (0, 2):
        dado = Dado(i+1)
        if i == 0:
            dado.rect.x = 680
            dado.rect.y = 20
        else:
            dado.rect.x = 870
            dado.rect.y = 20
        result.append(dado)
    return result

def creabotones():
    salida = []
    for i in range (0,4):
        botonF = botonFicha(i+1)
        if i == 0:
            botonF.ficha = 1
            botonF.rect.x = 680
            botonF.rect.y = 400
        elif i == 1:
            botonF.ficha = 2
            botonF.rect.x = 780
            botonF.rect.y = 400
        elif i == 2:
            botonF.ficha = 3
            botonF.rect.x = 680
            botonF.rect.y = 500
        elif i == 3:
            botonF.ficha = 4
            botonF.rect.x = 780
            botonF.rect.y = 500
        salida.append(botonF)
    return salida

def creaBotonMover():
	salida = []
	botonM = botonMovimiento()
	return salida

def armar(jugada):
	mensaje=numero+":"
	for n in jugada:
		mensaje+=str(n)+" "
	return mensaje[:-1]

def lanzar():
	global pantalla
	movimientos = 2
	global uso
	while True:
		pantalla.fill([255,255,255])
		if not uso:
			uso=True
			"""
			x=raw_input("Desea lanzar los dados? y/n")
			if x=="y":
				jugada=[0,0,0,0]
				d1=random.randint(1,6)
				d2=random.randint(1,6)
				print (d1,d2)
				for n in range(4):
					jugada[n]=input("Cuanto quiere mover la ficha {}".format(n+1))
				mensaje=armar(jugada)
				server.send(mensaje)
			"""
			jugada=[0,0,0,0]
			for event in pygame.event.get():
					pos=pygame.mouse.get_pos()
					#Eventos dentro del juego
					if event.type == pygame.QUIT:
						fin = True

					if event.type == pygame.MOUSEBUTTONDOWN:
							print ("Clic")
							clicD = 1
							clicM = True
							for b in botones:
								if b.rect.collidepoint(pos):
									if clicD == 1:
										dadosT = lanzamientoDados(False, 3)
										movimientos = 2
										for f in botonesFichas:
											f.valorAMover = 0
											f.seleccionado = False

										print (dadosT)
										posiblesLanzamientos =[dadosT[0] + dadosT[1], dadosT[0], dadosT[1]]
										if dadosT[0] == dadosT[1]:
											presada = True
										else:
											presada = False
										for dado in dados:
											dado.seleccionado = False
											pantalla.blit(fuenteDados.render(str(dado.valor), False, [220,220,220]), dado.rect.center)
										pygame.display.flip()

									for d in dados:
										pantalla.blit(fuenteDados.render(str(dado.valor), False, [220, 220, 220]), dado.rect.center)
										d.image.fill([220,220,220])
										if d.numeroDado == 1:
											d.valor = dadosT[0]
											d.updateValor(dadosT[0])
										else:
											d.valor = dadosT[1]
											d.updateValor(dadosT[1])
							for d in dados:
								if d.rect.collidepoint(pos):
									d.estaSeleccionado()
									if d.numeroDado == 1:
										if d.seleccionado:
											listaDados[0] = d.valor
											listaDados[2] = True
										else:
											listaDados[0] = 0
											listaDados[2] = False

									else:
										if d.seleccionado:
											listaDados[1] = d.valor
											listaDados[3] = True
										else:
											listaDados[1] = 0
											listaDados[3] = False
							
							for b in botonesFichas:
								if b.rect.collidepoint(pos):
									b.estaSeleccionado()
									if b.seleccionado and movimientos > 0:
										if listaDados[2]:
											if b.ficha == 1:
												b.valorAMover += listaDados[0]
												movimientos -= 1
												b.seleccionado = False
												b.image.fill([220, 220, 220])
												for d in dados:
													d.image.fill([220, 220, 220])
												pygame.display.flip()
											if b.ficha == 2:
												b.valorAMover += listaDados[0]
												movimientos -= 1
												b.seleccionado = False
												b.image.fill([220, 220, 220])
												for d in dados:
													d.image.fill([220, 220, 220])
												pygame.display.flip()
											if b.ficha == 3:
												b.valorAMover += listaDados[0]
												movimientos -= 1
												b.seleccionado = False
												b.image.fill([220, 220, 220])
												for d in dados:
													d.image.fill([220, 220, 220])
												pygame.display.flip()

											if b.ficha == 4:
												b.valorAMover = listaDados[0]
												movimientos -= 1
												b.seleccionado = False
												b.image.fill([220, 220, 220])
												for d in dados:
													d.image.fill([220, 220, 220])
												pygame.display.flip()
											listaDados[2] = False
												
										elif listaDados[3]:
											if b.ficha == 1:
												b.valorAMover += listaDados[1]
												movimientos -= 1
												b.seleccionado = False
												b.image.fill([220, 220, 220])
												for d in dados:
													d.image.fill([220, 220, 220])
												pygame.display.flip()
											if b.ficha == 2:
												b.valorAMover += listaDados[1]
												movimientos -= 1
												b.seleccionado = False
												b.image.fill([220, 220, 220])
												for d in dados:
													d.image.fill([220, 220, 220])
												pygame.display.flip()
											if b.ficha == 3:
												b.valorAMover += listaDados[1]
												movimientos -= 1
												b.seleccionado = False
												b.image.fill([220, 220, 220])
												for d in dados:
													d.image.fill([220, 220, 220])
												pygame.display.flip()

											if b.ficha == 4:
												b.valorAMover += listaDados[1]
												movimientos -= 1
												b.seleccionado = False
												b.image.fill([220, 220, 220])
												for d in dados:
													d.image.fill([220, 220, 220])
												pygame.display.flip()
											b.image.fill([220, 220, 220])
											listaDados[3] = False

							for b in botonesMover:
								if clicM:
									global numero
									global server
									if b.rect.collidepoint(pos):
										print "envio"
										mensaje=numero+":"
										jugada=[]
										for b in botonesFichas:
											jugada.append(b.valorAMover)
										for n in jugada:
											mensaje+=str(n)+" "
										mensaje= mensaje[:-1]
										server.send(mensaje)
								clicM = False
								clicD = 0
			#Se dibujan casillas
			grupo.draw(pantalla)
			for j in blancos:
				pantalla.blit(fuente.render(str(j.id_obj),False,[0,0,0]),j.rect.center)
				for fichito in fichos:
					for i in fichito:
						if not i.pos in [-1,0]:
							if j.id_obj == i.pos:
								i.rect.center = j.rect.center
								print i.pos

						elif i.pos == 0:
							if i.id[0] == VERDE:
								i.rect.center = [centros[0][0],centros[0][1]-75+i.id[1]*25]
							elif i.id[0] == AZUL:
								i.rect.center = [centros[1][0],centros[1][1]-75+i.id[1]*25]
							elif i.id[0] == AMARILLO:
								i.rect.center = [centros[2][0],centros[2][1]-75+i.id[1]*25]
							elif i.id[0] == ROJO:
								i.rect.center = [centros[3][0],centros[3][1]-75+i.id[1]*25]

						elif i.pos == -1:
							i.rect.center = [-30,-30]
				
			for fichitos in fichos:
				for i in fichitos:
					pygame.draw.circle(pantalla,i.color,i.rect.center,9)
					pantalla.blit(fuente.render(str(i.nume[1]),False,[255,255,255]),i.rect)


			#Dados pos
			pygame.draw.rect(pantalla, [0,0,0], [680, 20, 150, 150], 4)
			pygame.draw.rect(pantalla, [0,0,0], [870, 20, 150, 150], 4)

			#Boton lanzar
			pygame.draw.rect(pantalla, [0,0,0], [770, 200, 150, 50], 4)
			#Boton mover
			pygame.draw.rect(pantalla, [0,0,0], [900, 350, 150, 50], 4)

			#Se dibujan dados y boton de lanzamiento
			todos.draw(pantalla)

			for dado in dados:
				pantalla.blit(fuenteDados.render(str(dado.valor), False, [0,0,0]), dado.rect.center)
			for b in botones:
				pantalla.blit(fuenteDados.render("Lanzar", False, [0,0,0]), b.rect.topleft)
			for b in botonesFichas:
				pantalla.blit(fuenteDados.render(str(b.ficha), False, [0,0,0]), b.rect.topleft)
				pantalla.blit(fuenteDados.render(str(b.valorAMover), False, [0,0,0]), b.rect.center)
			for b in botonesMover:
				pantalla.blit(fuenteDados.render("Mover", False, [0,0,0]), b.rect.topleft)

			pantalla.blit(fuenteDados.render("Fichas", False, [0,0,0]), [700, 350])
			pygame.display.flip()
			uso=False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("192.168.9.17", 8000))

os.system('cls' if os.name == 'nt' else 'clear')
nombre = raw_input("Ingresa tu nombre:")
server.send(":"+nombre)
numero="0"
juego=False
uso=False
listaDados= [0, 0, False, False]

if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode([Ancho+400,Alto])
    fuente = pygame.font.Font(None, 20)
    fuenteDados = pygame.font.Font(None, 50)
    todos = pygame.sprite.Group()
    botones = pygame.sprite.Group()
    botonesFichas = pygame.sprite.Group()
    botonesMover = pygame.sprite.Group()
    dados = pygame.sprite.Group()
    grupo = pygame.sprite.Group()
    lista, bases, blancos = cuadros()
    grupo.add(lista)
    fichos = CreacionFichos()

    pygame.draw.rect(pantalla,[255,255,255],[[650,0],[850,650]])
    pygame.draw.line(pantalla,[0,0,0],[650,0],[650,650],2)

    dado = creadados()
    dados.add(dado)
    todos.add(dado)

    botonF = creabotones()
    botonesFichas.add(botonF)
    todos.add(botonF)

    botonesFichas.add(botonF)
    todos.add(botonF)

    botonLanzar = botonLanzamiento()
    botones.add(botonLanzar)
    todos.add(botonLanzar)

    botonMov = botonMovimiento()
    botonesMover.add(botonMov)
    todos.add(botonMov)

    presada = False
    fin = False

    while not juego:
        sockets = [sys.stdin, server]
        leidos, escrito, error = select.select(sockets, [], [])
        for socks in leidos:
            if socks == server:
                mensaje = socks.recv(1024)
                os.system('cls' if os.name == 'nt' else 'clear')
                if mensaje.count("#") > 0:
                    print ("Mi numero es #: " + mensaje[-1])
                    numero = mensaje[-1]
                    juego = True
                    break
                print (mensaje)
    if juego:
		start_new_thread(lanzar,())
		while not fin:
			pantalla.fill([255,255,255])
			sockets =[sys.stdin, server]
			leidos, escrito, error = select.select(sockets, [], [])
			for socks in leidos:
				if socks == server:
					mensaje = socks.recv(1024)
					print mensaje
					mensaje = mensaje.split("#")
					aux = mensaje[3]
					mensaje[3] = mensaje[2]
					mensaje[2] = aux
					pantalla.blit(fuenteDados.render(str(mensaje[-1]), False, [0,0,0]), [700, 600])
					for n in range(4):
						mensaje[n] = mensaje[n].split(" ")
					print mensaje
					
					print len(fichos)
					for n in fichos:
						print len(n), "elemento"

					for i in range(4):
						for j in range(4):
							fichos[i][j].pos=int(mensaje[i][j])
					
					for i in range(4):
						for j in range(4):
							print fichos[i][j].pos
					print("actualice")
					if mensaje[0] == 'G':
						juego = False
						fin = True
					break
    server.close()