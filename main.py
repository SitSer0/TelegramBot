import telebot
from setting.gitignore import BOT_TOKEN

from handlers import initialize_handlers

"""Инициализация бота"""
bot = telebot.TeleBot(BOT_TOKEN)
"""Инициализация всех команд для общения с ботом"""
initialize_handlers(bot)

bot.polling()
