# Aqui procedo a importar las bibliotecas necesarias para empezar a construir el juego.
import pygame
import sys
import random
import time

# Inicializao la biblioteca de Pygame
pygame.init()

# Aqui procedo a darle las dimensiones que tendra la pantalla de juego.
screen_width = 800 
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Ahora definimos los colores.
color_blanco = (255, 255, 255) # El blanco sera el jugador
color_negro = (0, 0, 0) # El negro sera el fondo del juego
color_rojo = (255, 0, 0) # El rojo los obstaculos o enemigo

# El reloj que tiene como objetivo controlar los FPS del juego
clock = pygame.time.Clock()

# Definimos la clase del jugador
class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
    
    # Aqui le definimos el movimiento al jugador
    def mover(self):
        llave = pygame.key.get_pressed()
        if llave[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if llave[pygame.K_RIGHT] and self.x < screen_width - 50:
            self.x += self.speed
        if llave[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if llave[pygame.K_DOWN] and self.y < screen_height - 50:
            self.y += self.speed
    
    # Aqui dibujamos el jugador dentro del juego
    def draw(self, screen):
        pygame.draw.rect(screen, color_blanco, (self.x, self.y, 50, 50))

# Ahora procedo a definir la clase del enemigo
class Enemigo:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
    
    # De igual forma definimos el movimiento que tendra el enemigo
    def mover(self):
        self.y += self.speed
        if self.y > screen_height:
            self.y = -50
            self.x = random.randint(0, screen_width - 50)
    
    # Aqui dibujamos el jenemigo dentro del juego
    def draw(self, screen):
        pygame.draw.rect(screen, color_rojo, (self.x, self.y, 50, 50))

# Aqui se crea la colision entre el jugador y el enemigo (Los cuadros rojos)
def colision(jugador, enemigo):
    return (jugador.x < enemigo.x + 50 and
            jugador.x + 50 > enemigo.x and
            jugador.y < enemigo.y + 50 and
            jugador.y + 50 > enemigo.y)

# Si perdimos, aqui nos dara la opcion de reintentar o salir
def mostrar_opciones(screen, mensaje, color, opciones):
    run = True
    while run:
        screen.fill(color_negro)
        font = pygame.font.Font(None, 74)
        text = font.render(mensaje, True, color)
        screen.blit(text, (screen_width // 4, screen_height // 4))
        
        font_opcion = pygame.font.Font(None, 50)
        opcion1 = font_opcion.render(opciones[0], True, color_blanco)
        opcion2 = font_opcion.render(opciones[1], True, color_blanco)
        screen.blit(opcion1, (screen_width // 4, screen_height // 2))
        screen.blit(opcion2, (screen_width // 4, screen_height // 2 + 60))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Aqui defino la tecla "R" para reintentar
                    return 'retry'
                if event.key == pygame.K_q:  # Aqui defino la tecla "Q" para salir
                    return 'quit'

# Aqui creo los multiples obstaculos del juego
def crear_enemigos(numero, velocidad_inicial):
    enemigos = []
    for i in range(numero):
        x = random.randint(0, screen_width - 50)
        y = random.randint(-600, -50)
        enemigos.append(Enemigo(x, y, velocidad_inicial))
    return enemigos

# Esta sera la pantalla de inicio
def pantalla_inicio():
    run = True
    while run:
        screen.fill(color_negro)
        font_titulo = pygame.font.Font(None, 100)
        font_opcion = pygame.font.Font(None, 50)
        
        titulo = font_titulo.render('Carrera.io', True, color_blanco)
        opcion = font_opcion.render('Presiona Enter para empezar', True, color_blanco)
        
        screen.blit(titulo, (screen_width // 4, screen_height // 4))
        screen.blit(opcion, (screen_width // 6, screen_height // 2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Opcion que definimos para empezar
                    run = False
        
        pygame.display.update()

# Aqui creamos la funcion de bucle del juego
def game_loop():
    jugador = Jugador(375, 500)
    tiempo_total = 60  # 60 segundos sera lo que dure el juego
    tiempo_inicial = pygame.time.get_ticks()
    enemigos = crear_enemigos(10, 3)  # Crear 10 enemigos con velocidad inicial de 3
    resultado = None
    running = True
    
    while running:
        screen.fill(color_negro)
        
        # Aqui definimos el temporizador que le diral al juego cuanto tiempo tiene que aguantar
        tiempo_actual = pygame.time.get_ticks()
        tiempo_restante = tiempo_total - (tiempo_actual - tiempo_inicial) // 1000
        
        if tiempo_restante <= 0:
            resultado = mostrar_opciones(screen, "¡Ganaste!", color_blanco, ["Jugar de nuevo (R)", "Salir (Q)"]) #Las opciones si ganamos
            if resultado == 'retry':
                return
            elif resultado == 'quit':
                pygame.quit()
                sys.exit()
        
        # Aqui lo mostramos de manera visual
        font = pygame.font.Font(None, 36)
        texto_tiempo = font.render(f"Tiempo restante: {tiempo_restante}s", True, color_blanco)
        screen.blit(texto_tiempo, (10, 10))
        
        # Aumentamos la velocidad del enemigo a medida que pasa el tiempo
        velocidad_actual = 3 + (60 - tiempo_restante) // 10
        
        # Se procesan las acciones
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Aqui los movimientos del jugador
        jugador.mover()
        jugador.draw(screen)
        
        # En este otro los del enemigo
        for enemigo in enemigos:
            enemigo.speed = velocidad_actual
            enemigo.mover()
            enemigo.draw(screen)

            # Verificamos las colisiones
            if colision(jugador, enemigo):
                resultado = mostrar_opciones(screen, "¡Perdiste!", color_rojo, ["Reintentar (R)", "Salir (Q)"])
                if resultado == 'retry':
                    return
                elif resultado == 'quit':
                    pygame.quit()
                    sys.exit()
        
        # Se actualiza la pantalla
        pygame.display.flip()
        clock.tick(60)
    
    # Salimos del juego
    pygame.quit()
    sys.exit()

# Muestra pantalla de inicio
pantalla_inicio()

# Iniciar el juego en un bucle hasta que el jugador decida salir
while True:
    game_loop()