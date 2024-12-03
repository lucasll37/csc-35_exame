import pygame
import numpy as np
from typing import List, Tuple, Dict
from collections import deque
from globals import *
from utils import draw_logs
from message import Message
from drone import Drone
from baseStationControl import BaseStationControl
from copy import deepcopy


class AdHoc():
    def __init__(self, dimention: Tuple[float, float] = (100, 100)):
        self.uav: Dict[int, Drone] = dict()
        self.bsc: Dict[int, BaseStationControl] = dict()
        self.dimention = dimention
        self.messages_in_transit: List[Message] = []

    def add_drone(self, uav_list: List[Drone]):
        for uav in uav_list:
            self.uav[uav.id] = uav

    def add_bsc(self, gdc_list: List[BaseStationControl]):
        for bsc in gdc_list:
            self.bsc[bsc.id] = bsc

    def update(self) -> bool:
        pause = False

        self.messages_in_transit.clear()

        for uav_id, uav in self.uav.items():
            
            for msg in uav.buffer_msg_out:
                self.uav[msg.destination_id].buffer_msg_in.append(msg)
                self.messages_in_transit.append(msg)

            uav.clear_buffer_msg_out()
            uav.update()

        for bsc_id, bsc in self.bsc.items():
            for msg in bsc.buffer_msg_out:
                self.uav[msg.destination_id].buffer_msg_in.append(msg)
                self.messages_in_transit.append(msg)

            bsc.clear_buffer_msg_out()
            bsc.update()

        self._update_neighbors()
        return pause


    def draw(self, screen: pygame.Surface) -> bool:
        pause = False
        logs = []  # Lista de logs a serem exibidos

        for bsc in self.bsc.values():
            bsc.draw(screen)

            for auv_neighbor in bsc.neighbors:
                message_in_transit = any(
                    msg.source_id == bsc.id and msg.destination_id == auv_neighbor.id for msg in self.messages_in_transit
                )
                color = GREEN if message_in_transit else BLUE

                x1 = int((bsc.position[0] + LARGURA) * 0.5)
                y1 = int((bsc.position[1] + ALTURA) * 0.5)
                x2 = int((auv_neighbor.position[0] + LARGURA) * 0.5)
                y2 = int((auv_neighbor.position[1] + ALTURA) * 0.5)

                distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if distance == 0:
                    continue
                dx = (x2 - x1) / distance
                dy = (y2 - y1) / distance

                largura = 1
                tamanho_traco = 5
                espaco = 10
                passo = tamanho_traco + espaco

                for i in range(0, int(distance), passo):
                    inicio = (x1 + dx * i, y1 + dy * i)
                    fim = (x1 + dx * min(i + tamanho_traco, distance), y1 + dy * min(i + tamanho_traco, distance))
                    pygame.draw.line(screen, color, inicio, fim, largura)

                if message_in_transit:
                    pause = True
                    logs.append(f"Message in transit from BSC {bsc.id} to UAV {auv_neighbor.id}")

        for uav in self.uav.values():
            uav.draw(screen)

            for auv_neighbor in uav.neighbors:
                if uav.id < auv_neighbor.id:
                    continue

                message_in_transit = any(
                    msg.source_id == uav.id and msg.destination_id == auv_neighbor.id for msg in self.messages_in_transit
                )
                color = GREEN if message_in_transit else BLUE

                x1 = int((uav.position[0] + LARGURA) * 0.5)
                y1 = int((uav.position[1] + ALTURA) * 0.5)
                x2 = int((auv_neighbor.position[0] + LARGURA) * 0.5)
                y2 = int((auv_neighbor.position[1] + ALTURA) * 0.5)

                distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if distance == 0:
                    continue
                dx = (x2 - x1) / distance
                dy = (y2 - y1) / distance

                largura = 1
                tamanho_traco = 5
                espaco = 10
                passo = tamanho_traco + espaco

                for i in range(0, int(distance), passo):
                    inicio = (x1 + dx * i, y1 + dy * i)
                    fim = (x1 + dx * min(i + tamanho_traco, distance), y1 + dy * min(i + tamanho_traco, distance))
                    pygame.draw.line(screen, color, inicio, fim, largura)

                if message_in_transit:
                    pause = True
                    logs.append(f"Message in transit from UAV {uav.id} to UAV {auv_neighbor.id}")

        # Chama a função utilitária para exibir os logs
        draw_logs(screen, logs)

        return pause


    # def draw(self, screen: pygame.Surface) -> bool:
    #     pause = False

    #     for bsc in self.bsc.values():
    #         bsc.draw(screen)

    #         # Desenha as linhas tracejadas para os vizinhos
    #         for auv_neighbor in bsc.neighbors:

    #             # Verifica se há mensagem em trânsito nesta conexão
    #             message_in_transit = any(
    #                 msg.source_id == bsc.id and msg.destination_id == auv_neighbor.id for msg in self.messages_in_transit
    #             )

    #             # Define a cor: verde se há mensagem, BLUE se é apenas conexão
    #             color = GREEN if message_in_transit else BLUE


    #             # Calcula as posições escaladas para a tela
    #             x1 = int((bsc.position[0] + LARGURA) * 0.5)
    #             y1 = int((bsc.position[1] + ALTURA) * 0.5)
    #             x2 = int((auv_neighbor.position[0] + LARGURA) * 0.5)
    #             y2 = int((auv_neighbor.position[1] + ALTURA) * 0.5)

    #             # # Calcula a distância total e a direção entre os dois pontos
    #             distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #             if distance == 0:
    #                 continue  # Evita divisão por zero
    #             dx = (x2 - x1) / distance
    #             dy = (y2 - y1) / distance

    #             # Define parâmetros da linha tracejada
    #             largura = 1
    #             tamanho_traco = 5
    #             espaco = 10
    #             passo = tamanho_traco + espaco

    #             # Desenha a linha tracejada
    #             for i in range(0, int(distance), passo):
    #                 inicio = (x1 + dx * i, y1 + dy * i)
    #                 fim = (x1 + dx * min(i + tamanho_traco, distance), y1 + dy * min(i + tamanho_traco, distance))
    #                 pygame.draw.line(screen, color, inicio, fim, largura)

    #             if message_in_transit:
    #                 pause = True

    #     for uav in self.uav.values():
    #         # Desenha o UAV
    #         uav.draw(screen)

    #         # Desenha as linhas tracejadas para os vizinhos
    #         for auv_neighbor in uav.neighbors:
    #             if uav.id < auv_neighbor.id:
    #                 continue


    #             # Verifica se há mensagem em trânsito nesta conexão
    #             message_in_transit = any(
    #                 msg.source_id == uav.id and msg.destination_id == auv_neighbor.id for msg in self.messages_in_transit
    #             )

    #             # Define a cor: verde se há mensagem, BLUE se é apenas conexão
    #             color = GREEN if message_in_transit else BLUE

    #             # Calcula as posições escaladas para a tela
    #             x1 = int((uav.position[0] + LARGURA) * 0.5)
    #             y1 = int((uav.position[1] + ALTURA) * 0.5)
    #             x2 = int((auv_neighbor.position[0] + LARGURA) * 0.5)
    #             y2 = int((auv_neighbor.position[1] + ALTURA) * 0.5)

    #             # Calcula a distância total e a direção entre os dois pontos
    #             distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #             if distance == 0:
    #                 continue  # Evita divisão por zero
    #             dx = (x2 - x1) / distance
    #             dy = (y2 - y1) / distance

    #             # Define parâmetros da linha tracejada
    #             largura = 1
    #             tamanho_traco = 5
    #             espaco = 10
    #             passo = tamanho_traco + espaco

    #             # Desenha a linha tracejada
    #             for i in range(0, int(distance), passo):
    #                 inicio = (x1 + dx * i, y1 + dy * i)
    #                 fim = (x1 + dx * min(i + tamanho_traco, distance), y1 + dy * min(i + tamanho_traco, distance))
    #                 pygame.draw.line(screen, color, inicio, fim, largura)

    #             if message_in_transit:
    #                 pause = True

    #     return pause
                    

    def _update_neighbors(self):
        # Atualiza os vizinhos das estações base
        for bsc_id, bsc in self.bsc.items():
            distances = self._close_neighbor_bsc(bsc_id)
            selected_neighbors = list(distances.keys())[:bsc.n_neighbors]
            bsc.neighbors = [self.uav[uav_id] for uav_id in selected_neighbors]
            

        # Atualiza os vizinhos dos drones
        for uav_id, uav in self.uav.items():
            distances = self._close_neighbor(uav_id)
            selected_neighbors = list(distances.keys())[:uav.n_neighbors]
            uav.neighbors = [self.uav[uav_id] for uav_id in selected_neighbors]

        # Garante que a relação de vizinhança seja recíproca
        for uav_id, uav in self.uav.items():
            for neighbor in uav.neighbors:
                if uav_id not in neighbor.neighbors:
                    neighbor.neighbors.append(uav)

        # Verifica se a rede é conectada
        if not self._is_connected():
            self._ensure_connectivity()

    def _is_connected(self) -> bool:
        """
        Verifica se todos os UAVs estão conectados direta ou indiretamente.
        """
        if not self.uav:
            return True  # Uma rede vazia é trivialmente conectada

        visited = set()
        queue = deque([next(iter(self.uav.values()))])  # Começa com um nó arbitrário

        while queue:
            current = queue.popleft()
            if current.id not in visited:
                visited.add(current.id)
                # Adiciona os vizinhos ainda não visitados à fila
                queue.extend([neighbor for neighbor in current.neighbors if neighbor.id not in visited])

        # Verifica se todos os UAVs foram visitados
        return len(visited) == len(self.uav)

    def _ensure_connectivity(self):
        """
        Garante que todos os UAVs estão conectados adicionando conexões mínimas.
        """
        uav_ids = list(self.uav.keys())
        for i in range(len(uav_ids)):
            for j in range(i + 1, len(uav_ids)):
                uav1, uav2 = self.uav[uav_ids[i]], self.uav[uav_ids[j]]
                if uav2.id not in uav1.neighbors and uav1.id not in uav2.neighbors:
                    # Conecta os UAVs se necessário
                    uav1.neighbors[uav2.id] = uav2
                    uav2.neighbors[uav1.id] = uav1
                    # Revalida a conectividade
                    if self._is_connected():
                        return

    def _close_neighbor_bsc(self, bsc_id: int) -> Dict[str, float]:
        distances: Dict[str, float] = dict()

        for uav_id, _ in self.uav.items():
            distances[uav_id] = self._distance_bsc(bsc_id, uav_id)

        ordered = dict(sorted(distances.items(), key=lambda item: item[1]))
        return ordered

    def _close_neighbor(self, id: int) -> Dict[str, float]:
        distances: Dict[str, float] = dict()

        for uav_id, _ in self.uav.items():
            if uav_id != id:
                distances[uav_id] = self._distance(id, uav_id)

            else:
                distances[uav_id] = float(np.inf)

        ordered = dict(sorted(distances.items(), key=lambda item: item[1]))
        return ordered

    def _distance_bsc(self, bsc_id: int, uav_id: int) -> float:
        return float(np.sqrt((self.bsc[bsc_id].position[0] - self.uav[uav_id].position[0])**2 + \
                       (self.bsc[bsc_id].position[1] - self.uav[uav_id].position[1])**2 + \
                        (self.bsc[bsc_id].position[2] - self.uav[uav_id].position[2])**2))

    def _distance(self, uav0_id: int, uav1_id: int) -> float:
        return float(np.sqrt((self.uav[uav1_id].position[0] - self.uav[uav0_id].position[0])**2 + \
                       (self.uav[uav1_id].position[1] - self.uav[uav0_id].position[1])**2 + \
                        (self.uav[uav1_id].position[2] - self.uav[uav0_id].position[2])**2))
