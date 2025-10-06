import pygame, random, sys

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("EcoRunner")
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 40)
fuente_titulo = pygame.font.Font(None, 70)

# Función para mostrar texto centrado
def mostrar_texto(texto, fuente, color, y):
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(ANCHO // 2, y))
    pantalla.blit(render, rect)

# Pantalla de inicio
def pantalla_inicio():
    en_inicio = True
    while en_inicio:
        pantalla.fill((180, 255, 180))
        mostrar_texto("EcoRunner", fuente_titulo, (0, 100, 0), 120)
        mostrar_texto("Ayuda al planeta esquivando la contaminación", fuente, (0, 0, 0), 200)
        mostrar_texto("Usa ↑ para saltar obstáculos.", fuente, (0, 0, 0), 260)
        mostrar_texto("Presioná ESPACIO para comenzar", fuente, (0, 100, 0), 320)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                en_inicio = False

        pygame.display.flip()
        reloj.tick(30)

# Pantalla de Game Over
def pantalla_game_over(puntaje):
    en_game_over = True
    while en_game_over:
        pantalla.fill((255, 200, 200))
        mostrar_texto(" GAME OVER ", fuente_titulo, (150, 0, 0), 120)
        mostrar_texto(f"Puntaje final: {puntaje}", fuente, (0, 0, 0), 200)
        mostrar_texto("Presioná R para reiniciar o ESC para salir", fuente, (50, 50, 50), 280)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    juego()
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        reloj.tick(30)

# Juego principal
def juego():
    jugador = pygame.Rect(100, 300, 40, 40)
    salto = False
    velocidad_salto = 0
    obstaculos = []
    puntos = 0
    vidas = 3

    corriendo = True
    while corriendo:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and not salto:
                salto = True
                velocidad_salto = -15

        # Movimiento del salto
        if salto:
            jugador.y += velocidad_salto
            velocidad_salto += 1
            if jugador.y >= 300:
                jugador.y = 300
                salto = False

        # Generar obstáculos
        if random.randint(1, 50) == 1:
            obstaculos.append(pygame.Rect(800, 320, 20, 30))

        # Mover obstáculos y detectar colisiones
        for o in list(obstaculos):
            o.x -= 8
            if o.x < 0:
                obstaculos.remove(o)
                puntos += 1

            if jugador.colliderect(o):
                vidas -= 1
                obstaculos.remove(o)
                if vidas <= 0:
                    pantalla_game_over(puntos)

        # Dibujar fondo y elementos
        pantalla.fill((200, 255, 200))
        pygame.draw.rect(pantalla, (0, 200, 0), jugador)
        for o in obstaculos:
            pygame.draw.rect(pantalla, (80, 80, 80), o)

        # Mostrar puntos y vidas
        texto_puntos = fuente.render(f"Puntos: {puntos}", True, (0, 0, 0))
        pantalla.blit(texto_puntos, (10, 10))
        texto_vidas = fuente.render(f"Vidas: {vidas}", True, (0, 0, 0))
        pantalla.blit(texto_vidas, (10, 50))

        pygame.display.flip()
        reloj.tick(30)

# Iniciar el juego
pantalla_inicio()
juego()
