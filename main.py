import telebot
# t.me/MIPT_4_v_ryad_bot
from handlers import initialize_handlers
"""Инициализация бота"""
bot = telebot.TeleBot('6495942120:AAEG72ekxZYrGtWOwQMsfNw3SUxraMLVSBw')
"""Инициализация всех команд для общения с ботом"""
initialize_handlers(bot)

bot.polling()