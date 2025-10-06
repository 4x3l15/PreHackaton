# stop_co.py
import pygame
import random

pygame.init()
ANCHO, ALTO = 600, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Stop CO Challenge")
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 60)

auto = pygame.Rect(300, 350, 50, 30)
humo = pygame.Rect(random.randint(0, 580), 0, 20, 20)
puntos = 0
vel_humo = 5
max_puntos = 10
corriendo = True
final = False

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: auto.x -= 6
    if teclas[pygame.K_RIGHT]: auto.x += 6

    auto.x = max(0, min(ANCHO - auto.width, auto.x))

    if not final:
        humo.y += vel_humo
        if humo.y > ALTO:
            humo.y = 0
            humo.x = random.randint(0, 580)
            puntos += 1
            if puntos % 3 == 0:  # sube dificultad
                vel_humo += 1

        if auto.colliderect(humo):
            print("💨 ¡Contaminación detectada!")
            puntos = 0
            vel_humo = 5

        if puntos >= max_puntos:
            final = True
            co2_ev = round(puntos * 0.12, 2)
            print(f"🎉 ¡Has reducido {co2_ev} kg de CO₂! 🌱")

    pantalla.fill((180, 220, 255))
    pygame.draw.rect(pantalla, (0, 255, 0), auto)
    pygame.draw.rect(pantalla, (80, 80, 80), humo)

    if not final:
        texto = fuente.render(f"Puntos: {puntos}", True, (0, 0, 0))
        pantalla.blit(texto, (10, 10))
        co2 = round(puntos * 0.12, 2)
        pantalla.blit(fuente.render(f"CO₂ evitado: {co2} kg", True, (0, 0, 0)), (10, 40))
    else:
        msg = fuente_grande.render("¡META ALCANZADA!", True, (10, 100, 10))
        sub = fuente.render(f"Has reducido {round(puntos * 0.12, 2)} kg de CO₂ 🌍", True, (0, 0, 0))
        pantalla.blit(msg, (ANCHO // 2 - msg.get_width() // 2, 150))
        pantalla.blit(sub, (ANCHO // 2 - sub.get_width() // 2, 230))

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
