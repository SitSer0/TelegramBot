"""
Модуль для управления игровыми комнатами в игре '4 в ряд'.

Класс RoomManager обеспечивает функциональность для создания, получения и удаления игровых комнат.
Каждая комната представляет из себя игру '4 в ряд' и содержит информацию об игроках и текущем состоянии игры.

Методы класса:
- create_room: Создает новую комнату с уникальным идентификатором и добавляет создателя в список игроков.
- get_room: Возвращает комнату по ее идентификатору.
- delete_room: Удаляет комнату по ее идентификатору.
"""

import random
import string
from game_logic import Game

class RoomManager:
    def __init__(self):
        """Инициализация менеджера комнат с пустым словарем комнат."""
        self.rooms = {}

    def create_room(self, user_id):
        """
        Создает новую игровую комнату с уникальным ID и добавляет пользователя в список игроков комнаты.
        """
        room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while room_id in self.rooms:
            room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.rooms[room_id] = {'players': [user_id], 'game': Game(), 'current_player': user_id}
        return room_id

    def get_room(self, room_id):
        """
        Возвращает комнату по ее идентификатору.
        """
        return self.rooms.get(room_id)

    def delete_room(self, room_id):
        """
        Удаляет комнату по ее идентификатору.
        """
        if room_id in self.rooms:
            del self.rooms[room_id]
