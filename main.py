"""
Gеред запуском бота нужно установить необходимые библиотеки, это можно сделать командой

pip install pyTelegramBotAPI

6360575319:AAGKFR5VuEtPUbfvsAyofVgv_SgxzWNlBqg

"""

import telebot
from bot_handlers import setup_handlers
from game_manager import GameManager

TOKEN = '6360575319:AAGKFR5VuEtPUbfvsAyofVgv_SgxzWNlBqg'
bot = telebot.TeleBot(TOKEN)
game_manager = GameManager()

setup_handlers(bot, game_manager)

bot.polling()
