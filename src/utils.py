import pygame
from typing import List
from globals import *

def draw_logs(screen: pygame.Surface, logs: List[str]):

    log_bar_height = 100
    log_bar_color = (30, 30, 30)  # Cinza escuro
    text_color = (255, 255, 255)  # Branco

    # Desenha a faixa
    pygame.draw.rect(screen, log_bar_color, (0, ALTURA - log_bar_height, LARGURA, log_bar_height))

    # Renderiza os logs
    font = pygame.font.Font(None, 24)
    for i, log in enumerate(logs):
        text_surface = font.render(log, True, text_color)
        screen.blit(text_surface, (10, ALTURA - log_bar_height + 10 + i * 20))  # Ajuste de espaçamento
