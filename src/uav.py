from abc import ABC
from globals import *
import numpy as np
from typing import Tuple
import numpy as np


class UAV(ABC):
    id = 0

    def __init__(self, position: Tuple[float, float, float] | None = None, velocity: float = 1):
        self.id = self._id_generator()
        self.velocity = velocity

        if position is None:
            self.position = (np.random.uniform(-LARGURA, LARGURA), np.random.uniform(-ALTURA, ALTURA), 10)

        else:
            self.position = position

    @classmethod
    def _id_generator(self) -> int:
        UAV.id += 1
        return UAV.id - 1
    
    def __repr__(self):
        return f"UAV {self.id} at {self.position}"