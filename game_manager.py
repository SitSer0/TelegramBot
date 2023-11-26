import random
import string
from hangman_game import HangmanGame

class GameManager:
    def __init__(self):
        self.games = {}
        self.user_game = {}

    def create_game(self, word_list):
        unique_key = self._generate_unique_key()
        self.games[unique_key] = HangmanGame(word_list)
        return unique_key

    def _generate_unique_key(self, length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def get_game(self, key):
        return self.games.get(key)

    def game_exists(self, key):
        return key in self.games

    def add_player_to_game(self, user_id, game_key, username):
        if game_key in self.games and user_id not in self.user_game:
            self.games[game_key].add_player(user_id, username)
            self.user_game[user_id] = game_key
            return True
        return False

    def is_player_in_game(self, user_id, game_key):
        return user_id in self.games[game_key].players

    def get_user_game(self, user_id):
        return self.user_game.get(user_id)
