import pygame
from time import sleep
import numpy as np
from drone import Drone
from baseStationControl import BaseStationControl
from hacker import Hacker
from adhoc import AdHoc
from globals import *
from encryption import *


##################### SETTINGS #####################
n_drones = 6
attack = True # Replay attack
use_nounce = True # Defesa contra Replay Attack
logs = True
#####################################################

def main():
    pygame.init()
    SCREEN = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Flying Ad Hoc Network (FANET)")

    _font = pygame.font.match_font('Droid Sans Mono') 
    font = pygame.font.Font(_font, 30)

    symmetric_key = generate_symmetric_key()

    base_station_0 = BaseStationControl(position=(-LARGURA * 0.9, -ALTURA * 0.9, 0), symmetric_key=symmetric_key)
    hacker_0 = Hacker(position=(LARGURA * 0.75, ALTURA * 0.8, 0), attack=attack)
    drones = [Drone(symmetric_key=symmetric_key, use_nounce = use_nounce) for _ in range(n_drones)]

    # Inicializa a rede FANET
    fanet = AdHoc(symmetric_key=symmetric_key, logs=logs)
    fanet.add_bsc([base_station_0])
    fanet.add_drone(drones)
    fanet.add_hacker([hacker_0])

    base_station_0.send_msg((LARGURA * np.random.uniform(-1, 1), -ALTURA * np.random.uniform(-1, 1), 10), "discover")

    clock = pygame.time.Clock()
    RUNNING = True
    PAUSED = True

    while RUNNING:
        delta_time = clock.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                RUNNING = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    PAUSED = not PAUSED

        if not PAUSED:
            SCREEN.fill(BLACK)
            fanet.update(delta_time)
            fanet.draw(SCREEN)

            if fanet.bsc[0].mission_id is None:
                sleep(1)
                base_station_0.send_msg((LARGURA * np.random.uniform(-1, 1), -ALTURA * np.random.uniform(-1, 1), 10), "discover")

        else:
            pause_text = font.render("Paused. Press Space to continue.", True, (255, 255, 255))
            SCREEN.blit(pause_text, (LARGURA // 2 - pause_text.get_width() // 2, ALTURA // 2 - pause_text.get_height() // 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
