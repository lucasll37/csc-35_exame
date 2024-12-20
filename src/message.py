from typing import Tuple
import numpy as np

class Message():
    id = 0

    def __init__(self, position: Tuple[float, float, float], type: str):
        self.id = self._id_generator()
        self.position = position
        self.type= type
        self.mission_id: int | None = None
        self.source_id: int | None = None
        self.destination_id: int | None = None
        self.closest_uav_id: int | None = None
        self.distance = float(np.inf)

    @classmethod
    def _id_generator(self) -> int:
        Message.id += 1
        return Message.id - 1
    
    def __repr__(self):
        return f"Source ID: {self.source_id} | Destination ID: {self.destination_id} | Type: {self.type} | Mission ID: {self.mission_id} | Closest UAV ID: {self.closest_uav_id} | Distance: {self.distance} | Position: {self.position}"