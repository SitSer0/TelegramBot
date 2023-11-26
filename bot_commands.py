from telebot import types

def show_main_menu(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_create_game = types.KeyboardButton("/create")
    item_join_game = types.KeyboardButton("/join")
    markup.row(item_create_game, item_join_game)
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=markup)

def create_game(bot, game_manager, message):
    user_id = message.chat.id
    username = message.from_user.username or message.from_user.first_name
    game_key = game_manager.create_game(['apple', 'banana', 'cherry'])
    if game_manager.add_player_to_game(user_id, game_key, username):
        bot.send_message(user_id, f"Игра создана! Ключ для подключения: {game_key}")
    else:
        bot.send_message(user_id, "Не удалось создать игру.")

def join_game(bot, game_manager, message):
    user_id = message.chat.id
    username = message.from_user.username or message.from_user.first_name
    args = message.text.split()
    if len(args) == 2:
        game_key = args[1].upper()
        if game_manager.game_exists(game_key):
            game = game_manager.get_game(game_key)
            if not game_manager.is_player_in_game(user_id, game_key):
                if game_manager.add_player_to_game(user_id, game_key, username):
                    bot.send_message(user_id, f"Вы подключились к игре {game_key}.")
                    if game.is_ready_to_start():
                        for player_id in game.players:
                            opponent_nicks = game.get_opponent_nicks(player_id)
                            opponents = ', '.join(opponent_nicks)
                            bot.send_message(player_id, f"Игра началась! Ваш противник: {opponents}.")
                else:
                    bot.send_message(user_id, "Невозможно присоединиться к этой игре.")
            else:
                bot.send_message(user_id, "Вы не можете присоединиться к своей же игре.")
        else:
            bot.send_message(user_id, "Игра с таким ключом не найдена.")
    else:
        bot.send_message(user_id, "Пожалуйста, укажите ключ игры после команды /join")
