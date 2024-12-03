import pygame
import numpy as np
from copy import deepcopy
from typing import Tuple, List
from globals import *
from message import Message
from drone import UAV


class BaseStationControl():
    id = 0
    mission_id = 0

    def __init__(self, position: Tuple[float, float, float] | None = None, n_neighbors = 1):

        if position is None:
            self.position = (np.random.uniform(-LARGURA, LARGURA), np.random.uniform(-ALTURA, ALTURA), 0)

        else:
            self.position = position

        self.id = self._id_generator()
        self.buffer_msg_in: List[Message] = list()
        self.buffer_msg_out: List[Message] = list()
        self.n_neighbors = n_neighbors
        self.neighbors: List[UAV] = list()
        self.target: Tuple[float, float, float] | None = None
        self.closest_uav_id: int | None = None
        self.request_id: int | None = None
        self.tmp_msg: List[Message] = list()
        
        
    def send_msg(self, target: Tuple[float, float, float], type: str):

        if type == "discover":
            self.mission_id = self._mission_id_generator()
            
            msg = Message(target, type)
            msg.mission_id =self.mission_id
            msg.source_id = self.id
            self.tmp_msg.append(msg)

    
    def clear_buffer_msg_out(self):
        self.buffer_msg_out = list()


    def handle_receive_msg(self):
        if len(self.buffer_msg_in) > 0:
            pass

        self._clear_buffer_msg_in()


    def _clear_buffer_msg_in(self):
        self.buffer_msg_in = list()
        

    def set_target(self, target: Tuple[float, float, float] | None = None):
        self.target = target
        

    def update(self):
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

        pygame.draw.rect(screen, GREEN, pygame.Rect(x - 5, y - 5, 10, 10))


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
