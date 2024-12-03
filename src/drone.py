from globals import *
from message import Message
import pygame
import numpy as np
from typing import Tuple, List
from copy import deepcopy
import numpy as np
from uav import UAV


class Drone(UAV):
    def __init__(self, n_neighbors = 2):
        super().__init__()

        self.buffer_msg_in: List[Message] = list()
        self.buffer_msg_out: List[Message] = list()
        self.neighbors: List[UAV] = list()
        self.target = None
        self.active = False
        self.direction = (0, 0, 0)
        self.base_position = np.array(self.position)
        self.n_neighbors = n_neighbors

    def goto(self, position: Tuple[float, float, float]):
        self.target = position
        self.active = True

        diff = np.array(self.target) - np.array(self.position)
        magnitude = np.linalg.norm(diff)

        if magnitude > 0:
            self.direction = tuple(diff / magnitude)
        else:
            self.direction = (0, 0, 0)

    def update(self):
        self._handle_receive_msg()

        if self.active and self.target:
            # Move em direção ao alvo
            new_position = np.array(self.position) + np.array(self.direction) * self.velocity

            if np.linalg.norm(np.array(self.target) - new_position) <= self.velocity:
                self.position = self.target
                self.active = False
                self.direction = (0, 0, 0)
            else:
                self.position = (new_position[0], new_position[1], new_position[2])

        else:
            pass
            # # Pequenos movimentos aleatórios quando não está ativo
            # deslocamento = np.array([
            #     np.random.uniform(-0.2, 0.2),  # Movimento aleatório suave no eixo X
            #     np.random.uniform(-0.2, 0.2),  # Movimento aleatório suave no eixo Y
            #     0  # Mantém o eixo Z fixo
            # ])
            # nova_posicao = np.array(self.position) + deslocamento

            # # Restringe o movimento ao redor da posição média
            # limite = 2.0  # Distância máxima permitida
            # if np.linalg.norm(nova_posicao - self.base_position) <= limite:
            #     self.position = tuple(nova_posicao)
            # else:
            #     # Ajusta para ficar dentro do limite
            #     direcao_retorno = self.base_position - nova_posicao
            #     direcao_retorno /= np.linalg.norm(direcao_retorno)
            #     self.position = tuple(self.position + direcao_retorno * 0.1)


    def send_msg(self, msg: Message):
        msg.source_id = self.id

        for neighbor_id in self.neighbors:
            _msg = deepcopy(msg)
            _msg.destinated_id = neighbor_id
            
            self.buffer_msg_out.append(_msg)

    
    def clear_buffer_msg_out(self):
        self.buffer_msg_out = list()


    def _handle_receive_msg(self):
        if len(self.buffer_msg_in) > 0 and len(self.neighbors) > 0:

            for msg in self.buffer_msg_in:

                if msg.type == "discover":
                    distance = self.distance_target(msg.position)
                    print(f"Drone {self.id} recebeu mensagem de descoberta de {msg.source_id} com distância {distance}")
                    _msg = deepcopy(msg)

                    if distance < msg.distance:
                        for neighbor in self.neighbors:

                            if neighbor.id != msg.source_id:
                                _msg.source_id = self.id
                                _msg.destination_id = neighbor.id
                                _msg.distance = distance
                                _msg.closest_uav_id = self.id
                                neighbor.buffer_msg_in.append(_msg)

                    else:
                        for neighbor in self.neighbors:
                            _msg.source_id = self.id
                            _msg.destination_id = neighbor.id
                            neighbor.buffer_msg_in.append(_msg)

            self._clear_buffer_msg_in()


    def _clear_buffer_msg_in(self):
        self.buffer_msg_in = list()


    def draw(self, screen: pygame.Surface):
        x = int((self.position[0] + LARGURA) * 0.5)
        y = int((self.position[1] + ALTURA) * 0.5)

        color = RED if self.active else BLUE
        pygame.draw.circle(screen, color, (x, y), 5)


    def distance_target(self, position: Tuple[float, float, float]) -> float:
        return float(np.linalg.norm(np.array(self.position) - np.array(position)))
