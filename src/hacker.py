import pygame
import numpy as np
from copy import deepcopy
from encryption import *
from typing import Tuple, List, Dict
from globals import *
from message import Message
from drone import UAV


class Hacker():
    id = 0
    mission_id = 0

    def __init__(self, position: Tuple[float, float, float] | None = None, n_neighbors = 1, attack = False):

        if position is None:
            self.position = (np.random.uniform(-LARGURA, LARGURA), np.random.uniform(-ALTURA, ALTURA), 0)

        else:
            self.position = position

        self.id = self._id_generator()
        self.mission_id: int | None = None
        self.snooped_msg: Dict[int, List[Message]] = dict()
        self.buffer_msg_out: List[Message] = list()
        self.n_neighbors = n_neighbors
        self.neighbors: List[UAV] = list()
        self.attack = attack

        _font = pygame.font.match_font('Droid Sans Mono') 
        _image = pygame.image.load("./assets/hacker_0.png")

        self.hacker_image = pygame.transform.scale(_image, (80, 80))
        self.font = pygame.font.Font(_font, 18)


    def send_msg(self, target: Tuple[float, float, float], type: str):

        if type == "discover":
            self.mission_id = self._mission_id_generator()
            
            msg = Message(target, type)
            msg.mission_id =self.mission_id
            msg.source_id = self.id
            self.tmp_msg.append(msg)
            # print(f"Emitindo mensagem de descoberta | mission_id: {self.mission_id}")

        elif type == "execute":
            msg = Message(target, type)
            msg.mission_id = self.mission_id
            msg.source_id = self.id
            msg.closest_uav_id = self.closest_uav_id
            self.tmp_msg.append(msg)

    
    def clear_buffer_msg_out(self):
        self.buffer_msg_out = list()


    def _handle_attack(self):
        if self.attack:
            for neighbor in self.neighbors:
                if neighbor.id in self.snooped_msg:
                    encrypted_msg = self.snooped_msg[neighbor.id][0]
                    self.buffer_msg_out.append(encrypted_msg)
                    print(f"[ATTACK] Encrypted Message (hex): {encrypted_msg.hex()}\n\n")


    def update(self, delta_time: float | None = None):
        self._handle_attack()


    def draw(self, screen: pygame.Surface):
        x = int((self.position[0] + LARGURA) * 0.5)
        y = int((self.position[1] + ALTURA) * 0.5)

        screen.blit(self.hacker_image,
                    (x - self.hacker_image.get_width() // 2, 
                    y - self.hacker_image.get_height() // 2))
        
        text_surface = self.font.render(f"HACKER_ID: {self.id}", True, (255, 255, 255))
        screen.blit(text_surface, (x+25, y-25))


    @classmethod
    def _id_generator(self) -> int:
        Hacker.id += 1
        return Hacker.id - 1
    
    @classmethod
    def _mission_id_generator(self) -> int:
        Hacker.mission_id += 1
        return Hacker.mission_id - 1
    
    
    def __repr__(self):
        return f"HACKER {self.id} at {self.position}"
