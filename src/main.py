import pygame
from drone import Drone
from baseStationControl import BaseStationControl
from adhoc import AdHoc
from globals import *

fanet = AdHoc()

drone_0 = Drone()
drone_1 = Drone()
drone_2 = Drone()
drone_3 = Drone()
drone_4 = Drone()
drone_5 = Drone()
drone_6 = Drone()
drone_7 = Drone()
drone_8 = Drone()
drone_9 = Drone()
drone_10 = Drone()
drone_11 = Drone()
drone_12 = Drone()

base_station_0 = BaseStationControl(position=(-LARGURA * 0.9, -ALTURA * 0.9, 0))
base_station_1 = BaseStationControl(position=(LARGURA * 0.9, ALTURA * 0.9, 0))

fanet.add_drone([drone_0, drone_1, drone_2, drone_3, drone_4, drone_5, drone_6, drone_7, drone_8, drone_9, drone_10, drone_11, drone_12])
fanet.add_bsc([base_station_0, base_station_1])

base_station_0.send_msg((0, 0, 0), "discover")
drone_0.goto((0, 0, 10))


# Configuração do pygame
pygame.init()
SCREEN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flying Ad Hoc Network (FANET)")

# Loop principal
def main():
    clock = pygame.time.Clock()
    RUNNING = True
    PAUSED = False

    while RUNNING:
        delta_time = clock.tick(FPS) / 1000.0  # Tempo decorrido em segundos

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                RUNNING = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # Alterna entre pausado e rodando
                    PAUSED = not PAUSED

        if not PAUSED:
            # Atualiza e desenha apenas se não estiver pausado
            SCREEN.fill(BLACK)
            fanet.update()
            fanet.draw(SCREEN)
        else:
            # Mensagem na tela enquanto pausado
            font = pygame.font.Font(None, 30)
            pause_text = font.render("Paused. Press Space to continue.", True, (255, 255, 255))
            SCREEN.blit(pause_text, (LARGURA // 2 - pause_text.get_width() // 2, ALTURA // 2 - pause_text.get_height() // 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
