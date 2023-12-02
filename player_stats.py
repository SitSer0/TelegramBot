"""
Модуль для работы со статистикой игроков в игре '4 в ряд'.

В этом модуле определены функции для создания таблицы статистики игроков в базе данных SQLite,
а также функции для обновления и получения статистики конкретного пользователя.
"""

import sqlite3

# Создание и подключение к базе данных
conn = sqlite3.connect('game_stats.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_stats (
        user_id TEXT PRIMARY KEY,
        wins INTEGER NOT NULL,
        losses INTEGER NOT NULL
    );
''')
conn.commit()
conn.close()

def update_user_stats(user_id, win=True):
    """
    Обновляет статистику пользователя в базе данных.
    """
    conn = sqlite3.connect('game_stats.db')
    cursor = conn.cursor()

    cursor.execute("SELECT wins, losses FROM user_stats WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        wins, losses = result
        wins += int(win)
        losses += int(not win)
        cursor.execute("UPDATE user_stats SET wins = ?, losses = ? WHERE user_id = ?", (wins, losses, user_id))
    else:
        cursor.execute("INSERT INTO user_stats (user_id, wins, losses) VALUES (?, ?, ?)", (user_id, int(win), int(not win)))

    conn.commit()
    conn.close()

def get_user_stats(user_id):
    """
    Получает статистику пользователя из базы данных.
    """
    conn = sqlite3.connect('game_stats.db')
    cursor = conn.cursor()
    cursor.execute("SELECT wins, losses FROM user_stats WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data
