from globals import *
from message import Message
import pygame
import numpy as np
from typing import Tuple, List
from copy import deepcopy
import numpy as np
from uav import UAV
from baseStationControl import BaseStationControl


class Drone(UAV):
    def __init__(self, n_neighbors = 2):
        super().__init__()

        self.buffer_msg_in: List[Message] = list()
        self.buffer_msg_out: List[Message] = list()
        self.neighbors: List[UAV] = list()
        self.bsc: List[BaseStationControl] = list()
        self.target = None
        self.active = False
        self.direction = (0, 0, 0)
        self.base_position = np.array(self.position)
        self.n_neighbors = n_neighbors
        self.closest_uav_id: UAV | None = None
        self.closest_distance: float | None = None
        self.current_mission_id = -1
        self.timeout = 50
        self.current_timeout = 0
        self.is_discover = False
        self.saw_execute = False
        self.limit_spread = 0.1

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
        self._handle_move()
        self._handle_discover()


    def _handle_discover(self):
        if self.is_discover:
            self.current_timeout += 1

            if self.current_timeout >= self.timeout:
                self.is_discover = False
                self.saw_execute = False
                self.current_timeout = 0
                self.closest_distance = float(np.inf)

                if len(self.bsc) > 0:
                    self.send_msg_to_bsc()


    def send_msg(self, msg: Message):
        msg.source_id = self.id

        for neighbor_id in self.neighbors:
            _msg = deepcopy(msg)
            _msg.destinated_id = neighbor_id
            
            self.buffer_msg_out.append(_msg)


    def send_msg_to_bsc(self):
        for bsc in self.bsc:
            msg = Message((0, 0, 0), type="return")
            msg.source_id = self.id
            msg.destination_id = bsc.id
            msg.position = self.position
            msg.mission_id = self.current_mission_id
            msg.closest_uav_id = self.closest_uav_id
            msg.distance = self.closest_distance
            self.buffer_msg_out.append(msg)


    def clear_buffer_msg_out(self):
        self.buffer_msg_out = list()


    def _handle_receive_msg(self):
        if len(self.buffer_msg_in) > 0 and len(self.neighbors) > 0:

            for msg in self.buffer_msg_in:

                if self.current_mission_id < msg.mission_id:
                    self.current_mission_id = msg.mission_id
                    self.current_timeout = 0
                    self.is_discover = True
                    self.closest_distance = float(np.inf)

                # print(f"Drone {self.id} recebeu mensagem de {msg.source_id} com distância {msg.distance} | Menor distância registrada: {self.closest_distance}")
                if self.closest_distance != float(np.inf) and self.closest_distance <= msg.distance:
                    continue

                if msg.type == "discover":

                    if self.closest_distance == float(np.inf):
                        self.closest_distance = self.distance_target(msg.position)
                    
                    _msg = deepcopy(msg)

                    if self.closest_distance + self.limit_spread < msg.distance:
                        self.closest_uav_id = self.id

                        for neighbor in self.neighbors:
                            # print(f"[Caso 1] Drone {self.id} enviando mensagem para {neighbor.id}")
                            self.closest_uav_id = self.id

                            _msg.source_id = self.id
                            _msg.destination_id = neighbor.id
                            _msg.distance = self.closest_distance
                            _msg.closest_uav_id = self.id
                            neighbor.buffer_msg_in.append(_msg)

                    else:
                        for neighbor in self.neighbors:
                            
                            if neighbor.id != msg.source_id:
                                # print(f"[Caso 2] Drone {self.id} enviando mensagem para {neighbor.id}")
                                self.closest_uav_id = msg.source_id
                                self.closest_distance = msg.distance

                                _msg.source_id = self.id
                                _msg.destination_id = neighbor.id
                                neighbor.buffer_msg_in.append(_msg)

                elif msg.type == "execute":
                    print(f"Drone {self.id} recebeu mensagem TYPE EXECUTE de {msg.source_id} | shortest uav: {msg.closest_uav_id}")
                    if self.saw_execute:
                        continue

                    else:
                        self.saw_execute = True


                    if msg.closest_uav_id == self.id:
                        print(f"Drone {self.id} executa mensagem TYPE EXECUTE de {msg.source_id} | position: {msg.position} | shortest uav: {msg.closest_uav_id}")
                        self.goto(msg.position)

                    else:
                        _msg = deepcopy(msg)

                        for neighbor in self.neighbors:
                            
                            if neighbor.id != msg.source_id:
                                print(f"[Caso 3] Drone {self.id} transmite mensagem TYPE EXECUTE para {neighbor.id} | shortest uav: {msg.closest_uav_id}")
                                _msg.source_id = self.id
                                _msg.destination_id = neighbor.id
                                neighbor.buffer_msg_in.append(_msg)

            self._clear_buffer_msg_in()


    def _clear_buffer_msg_in(self):
        self.buffer_msg_in = list()


    def _handle_move(self):
        if self.active and self.target:
            # Move em direção ao alvo
            new_position = np.array(self.position) + np.array(self.direction) * self.velocity

            if np.linalg.norm(np.array(self.target) - new_position) <= self.velocity:
                self.position = self.target
                self.active = False
                self.direction = (0, 0, 0)
            else:
                self.position = (new_position[0], new_position[1], new_position[2])

        # else:
        #     # Pequenos movimentos aleatórios quando não está ativo
        #     deslocamento = np.array([
        #         np.random.uniform(-0.2, 0.2),  # Movimento aleatório suave no eixo X
        #         np.random.uniform(-0.2, 0.2),  # Movimento aleatório suave no eixo Y
        #         0  # Mantém o eixo Z fixo
        #     ])
        #     nova_posicao = np.array(self.position) + deslocamento

        #     # Restringe o movimento ao redor da posição média
        #       # Distância máxima permitida
        #     if np.linalg.norm(nova_posicao - self.base_position) <= self.limit_spread:
        #         self.position = tuple(nova_posicao)
        #     else:
        #         # Ajusta para ficar dentro do self.limit_spread
        #         direcao_retorno = self.base_position - nova_posicao
        #         direcao_retorno /= np.linalg.norm(direcao_retorno)
        #         self.position = tuple(self.position + direcao_retorno * 0.1)


    def draw(self, screen: pygame.Surface):
        x = int((self.position[0] + LARGURA) * 0.5)
        y = int((self.position[1] + ALTURA) * 0.4)

        color = RED if self.active else BLUE
        pygame.draw.circle(screen, color, (x, y), 5)


    def distance_target(self, position: Tuple[float, float, float]) -> float:
        return float(np.linalg.norm(np.array(self.position) - np.array(position)))
