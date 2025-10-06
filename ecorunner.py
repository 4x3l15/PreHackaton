# ecorunner.py
import pygame
import random

pygame.init()
ANCHO, ALTO = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("EcoRunner 🌱")
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 40)
fuente_grande = pygame.font.Font(None, 70)

jugador = pygame.Rect(100, 300, 40, 40)
y_suelo = 300
salto = False
vel_salto = 0
obstaculos = []
puntos = 0
vel_obstaculos = 8
nivel = 1
spawn_rate = 40
estado = "inicio"  # inicio, jugando, final

def resetear():
    global jugador, salto, vel_salto, obstaculos, puntos, vel_obstaculos, nivel, spawn_rate
    jugador.x, jugador.y = 100, y_suelo
    salto = False
    vel_salto = 0
    obstaculos.clear()
    puntos = 0
    vel_obstaculos = 8
    nivel = 1
    spawn_rate = 40

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if e.type == pygame.KEYDOWN:
            if estado == "inicio" and e.key == pygame.K_SPACE:
                estado = "jugando"
            elif estado == "jugando" and e.key == pygame.K_SPACE and not salto:
                salto = True
                vel_salto = -15
            elif estado == "final" and e.key == pygame.K_r:
                resetear()
                estado = "inicio"

    if estado == "jugando":
        if salto:
            jugador.y += vel_salto
            vel_salto += 1
            if jugador.y >= y_suelo:
                jugador.y = y_suelo
                salto = False

        if random.randint(1, max(10, spawn_rate)) == 1:
            obstaculos.append(pygame.Rect(ANCHO, 320, 20, 30))

        for o in obstaculos[:]:
            o.x -= vel_obstaculos
            if o.x + o.width < 0:
                obstaculos.remove(o)
                puntos += 1

        for o in obstaculos:
            if jugador.colliderect(o):
                estado = "final"

        nuevo_nivel = puntos // 50 + 1
        if nuevo_nivel > nivel:
            nivel = nuevo_nivel
            vel_obstaculos += 2
            spawn_rate = max(10, spawn_rate - 6)

    pantalla.fill((200, 255, 200))
    pygame.draw.rect(pantalla, (100, 180, 100), (0, y_suelo + 40, ANCHO, 100))

    if estado == "inicio":
        titulo = fuente_grande.render("EcoRunner 🌎", True, (10, 80, 10))
        sub = fuente.render("Presiona ESPACIO para correr", True, (0, 0, 0))
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 120))
        pantalla.blit(sub, (ANCHO // 2 - sub.get_width() // 2, 200))

    elif estado == "jugando":
        pygame.draw.rect(pantalla, (0, 200, 0), jugador)
        for o in obstaculos:
            pygame.draw.rect(pantalla, (80, 80, 80), o)
        texto = fuente.render(f"Puntos: {puntos}  Nivel: {nivel}", True, (0, 0, 0))
        pantalla.blit(texto, (10, 10))
        co2 = round(puntos * 0.12, 2)
        pantalla.blit(fuente.render(f"CO₂ evitado: {co2} kg", True, (0, 0, 0)), (10, 40))

    elif estado == "final":
        co2 = round(puntos * 0.12, 2)
        msg = fuente_grande.render("¡Juego Terminado!", True, (120, 0, 0))
        eco = fuente.render(f"Has reducido {co2} kg de CO₂ 🌱", True, (0, 0, 0))
        reinicio = fuente.render("Presiona R para reiniciar", True, (0, 0, 0))
        pantalla.blit(msg, (ANCHO // 2 - msg.get_width() // 2, 100))
        pantalla.blit(eco, (ANCHO // 2 - eco.get_width() // 2, 180))
        pantalla.blit(reinicio, (ANCHO // 2 - reinicio.get_width() // 2, 240))

    pygame.display.flip()
    reloj.tick(60)
