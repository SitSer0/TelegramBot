import random

class HangmanGame:
    def __init__(self, word_list):
        self.word_list = word_list
        self.secret_word = random.choice(self.word_list).upper()
        self.correct_letters = set()
        self.incorrect_letters = set()
        self.max_attempts = 7
        self.remaining_attempts = self.max_attempts
        self.players = {}
        self.players = {}
        self.word_list = word_list
        self.word_to_guess = ""
        self.guesses_left = 6
        self.guesses = []
        self.game_status = "waiting"

    def start_game(self):
        if self.game_status == "waiting" and len(self.players) == 2:
            self.word_to_guess = random.choice(self.word_list)
            self.guesses_left = 6
            self.guesses = []
            self.game_status = "playing"
            return True
        return False

    def is_ready_to_start(self):
        # Игра готова начаться, если есть два уникальных игрока
        return len(self.players) == 2

    def get_opponent_nicks(self, user_id):
        # Возвращает ники всех игроков, кроме заданного
        return [nick for id, nick in self.players.items() if id != user_id]

    def guess(self, letter):
        letter = letter.upper()
        if letter in self.secret_word:
            self.correct_letters.add(letter)
            return True
        else:
            self.incorrect_letters.add(letter)
            self.remaining_attempts -= 1
            return False

    def get_display_word(self):
        return ' '.join([letter if letter in self.correct_letters else '_' for letter in self.secret_word])

    def is_won(self):
        return all(letter in self.correct_letters for letter in self.secret_word)

    def is_lost(self):
        return self.remaining_attempts <= 0

    def game_over(self):
        return self.is_won() or self.is_lost()

    def get_game_status(self):
        return {
            'display_word': self.get_display_word(),
            'remaining_attempts': self.remaining_attempts,
            'guessed_letters': self.correct_letters.union(self.incorrect_letters)
        }

    def add_player(self, user_id, username):
        if user_id not in self.players:
            self.players[user_id] = username
            return True
        return False
