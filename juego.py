import pygame
import sys

# Inicializar pygame y el mezclador de sonido
pygame.init()
pygame.mixer.init()

# Cargar y reproducir música de fondo
pygame.mixer.music.load("trapeaste conmigo.mp3")  # Asegúrate de tener este archivo
pygame.mixer.music.set_volume(0.5)  # Volumen entre 0.0 y 1.0
pygame.mixer.music.play(-1)  # Reproducir en bucle infinito

# Configuración de la pantalla
ANCHO, ALTO = 500, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego con Colisiones")

# Cargar imagen de fondo
fondo = pygame.image.load("fondo.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Cargar imagen de los personajes
imagen_personaje1 = pygame.image.load("personaje1.png")
imagen_personaje1 = pygame.transform.scale(imagen_personaje1, (100, 100))

imagen_personaje2 = pygame.image.load("personaje2.png")
imagen_personaje2 = pygame.transform.scale(imagen_personaje2, (100, 100))

# Fuente para texto
fuente = pygame.font.SysFont("Arial", 30)

# Clase para los jugadores
class Jugador:
    def __init__(self, x, y, imagen, controles):
        self.x = x
        self.y = y
        self.vida = 100
        self.velocidad = 5
        self.imagen = imagen
        self.controles = controles
        self.rect = pygame.Rect(self.x, self.y, imagen.get_width(), imagen.get_height())

    def mover(self, teclas):
        if teclas[self.controles["izquierda"]] and self.x > 0:
            self.x -= self.velocidad
        if teclas[self.controles["derecha"]] and self.x < ANCHO - self.imagen.get_width():
            self.x += self.velocidad
        if teclas[self.controles["arriba"]] and self.y > 0:
            self.y -= self.velocidad
        if teclas[self.controles["abajo"]] and self.y < ALTO - self.imagen.get_height():
            self.y += self.velocidad
        self.rect.topleft = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

# Clase para poderes (proyectiles)
class Poder:
    def __init__(self, x, y, direccion, color, velocidad=7, radio=5, daño=10):
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.velocidad = velocidad * direccion
        self.daño = daño
        self.rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio*2, self.radio*2)

    def mover(self):
        self.x += self.velocidad
        self.rect.topleft = (self.x - self.radio, self.y - self.radio)

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (self.x, self.y), self.radio)

    def fuera_de_pantalla(self):
        return self.x < 0 or self.x > ANCHO

# Función para dibujar la barra de vida
def dibujar_vida(jugador, x, y, color):
    pygame.draw.rect(pantalla, (255, 0, 0), (x, y, 100, 10))  # Fondo rojo
    pygame.draw.rect(pantalla, color, (x, y, max(0, jugador.vida), 10))  # Vida restante

# Crear jugadores
jugador1 = Jugador(ANCHO // 4, ALTO // 2, imagen_personaje1, {
    "izquierda": pygame.K_a,
    "derecha": pygame.K_d,
    "arriba": pygame.K_w,
    "abajo": pygame.K_s
})

jugador2 = Jugador(3 * ANCHO // 4, ALTO // 2, imagen_personaje2, {
    "izquierda": pygame.K_LEFT,
    "derecha": pygame.K_RIGHT,
    "arriba": pygame.K_UP,
    "abajo": pygame.K_DOWN
})

# Listas para poderes activos
poderes_jugador1 = []
poderes_jugador2 = []

# Función para manejar colisiones entre jugadores
def manejar_colisiones(jugador1, jugador2):
    if jugador1.rect.colliderect(jugador2.rect):
        if jugador1.x < jugador2.x:
            jugador1.x -= 5
            jugador2.x += 5
        else:
            jugador1.x += 5
            jugador2.x -= 5
        if jugador1.y < jugador2.y:
            jugador1.y -= 5
            jugador2.y += 5
        else:
            jugador1.y += 5
            jugador2.y -= 5
        jugador1.rect.topleft = (jugador1.x, jugador1.y)
        jugador2.rect.topleft = (jugador2.x, jugador2.y)

# Bucle principal del juego
clock = pygame.time.Clock()
ejecutando = True
while ejecutando:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    jugador1.mover(teclas)
    jugador2.mover(teclas)

    # Lanzar poderes del Jugador 1
    if teclas[pygame.K_f]:
        poderes_jugador1.append(Poder(jugador1.x + 50, jugador1.y + 25, 1, (0, 255, 255)))
    if teclas[pygame.K_g]:
        poderes_jugador1.append(Poder(jugador1.x + 50, jugador1.y + 25, 1, (255, 165, 0), velocidad=4, radio=8, daño=20))

    # Lanzar poderes del Jugador 2
    if teclas[pygame.K_SPACE]:
        poderes_jugador2.append(Poder(jugador2.x, jugador2.y + 25, -1, (255, 0, 255)))
    if teclas[pygame.K_RSHIFT]:
        poderes_jugador2.append(Poder(jugador2.x, jugador2.y + 25, -1, (0, 255, 0), velocidad=10, radio=3, daño=5))

    manejar_colisiones(jugador1, jugador2)

    # Dibujar fondo
    pantalla.blit(fondo, (0, 0))

    # Mover, dibujar y verificar colisiones de los poderes
    for poder in poderes_jugador1[:]:
        poder.mover()
        poder.dibujar(pantalla)
        if poder.fuera_de_pantalla():
            poderes_jugador1.remove(poder)
        elif poder.rect.colliderect(jugador2.rect):
            jugador2.vida -= poder.daño
            poderes_jugador1.remove(poder)

    for poder in poderes_jugador2[:]:
        poder.mover()
        poder.dibujar(pantalla)
        if poder.fuera_de_pantalla():
            poderes_jugador2.remove(poder)
        elif poder.rect.colliderect(jugador1.rect):
            jugador1.vida -= poder.daño
            poderes_jugador2.remove(poder)

    # Dibujar jugadores
    jugador1.dibujar(pantalla)
    jugador2.dibujar(pantalla)

    # Dibujar barras de vida
    dibujar_vida(jugador1, 20, 20, (0, 200, 0))
    dibujar_vida(jugador2, ANCHO - 120, 20, (0, 200, 0))

    # Verificar si alguien ganó
    if jugador1.vida <= 0 or jugador2.vida <= 0:
        texto = "¡Jugador 2 gana!" if jugador1.vida <= 0 else "¡Jugador 1 gana!"
        mensaje = fuente.render(texto, True, (255, 255, 0))
        pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2 - 20))
        pygame.display.update()
        pygame.time.delay(3000)
        ejecutando = False

    pygame.display.update()

# Detener la música y cerrar Pygame
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
