from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    return InlineKeyboardMarkup([ 
        [InlineKeyboardButton("Добавить привычку", callback_data="add_habit")], 
        [InlineKeyboardButton("Список привычек", callback_data="list_habits")], 
        [InlineKeyboardButton("Отметить привычку", callback_data="mark_habit")], 
        [InlineKeyboardButton("Удалить привычку", callback_data="delete_habit")] 
    ])
