"""
Fernando López Gómez
Si necesitas ayuda, usa el IDLE de python, no la terminal
"""
import pygame
import os
import math
import random
from pygame import mixer #para poder agregar música

#Inicializar pygame
pygame.init()

#Creamos la ventana del juego
ancho = 800
alto = 700
screen = pygame.display.set_mode((ancho,alto))

#Titulo, ícono  y fondo del juego. #Para las imágenes puedes usar https://www.flaticon.com/

pygame.display.set_caption("Space Invaders Game")    
icon = pygame.image.load(os.path.join("Imagenes",'ufo.png'))
BG = pygame.transform.scale(pygame.image.load(os.path.join("Imagenes",'fondo.png')),(ancho,alto))#Para ajustar el tamaño de la imagen 

pygame.display.set_icon(icon)

#Sonido de fondo
mixer.music.load(os.path.join("sounds",'backgroundwav.wav')) #se cargan mas rápido en wav. Existen convertidores en internet
mixer.music.play(-1) #This Loops the song

#Jugador
playerImg = pygame.transform.scale(pygame.image.load(os.path.join("Imagenes",'player.png')),(70,70))
playerX = 370
playerY = 550

#Puntaje
score_value = 0
font = pygame.font.SysFont("comicsans", 50)
#font = pygame.font.Font('freesansbold.ttf', 32) #.ttf es una extensión y 32 es el tamaño
"""
freesansbold es la única fuente incluida en pygame, para obtener más fuentes, puedes descargarlas desde el link dentro de la carpeta en donde estes manejando
este archivo
Link: https://www.dafont.com/pt/
Si te soy sincero a este punto no sé cuál es la diferencia entre .Font y .SysFont
"""
textX = 10
textY = 10

#Enemigos
enemyImg = pygame.transform.scale(pygame.image.load(os.path.join("Imagenes",'enemy.png')),(60,60))
enemyX = random.randint(0, 740)
enemyY = random.randint(0, 490) #A partir del 550 es la zona de spawn del jugador, por lo que el enemigo debe estar 60 pixeles antes
enemyX_change = 0.3
enemyY_change = 10

#Láser
laserImg = pygame.transform.scale(pygame.image.load(os.path.join("Imagenes",'laser.png')),(60,60))
laserX = 0      
laserY = 550
laserX_change = 0
laserY_change = 1
#laser state: "Ready" para cuando está lista para ser disparada
#"Fire" para cuando esté en movimiento
laser_state = "Ready"

#Juego terminado
fontGO = pygame.font.Font('freesansbold.ttf', 62)
textGOX = 250
textGOY = 300


def show_score (x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255) ) #render es para mostrar el texto en la pantalla 
    screen.blit(score, (x, y))  
    
def game_over():
    txt = fontGO.render("Game Over", True, (255, 255, 255))
    #screen.blit(txt, (x, y)) #este es para que reciba variables. Como son constantes, no necesitamos argumentos
    screen.blit(txt, (textGOX, textGOY)) #Dejamos este porque el valor de la ubicación no cambia
    
def jugador (x,y) :
    screen.blit(playerImg, (x, y))


def enemigos (x,y) :
    screen.blit(enemyImg, (x, y))
    
def fire_laser (x,y) :
    global laser_state
    laser_state = "Fire"
    screen.blit(laserImg, (x + 5 , y)) #El +5 es para que el láser salga del centro de la nave

def Colision (x2, y2, x1, y1):
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2)) #Fórmula de la distancia entre 2 puntos
    if distance < 27:
        return True
    else:
        return False

#Game Loop
run = True
while run:
    #screen.fill((0, 0, 0)) #RGB- Red, green, blue. Este se usa en caso de que quieras un color sólido
    screen.blit(BG,(0, 0)) # Se usa para poner una imagen de fondo
    """
    BG es la imagen a usar. (Le puse BG por background)
    (0,0) son las coordenadas en donde empezar a dibujar la imagen. En pygame el punto (0,0) es el punto superior izquierdo de la pantalla
    por lo que al aumentar en el eje x se mueve a la izquierda y al aumentar en el eje y se mueve hacia abajo
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Si se quiere salir del juego, entonces salte del while
            run = False
            
        """ 
        Puedes probar el siguiente código para que te des una idea de cómo funciona el lector del teclado
        
        if event.type == pygame.KEYDOWN: #Si una tecla está siendo presionada
            print("Se ha presionado una tecla")
            if event.key == pygame.K_LEFT: #Si la tecla presionada es la flecha izq
                print("Se está presionando la flecha izquierda")
            if event.key == pygame.K_RIGHT: #Si la tecla presionada es la flecha der
                print("Se está presionando la flecha derecha")
        
        if event.type == pygame.KEYUP: #Si una tecla presionada sube (Es decir, se deja de presionar)
            print("La tecla se ha dejado de presionar")
        """
        
        #Movimiento del jugador: Movemos 0.5 pixeles dependiendo de la coordenada
        playerX_change = 0
        playerY_change = 0
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT: 
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT: 
                playerX_change = 0.5
            if event.key == pygame.K_UP: 
                playerY_change = -0.5
            if event.key == pygame.K_DOWN: 
                playerY_change = 0.5
            #Para el láser
            if event.key == pygame.K_SPACE: 
                if laser_state is "Ready": #Para sólo disparar cuando esté lista
                    laserX = playerX
                    laserY = playerY
                    fire_laser(laserX, laserY)
                    laser_sound = mixer.Sound(os.path.join("sounds",'laser.wav')) #En este caso el audio es muy corto, entonces se usa el .sound
                    laser_sound.play()
        
        if event.type == pygame.KEYUP: 
            pass      
    
            
            
            
    
    playerX += playerX_change
    playerY += playerY_change
    
    #Definimos los límites del jugador
    """ La pantalla tiene 800 pixeles de largo, entonces el eje x va desde 0 hasta 800.
    Previamente definimos que la figura del jugador será de 70 x 70 pixeles, entonces, si python dibuja las figuras desde
    la esquina superior izquierda, necesitamos un límite de 70 pixeles antes del borde de la pantalla para que la figura no se corte"""
    #Para los límites Derecho e izquierdo
    if playerX <= 0:
        playerX = 0
    elif playerX >= 730:
        playerX = 730
    #Para límites Superior e inferior
    if playerY <= 0:
        playerY = 0
    elif playerY >= 630:
        playerY = 630
        
        
    #Movimiento del enemigo
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 0.3
        enemyY += enemyY_change #Lo ponemos dentro del if para que sólo se ejecute 1 vez dada la condición
    elif enemyX >= 740:
        enemyX_change = -0.3
        enemyY += enemyY_change
    elif enemyY > 490:
        enemyY = 2000
        game_over()
        
    
    
    #Movimiento del láser
    if laser_state is "Fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change #Recordando que hacia arriba disminuye y
    
    if laserY <= 0: #Recargando el láser
        laserY = 550
        laser_state = "Ready"
    
    #Evaluar las colisiones
    choque = Colision(enemyX, enemyY, laserX, laserY)
    if choque:
        laserY = 550 #Recargamos el Láser
        laser_state = "Ready"
        score_value += 1
        #Respawneamos el enemigo
        enemyX = random.randint(0, 740)
        enemyY = random.randint(0, 490)
    
    choche_contra_enemigo = Colision(enemyX, enemyY, playerX, playerY)
    if choche_contra_enemigo:
        enemyY = 2000
        game_over()
    
    
    jugador(playerX, playerY)
    enemigos(enemyX, enemyY)
    show_score(textX, textY)

    
    pygame.display.update()




