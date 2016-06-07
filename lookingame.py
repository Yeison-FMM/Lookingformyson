#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame, random, pyganim
from pygame.locals import * 

import imp
gamemanager = imp.load_source('gamemanager', 'gamemanager/gamemanager.py')
menustate = imp.load_source('menustates', 'states/menustate.py')

# Constantes
WIDTH = 800
HEIGHT = 600
# Clases
# ---------------------------------------------------------------------
class Opcion:

    def __init__(self, fuente, titulo, x, y, paridad, funcion_asignada):
        self.imagen_normal = fuente.render(titulo, 1, (83, 108, 93))
        self.imagen_destacada = fuente.render(titulo, 1, (200, 255, 0))
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
        self.rect.x = 500 * paridad
        self.rect.y = y
        self.funcion_asignada = funcion_asignada
        self.x = float(self.rect.x)

    def actualizar(self):
        destino_x = 710
        self.x += (destino_x - self.x) / 5.0
        self.rect.x = int(self.x)

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)

    def destacar(self, estado):
        if estado:
            self.image = self.imagen_destacada
        else:
            self.image = self.imagen_normal

    def activar(self):
        self.funcion_asignada()


class Cursor:

    def __init__(self, x, y, dy):
        self.image = pygame.image.load('images/cursor.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.y_inicial = y
        self.dy = dy
        self.y = 0
        self.seleccionar(0)

    def actualizar(self):
        self.y += (self.to_y - self.y) / 10.0
        self.rect.y = int(self.y)

    def seleccionar(self, indice):
        self.to_y = self.y_inicial + indice * self.dy

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)


class Menu:
    "Representa un menú con opciones para un juego"
    
    def __init__(self, opciones):
        self.opciones = []
        fuente = pygame.font.Font('fonts/FEASFBI_.TTF', 25)
        x = 710
        y = 10
        paridad = 1

        self.cursor = Cursor(x - 30, y, 33)
        for titulo, funcion in opciones:
            self.opciones.append(Opcion(fuente, titulo, x, y, paridad, funcion))
            y += 30
            if paridad == 1:
                paridad = -1
            else:
                paridad = 1

        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

    def actualizar(self):
        """Altera el valor de 'self.seleccionado' con los direccionales."""

        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                self.seleccionado -= 1
            elif k[K_DOWN]:
                self.seleccionado += 1
            elif k[K_RETURN]:
                # Invoca a la función asociada a la opción.
                self.opciones[self.seleccionado].activar()

        # procura que el cursor esté entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1
        
        self.cursor.seleccionar(self.seleccionado)

        # indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN]

        self.cursor.actualizar()
     
        for o in self.opciones:
            o.actualizar()

    def imprimir(self, screen):
        """Imprime sobre 'screen' el texto de cada opción del menú."""

        self.cursor.imprimir(screen)

        for opcion in self.opciones:
            opcion.imprimir(screen)


class LookinGame:
 	"""docstring for Bird"""
 	def __init__(self):
 		pygame.init()
 		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))		
		self.background_image = self.load_image("images/background_initial.png").convert()
		self.birdSprites = pyganim.PygAnimation([(self.load_image("images/birdtwo.png").convert_alpha(),200),
							(self.load_image("images/birdthree.png").convert_alpha(),200),
							(self.load_image("images/birdfour.png").convert_alpha(),200),
							(self.load_image("images/birdfive.png").convert_alpha(),200),
							(self.load_image("images/birdsix.png").convert_alpha(),200),
							(self.load_image("images/birdseven.png").convert_alpha(),200),
							(self.load_image("images/birdeight.png").convert_alpha(),200),
							(self.load_image("images/birdnine.png").convert_alpha(),200),
							(self.load_image("images/birdten.png").convert_alpha(),200),
							(self.load_image("images/birdeleven.png").convert_alpha(),200),
							(self.load_image("images/birdtwelve.png").convert_alpha(),200),
							(self.load_image("images/birdthirteen.png").convert_alpha(),200),
							(self.load_image("images/birdfourteen.png").convert_alpha(),200)])

	def load_image(self,filename, transparent=False):
	        try: image = pygame.image.load(filename)
	        except pygame.error, message:
	                raise SystemExit, message
	        image = image.convert()
	        if transparent:
	                color = image.get_at((0,0))
	                image.set_colorkey(color, RLEACCEL)
	        return image

	def salir_del_programa(self):
		print " Gracias por utilizar este programa."
		sys.exit(0)
 
	def comenzar_nuevo_juego(self):
		pygame.mixer.music.load("sounds/birdgame.mp3")
		print " Función que muestra un nuevo juego."
		clock = pygame.time.Clock()
		pygame.mixer.music.play()
		gameover = False
		while not gameover == True:
			for eventos in pygame.event.get():
				if eventos.type == pygame.KEYDOWN:
					if (eventos.key == pygame.K_o):
						gameover = True
						pygame.mixer.music.stop()
						self.run()
			self.screen.fill((255,255,255))
			self.birdSprites.blit(self.screen, (350, 50))
			pygame.display.update()
	
	def mostrar_opciones(self):
		pass	    

	def creditos(self):
		print " Función que muestra los creditos del programa." 

	def run(self):
		salir = False
		opciones = [
			("Jugar", self.comenzar_nuevo_juego),
			("Opciones", self.mostrar_opciones),
			("Salir", self.salir_del_programa)
        ]
		pygame.init()
		pygame.font.init()
		clock = pygame.time.Clock()
		screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption("Looking for my Son")
		pygame.mixer.music.load("sounds/intro.mp3")
		pygame.mixer.music.play(10)
		menu = Menu(opciones)
		while not salir:
			clock.tick(60)
			for eventos in pygame.event.get():
				if (eventos.type == QUIT):
					sys.exit(0)
					salir = True
			screen.blit(self.background_image, (0, 0))
			menu.actualizar()
			menu.imprimir(screen)
			pygame.display.flip()
			pygame.time.delay(10)
		return 0

if __name__ == '__main__':
	LookinGame().run()