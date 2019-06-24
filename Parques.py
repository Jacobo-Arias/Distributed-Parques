import pygame
import random
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

def torre(este): #creacion base torres cielo
    if este == 7:
        usuario = Bloque([77,25])
        usuario.image.fill(VERDE)
        usuario.rect.x = Ancho/2 - 77/2
        usuario.rect.y = 0
    if este == 1:
        usuario = Bloque([25,77])
        usuario.image.fill(AZUL)
        usuario.rect.x = 0
        usuario.rect.y = Alto/2 - 77 /2
    elif este == 3:
        usuario = Bloque([77,25])
        usuario.image.fill(ROJO)
        usuario.rect.x = Ancho/2 - 77/2
        usuario.rect.y = Alto - 24
    elif este == 5:
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
        if j in [1,3,5,7]: 
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
        contador[0] +=1

    return lista,bases,blancos



if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode([Ancho+400,Alto])
    fuente = pygame.font.Font(None, 20)



    grupo = pygame.sprite.Group()
    lista,bases,blancos = cuadros()
    grupo.add(lista)

    fin = False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
        

        grupo.draw(pantalla)
        for i in blancos:
            pantalla.blit(fuente.render(str(i.id_obj),False,[0,0,0]),i.rect.center)
        pygame.display.flip()