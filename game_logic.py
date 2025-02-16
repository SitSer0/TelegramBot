"""
Класс Game для игры '4 в ряд'.

Этот класс реализует логику игры '4 в ряд'. Игровое поле представлено в виде двумерного массива.
Игроки по очереди "бросают" фишки в столбцы, стремясь сформировать ряд из четырех фишек своего цвета.

"""

kMagicRed = '🔴'
kMagicYellow = '🟡'
kMagicWhite = '⚪'
kMagicThree = 3
kMagicFour = 4


class Game:
    def __init__(self, rows=6, cols=7, red=kMagicRed, yellow=kMagicYellow):
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.current_player = red

    def drop_piece(self, col):
        """
        Добавляет фишку в указанный столбец. Возвращает True, если ход был сделан.
        :param col:
        :return:
        """
        if self.board[0][col] != ' ':
            return False
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.current_player
                break
        return True

    def switch_player(self):
        """
        Меняет текущего игрока на следующего.
        :return:
        """
        self.current_player = kMagicYellow if self.current_player == kMagicRed else kMagicRed

    def print_board(self):
        """
        Печатает текущее состояние игрового поля в консоль.
        :return:
        """
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print('+---' * self.cols + '+')

    def check_winner(self):
        """
        Проверяет, выиграл ли текущий игрок. Возвращает True, если обнаружен выигрышный ряд.
        :return:
        """
        for row in range(self.rows):
            for col in range(self.cols - kMagicThree):
                if self.board[row][col] == self.current_player and all(
                        self.board[row][col + i] == self.current_player for i in range(1, kMagicFour)):
                    return True
        for row in range(self.rows - kMagicThree):
            for col in range(self.cols):
                if self.board[row][col] == self.current_player and all(
                        self.board[row + i][col] == self.current_player for i in range(1, kMagicFour)):
                    return True
        for row in range(self.rows - kMagicThree):
            for col in range(self.cols - kMagicThree):
                if self.board[row][col] == self.current_player and all(
                        self.board[row + i][col + i] == self.current_player for i in range(1, kMagicFour)):
                    return True
                if self.board[row + kMagicThree][col] == self.current_player and all(
                        self.board[row + kMagicThree - i][col + i] == self.current_player for i in
                        range(1, kMagicFour)):
                    return True
        return False

    def is_full(self):
        """
        Проверяет, заполнено ли игровое поле. Возвращает True, если все ячейки заполнены.
        :return:
        """
        return all(self.board[0][col] != ' ' for col in range(self.cols))
