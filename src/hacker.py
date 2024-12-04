from globals import *
from message import Message
from encryption import *
import pygame
import numpy as np
from typing import Tuple, List, Set, Optional
from copy import deepcopy
from uav import UAV
from baseStationControl import BaseStationControl


class Hacker(UAV):
    def __init__(self, symmetric_key: bytes | None, timeout = 200):
        super().__init__(symmetric_key=symmetric_key)

        self.buffer_msg_in: List[Message] = list()
        self.buffer_msg_out: List[Message] = list()
        self.neighbors: List[UAV] = list()
        self.bsc: List[BaseStationControl] = list()
        self.target: Tuple[float, float, float] = None
        self.active = False
        self.direction = (0, 0, 0)
        self.closest_uav_id: Optional[int] = None
        self.closest_distance: float = float('inf')
        self.current_mission_id = -1
        self.timeout = timeout
        self.current_timeout = 0
        self.saw_discover = False
        self.saw_execute = False
        self.saw_complete = False
        self.messages_seen: Set[int] = set()


    def goto(self, position: Tuple[float, float, float]):
        self.target = position
        self.active = True

        diff = np.array(self.target) - np.array(self.position)
        magnitude = np.linalg.norm(diff)

        if magnitude > 0:
            self.direction = tuple(diff / magnitude)
        else:
            self.direction = (0, 0, 0)

    def update(self, delta_time: float | None = None):
        self._handle_receive_msg(delta_time)
        self._handle_move(delta_time)
        self._handle_discover(delta_time)

    def _handle_discover(self, delta_time: float | None = None):
        if self.saw_discover :
            self.current_timeout += 1

            if self.current_timeout >= self.timeout:
                self.saw_discover = False
                self.saw_execute = False

                if len(self.bsc) > 0:
                    self.send_msg_to_bsc(type="return")

    def send_msg(self, msg: Message):
        msg.source_id = self.id

        for neighbor in self.neighbors:
            _msg = deepcopy(msg)
            _msg.source_id = self.id
            _msg.destination_id = neighbor.id
            _msg.mission_id = self.current_mission_id
            _msg.closest_uav_id = self.closest_uav_id

            self.buffer_msg_out.append(_msg)


    def send_msg_to_bsc(self, type: str):
        for bsc in self.bsc:
            msg = Message(self.target, type=type)
            msg.source_id = self.id
            msg.destination_id = bsc.id
            msg.mission_id = self.current_mission_id
            msg.closest_uav_id = self.closest_uav_id
            msg.distance = self.closest_distance
            self.buffer_msg_out.append(msg)
            

    def clear_buffer_msg_out(self):
        self.buffer_msg_out = list()

    def _handle_receive_msg(self, delta_time: float | None = None):
        if self.buffer_msg_in:

            for encrypted_msg in self.buffer_msg_in:
                msg = decrypt_object(self.symmetric_key, encrypted_msg)

                if self.current_mission_id < msg.mission_id:
                    self.current_mission_id = msg.mission_id
                    self.target = msg.position
                    self.current_timeout = 0
                    self.saw_discover = True
                    self.saw_execute = False
                    self.saw_complete = False
                    self.closest_distance = float('inf')


                if msg.type == "discover":
                    if self.closest_distance != float('inf') and self.closest_distance <= msg.distance:
                        continue

                    if self.closest_distance == float('inf'):
                        self.closest_distance = self.distance_target(msg.position)


                    if self.closest_distance < msg.distance:
                        self.closest_uav_id = self.id

                        for neighbor in self.neighbors:
                            _msg = deepcopy(msg)
                            _msg.source_id = self.id
                            _msg.destination_id = neighbor.id
                            _msg.distance = self.closest_distance
                            _msg.closest_uav_id = self.id
                            self.buffer_msg_out.append(_msg)
                    else:
                        for neighbor in self.neighbors:
                            _msg = deepcopy(msg)
                            if neighbor.id != msg.source_id:
                                self.closest_uav_id = msg.source_id
                                self.closest_distance = msg.distance

                                _msg.source_id = self.id
                                _msg.destination_id = neighbor.id
                                self.buffer_msg_out.append(_msg)

                elif msg.type == "execute":
                    if self.saw_execute:
                        continue
                    else:
                        self.saw_execute = True

                    if msg.closest_uav_id == self.id:
                        # print(f"Drone {self.id} executando missão {self.current_mission_id}")
                        self.goto(msg.position)

                    else:
                        for neighbor in self.neighbors:
                            _msg = deepcopy(msg)
                            if neighbor.id != msg.source_id:
                                # print(f"Drone {self.id} repassando missão {self.current_mission_id} para o drone {neighbor.id}")
                                _msg.source_id = self.id
                                _msg.destination_id = neighbor.id
                                self.buffer_msg_out.append(_msg)

                elif msg.type == "complete":
                    # print(f" {self.id} Entrou em complete")
                    if self.saw_complete:
                        # print(f"Eu sou o drone {self.id} e já vi a mensagem de complete")
                        continue
                    else:
                        self.saw_complete = True

                    if len(self.bsc) > 0:
                        # print(f"Drone {self.id} finalizando missão {self.current_mission_id} | Irei informar o BSC")
                        self.send_msg_to_bsc(type="finish")
                    else:
                        for neighbor in self.neighbors:
                            _msg = deepcopy(msg)
                            # if neighbor.id != msg.source_id:
                            # print(f"Drone {self.id} repassando finalização da missão {self.current_mission_id} para o drone {neighbor.id}")
                            _msg.source_id = self.id
                            _msg.destination_id = neighbor.id
                            self.buffer_msg_out.append(_msg)

            self._clear_buffer_msg_in()

    def _clear_buffer_msg_in(self):
        self.buffer_msg_in = list()

    def _handle_move(self, delta_time: float | None = None):
        if self.active and self.target:
            deslocamento = np.array(self.direction) * self.speed * delta_time
            new_position = np.array(self.position) + deslocamento

            if np.linalg.norm(np.array(self.target) - new_position) <= self.speed * delta_time:
                self.position = self.target
                self.active = False
                self.direction = (0, 0, 0)
                self.send_msg(Message(self.target, type="complete"))

                # print(f"Drone {self.id} chegou ao destino {self.target}")
                    
            else:
                self.position = (new_position[0], new_position[1], new_position[2])

    def draw(self, screen: pygame.Surface):
        x = int((self.position[0] + LARGURA) * 0.5)
        y = int((self.position[1] + ALTURA) * 0.5)

        pygame.draw.circle(screen, RED, (x, y), 5)

        if self.active:
            x = int((self.target[0] + LARGURA) * 0.5)
            y = int((self.target[1] + ALTURA) * 0.5)
            size = 5

            # Desenhar o "X" usando duas linhas cruzadas
            pygame.draw.line(screen, RED, (x - size, y - size), (x + size, y + size), 2)
            pygame.draw.line(screen, RED, (x - size, y + size), (x + size, y - size), 2)



    def distance_target(self, position: Tuple[float, float, float]) -> float:
        return float(np.linalg.norm(np.array(self.position) - np.array(position)))