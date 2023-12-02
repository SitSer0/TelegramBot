from telebot import types
from room_manager import RoomManager
from player_stats import get_user_stats, update_user_stats
from game_logic import Game

room_manager = RoomManager()
waiting_for_room_code = {}
rooms = {}

"""
Модуль обработчиков для Telegram-бота игры '4 в ряд'.

Этот модуль содержит функции-обработчики для различных команд и запросов, 
получаемых от пользователей в Telegram-боте. Включает в себя обработку команд 'start' и 'stats', 
а также обработку запросов на создание комнаты, присоединение к комнате и игровые ходы.

"""

def initialize_handlers(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        """
        Отправляет приветственное сообщение и клавиатуру с выбором действий.
        :param message:
        :return:
        """
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Создать комнату", callback_data="create_room"))
        markup.add(types.InlineKeyboardButton("Присоединиться к комнате", callback_data="join_room"))
        markup.add(types.InlineKeyboardButton("Команды бота", callback_data="help"))
        markup.add(types.InlineKeyboardButton("Личная статистика", callback_data="stats"))
        bot.send_message(message.chat.id, "Добро пожаловать в игру '4 в ряд'! Выберите действие:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == "create_room")
    def handle_create_room(call):
        """
        Обрабатывает запрос на создание новой игровой комнаты.
        :param call:
        :return:
        """
        room_id = room_manager.create_room(call.from_user.id)
        bot.send_message(call.message.chat.id, f"Комната создана! Код для присоединения: {room_id}")

    @bot.callback_query_handler(func=lambda call: call.data == "help")
    def handle_help(call):
        """
        Выводит все возможноые команды бота и его умения.
        :param call:
        :return:
        """
        bot.send_message(call.message.chat.id, "Для выхода в начальное меню еще раз наберите /start, далее вы сможете через кнопки прочувствовать весь функционал данного бота ;)")

    @bot.callback_query_handler(func=lambda call: call.data == "join_room")
    def handle_join_room(call):
        """
        Обрабатывает запрос на присоединение к существующей игровой комнате.
        """
        msg = bot.send_message(call.message.chat.id, "Введите код комнаты для присоединения:")
        waiting_for_room_code[call.from_user.id] = True
        bot.register_next_step_handler(msg, process_room_code, call.from_user.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("play_"))
    def handle_play(call):
        """
        Обрабатывает игровые ходы пользователей.
        :param call:
        :return:
        """
        _, col, room_id = call.data.split("_")
        col = int(col)
        room = room_manager.get_room(room_id)
        if not room:
            bot.answer_callback_query(call.id, "Комната не найдена!")
            return

        game = room['game']
        current_player_id = call.from_user.id

        if call.from_user.id != room['current_player']:
            bot.answer_callback_query(call.id, "Сейчас не ваш ход!")
            return

        if not game.drop_piece(col):
            bot.answer_callback_query(call.id, "Столбец заполнен!")
            return

        for player_id in room['players']:
            send_game_board(player_id, game, room_id)

        if game.check_winner():
            update_user_stats(current_player_id, win=True)

            opponent_id = room['players'][0] if current_player_id == room['players'][1] else room['players'][1]
            update_user_stats(opponent_id, win=False)
            for player_id in room['players']:
                bot.send_message(player_id, f"Игрок {game.current_player} победил!")
            if room_id in rooms:
                del rooms[room_id]
            return

        if game.is_full():
            for player_id in room['players']:
                bot.send_message(player_id, "Игра закончилась ничьей!")
            if room_id in rooms:
                del rooms[room_id]
            return

        game.switch_player()
        room['current_player'] = room['players'][0] if call.from_user.id == room['players'][1] else room['players'][1]


    @bot.callback_query_handler(func=lambda call: call.data == "stats")
    def send_user_stats(call):
        message = call.message
        """
        Отправляет статистику пользователя по команде '/stats'.
        :param message:
        :return:
        """
        user_id = message.from_user.id
        data = get_user_stats(user_id)
        if data:
            wins, losses = data
            bot.reply_to(message, f"Ваши статистики:\nПобеды: {wins}\nПоражения: {losses}")
        else:
            bot.reply_to(message, "Статистика для вас пока не доступна.")

    def start_game(room_id):
        """
        Начинает игру после присоединения второго игрока к комнате.
        :param room_id:
        :return:
        """
        room = room_manager.get_room(room_id)
        if not room or len(room['players']) != 2:
            print(f"Комната с ID {room_id} не готова к началу игры.")
            return

        player1_id, player2_id = room['players']

        try:
            player1_info = bot.get_chat(player1_id)
            player2_info = bot.get_chat(player2_id)

            player1_name = f"{player1_info.first_name} {player1_info.last_name}" if player1_info.last_name else player1_info.first_name
            player2_name = f"{player2_info.first_name} {player2_info.last_name}" if player2_info.last_name else player2_info.first_name

            bot.send_message(player1_id, f"Ваш соперник: {player2_name}")
            bot.send_message(player2_id, f"Ваш соперник: {player1_name}")

        except Exception as e:
            print(f"Ошибка при получении информации об игроках: {e}")
            return

        if len(room['players']) == 2:
            game = room['game']

            for player_id in room['players']:
                send_game_board(player_id, game, room_id)

            for player_id in room['players']:
                bot.send_message(player_id, "Игра началась! Ваш оппонент присоединился.")
        else:
            print(f"Не достаточно игроков в комнате {room_id} для начала игры.")

    def send_game_over_message(room_id, message):
        """
        Отправляет сообщение об окончании игры всем участникам комнаты.
        :param room_id:
        :param message:
        :return:
        """
        room = room_manager.get_room(room_id)
        if room:
            for player_id in room['players']:
                bot.send_message(player_id, message)
            room_manager.delete_room(room_id)

    def send_game_board_to_players(room_id):
        """
        Отправляет текущее состояние игрового поля всем участникам комнаты.
        :param room_id:
        :return:
        """
        room = room_manager.get_room(room_id)
        if not room:
            print(f"Комната с ID {room_id} не найдена при попытке отправить игровое поле.")
            return

        game = room['game']
        for player_id in room['players']:
            send_game_board(player_id, game, room_id)

    def send_game_board(chat_id, game, room_id):
        """
        Формирует и отправляет игровое поле конкретному пользователю.
        :param chat_id:
        :param game:
        :param room_id:
        :return:
        """
        markup = types.InlineKeyboardMarkup()
        for row in range(game.rows):
            row_buttons = []
            for col in range(game.cols):
                cell = game.board[row][col]
                if cell == '🔴':
                    button_text = "🔴"
                elif cell == '🟡':
                    button_text = "🟡"
                else:
                    button_text = "⚪"
                callback_data = f"play_{col}_{room_id}"
                row_buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
            markup.row(*row_buttons)
        bot.send_message(chat_id, "Выберите столбец, куда бросить фишку:", reply_markup=markup)

    def process_room_code(message, user_id):
        """
        Обрабатывает ввод кода комнаты пользователем.
        :param message:
        :param user_id:
        :return:
        """
        if user_id not in waiting_for_room_code or not waiting_for_room_code[user_id]:
            return
        room_id = message.text.strip()
        room = room_manager.get_room(room_id)
        if not room:
            bot.send_message(message.chat.id, "Комната с таким кодом не найдена.")
        elif user_id in room['players']:
            bot.send_message(message.chat.id, "Вы не можете присоединиться к своей же комнате.")
        elif len(room['players']) >= 2:
            bot.send_message(message.chat.id, "Комната уже полная.")
        else:
            room['players'].append(user_id)
            bot.send_message(message.chat.id, f"Вы присоединились к комнате {room_id}.")
            if len(room['players']) == 2:
                start_game(room_id)
        waiting_for_room_code[user_id] = False