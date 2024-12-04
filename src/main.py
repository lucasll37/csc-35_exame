import pygame
from time import sleep
import numpy as np
from drone import Drone
from hacker import Hacker
from baseStationControl import BaseStationControl
from adhoc import AdHoc
from globals import *
from encryption import *


n_drones = 6
symmetric_key = generate_symmetric_key()

base_station_0 = BaseStationControl(position=(-LARGURA * 0.9, -ALTURA * 0.9, 0), symmetric_key=symmetric_key)
drones = [Drone(symmetric_key=symmetric_key) for _ in range(n_drones)]
hackers = [Hacker(symmetric_key=symmetric_key)]

# Inicializa a rede FANET
fanet = AdHoc(logs=True)
fanet.add_bsc([base_station_0])
fanet.add_drone(drones)
# fanet.add_drone(hackers)

# Loop principal
def main():
    pygame.init()
    SCREEN = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Flying Ad Hoc Network (FANET)")

    base_station_0.send_msg((LARGURA * np.random.uniform(-1, 1), -ALTURA * np.random.uniform(-1, 1), 10), "discover")

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
            SCREEN.fill(BLACK)
            PAUSED = fanet.update(delta_time)
            PAUSED = fanet.draw(SCREEN) or PAUSED

            PAUSED = False # debug

            if fanet.bsc[0].mission_id is None:
                sleep(1)
                base_station_0.send_msg((LARGURA * np.random.uniform(-1, 1), -ALTURA * np.random.uniform(-1, 1), 10), "discover")

        else:
            # Mensagem na tela enquanto pausado
            font = pygame.font.Font(None, 30)
            pause_text = font.render("Paused. Press Space to continue.", True, (255, 255, 255))
            SCREEN.blit(pause_text, (LARGURA // 2 - pause_text.get_width() // 2, ALTURA // 2 - pause_text.get_height() // 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
