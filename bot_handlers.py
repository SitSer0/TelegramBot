import telebot
from bot_commands import show_main_menu, create_game, join_game

def setup_handlers(bot, game_manager):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_message(message.chat.id, "Привет! Я -- бот для игры в Виселицу по сети. Я умею создавать комнаты для игры с друзьями, а также мы можем поиграть с тобой, также у меня есть рейтинговая система и статистика матчей, которые позволяет соревноваться друг с другом! С помощью команды /help ты можешь узнать команды для моего использования.")

    @bot.message_handler(commands=['create'])
    def handle_create(message):
        create_game(bot, game_manager, message)

    @bot.message_handler(commands=['join'])
    def handle_join(message):
        join_game(bot, game_manager, message)

