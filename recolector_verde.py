# recolector_verde.py
import pygame
import random

pygame.init()
ANCHO, ALTO = 600, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Recolector Verde")
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 36)

# Colores
VERDE = (0, 200, 0)
MARRON = (100, 50, 0)
CELESTE = (135, 206, 235)
NEGRO = (0, 0, 0)

jugador = pygame.Rect(300, 200, 40, 40)
basuras = [pygame.Rect(random.randint(20, ANCHO - 40),
                       random.randint(20, ALTO - 40), 20, 20)
           for _ in range(5)]

puntos = 0
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: jugador.x -= 5
    if teclas[pygame.K_RIGHT]: jugador.x += 5
    if teclas[pygame.K_UP]: jugador.y -= 5
    if teclas[pygame.K_DOWN]: jugador.y += 5

    jugador.x = max(0, min(ANCHO - jugador.width, jugador.x))
    jugador.y = max(0, min(ALTO - jugador.height, jugador.y))

    for b in basuras[:]:
        if jugador.colliderect(b):
            puntos += 1
            basuras.remove(b)
            basuras.append(pygame.Rect(random.randint(20, ANCHO - 40),
                                       random.randint(20, ALTO - 40), 20, 20))
            print(" ¡El planeta te lo agradece!")

    # Dibujar
    pantalla.fill(CELESTE)
    for b in basuras:
        pygame.draw.rect(pantalla, MARRON, b)
    pygame.draw.rect(pantalla, VERDE, jugador)

    # Estadísticas ecológicas
    co2_ev = round(puntos * 0.12, 2)
    texto = fuente.render(f"Puntos: {puntos}", True, NEGRO)
    texto2 = fuente.render(f"CO₂ evitado: {co2_ev} kg", True, NEGRO)
    pantalla.blit(texto, (10, 10))
    pantalla.blit(texto2, (10, 40))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
