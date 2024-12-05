import pygame
import numpy as np
from copy import deepcopy
from encryption import *
from typing import Tuple, List
from globals import *
from message import Message
from drone import UAV


class BaseStationControl():
    id = 0
    mission_id = 0

    def __init__(self, position: Tuple[float, float, float] | None = None, n_neighbors = 1, symmetric_key: bytes | None = None):

        if position is None:
            self.position = (np.random.uniform(-LARGURA, LARGURA), np.random.uniform(-ALTURA, ALTURA), 0)

        else:
            self.position = position

        self.id = self._id_generator()
        self.mission_id: int | None = None
        self.buffer_msg_in: List[Message] = list()
        self.buffer_msg_out: List[Message] = list()
        self.n_neighbors = n_neighbors
        self.neighbors: List[UAV] = list()
        self.closest_uav_id: int | None = None
        self.request_id: int | None = None
        self.tmp_msg: List[Message] = list()
        self.symmetric_key = symmetric_key
        self.emit_execute = False

        _font = pygame.font.match_font('Droid Sans Mono') 
        _image = pygame.image.load("./assets/bsc_0.png")
        
        self.font = pygame.font.Font(_font, 18)
        self.bsc_image = pygame.transform.scale(_image, (50, 50))

        
    def send_msg(self, target: Tuple[float, float, float], type: str):

        if type == "discover":
            self.mission_id = self._mission_id_generator()
            self.emit_execute = False
            
            msg = Message(target, type)
            msg.mission_id =self.mission_id
            msg.source_id = self.id
            self.tmp_msg.append(msg)
            # print(f"Emitindo mensagem de descoberta | mission_id: {self.mission_id}")

        elif type == "execute":
            self.emit_execute = True
        
            msg = Message(target, type)
            msg.mission_id = self.mission_id
            msg.source_id = self.id
            msg.closest_uav_id = self.closest_uav_id
            self.tmp_msg.append(msg)

    
    def clear_buffer_msg_out(self):
        self.buffer_msg_out = list()


    def handle_receive_msg(self):
        if len(self.buffer_msg_in) > 0:

            for encrypted_msg in self.buffer_msg_in:
                msg = decrypt_object(self.symmetric_key, encrypted_msg)

                if msg.mission_id != self.mission_id:
                    continue
                
                if msg.type == "return" and not self.emit_execute:
                    self.closest_uav_id = msg.closest_uav_id
                    self.send_msg(msg.position, "execute")

                if msg.type == "finish":
                    self.mission_id = None


        self._clear_buffer_msg_in()


    def _clear_buffer_msg_in(self):
        self.buffer_msg_in = list()


    def update(self, delta_time: float | None = None):
        self.handle_receive_msg()

        if len(self.tmp_msg) > 0 and len(self.neighbors) > 0:

            for msg in self.tmp_msg:
                for neighbor in self.neighbors:
                    _msg = deepcopy(msg)
                    _msg.destination_id = neighbor.id
                    self.buffer_msg_out.append(_msg)

            self.tmp_msg = list()

    
    def draw(self, screen: pygame.Surface):
        x = int((self.position[0] + LARGURA) * 0.5)
        y = int((self.position[1] + ALTURA) * 0.5)

        screen.blit(self.bsc_image,
                    (x - self.bsc_image.get_width() // 2, 
                    y - self.bsc_image.get_height() // 2))
        
        text_surface = self.font.render(f"BSC_ID: {self.id}", True, (255, 255, 255))
        screen.blit(text_surface, (x+25, y-25))


    @classmethod
    def _id_generator(self) -> int:
        BaseStationControl.id += 1
        return BaseStationControl.id - 1
    
    @classmethod
    def _mission_id_generator(self) -> int:
        BaseStationControl.mission_id += 1
        return BaseStationControl.mission_id - 1
    
    
    def __repr__(self):
        return f"BSC {self.id} at {self.position}"
