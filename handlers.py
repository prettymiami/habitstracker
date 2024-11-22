from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from data import load_data, save_data
from keyboard import main_menu_keyboard

ENTER_HABIT_NAME, ENTER_HABIT_NUMBER, DELETE_HABIT = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    if user_id not in data:
        data[user_id] = []
        save_data(data)
    await update.message.reply_text(
        "Привет! Я помогу вам отслеживать привычки. Выберите действие:",
        reply_markup=main_menu_keyboard()
    )

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == "add_habit":
        await query.edit_message_text("Введите название привычки, которую хотите добавить:")
        return ENTER_HABIT_NAME
    elif action == "list_habits":
        await list_habits(update, context)
    elif action == "mark_habit":
        await mark_habit(update, context)
        return ENTER_HABIT_NUMBER
    elif action == "delete_habit":
        await delete_habit(update, context)
        return DELETE_HABIT

async def receive_habit_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    habit_name = update.message.text.strip()
    user_id = str(update.effective_user.id)
    data = load_data()

    if user_id in data and any(habit['habit'] == habit_name for habit in data[user_id]):
        await update.message.reply_text(f"Привычка '{habit_name}' уже существует.", reply_markup=main_menu_keyboard())
    else:
        data[user_id].append({"habit": habit_name, "completed": False})
        save_data(data)
        await update.message.reply_text(f"Привычка '{habit_name}' добавлена!", reply_markup=main_menu_keyboard())
    return ConversationHandler.END

async def list_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    if user_id in data and data[user_id]:
        habits = "\n".join([f"{i+1}. {habit['habit']} - {'✅' if habit['completed'] else '❌'}"
                            for i, habit in enumerate(data[user_id])])
        await update.callback_query.edit_message_text("Ваши привычки:\n" + habits, reply_markup=main_menu_keyboard())
    else:
        await update.callback_query.edit_message_text("У вас нет добавленных привычек.", reply_markup=main_menu_keyboard())

async def mark_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    if user_id in data and data[user_id]:
        habits = "\n".join([f"{i+1}. {habit['habit']} - {'✅' if habit['completed'] else '❌'}"
                            for i, habit in enumerate(data[user_id])])
        await update.callback_query.edit_message_text("Выберите номер привычки, чтобы отметить её выполненной:\n" + habits)
    else:
        await update.callback_query.edit_message_text("У вас нет добавленных привычек.", reply_markup=main_menu_keyboard())
        return ConversationHandler.END

async def receive_habit_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    try:
        habit_index = int(update.message.text) - 1
        if 0 <= habit_index < len(data[user_id]):
            data[user_id][habit_index]["completed"] = True
            save_data(data)
            await update.message.reply_text(
                f"Привычка '{data[user_id][habit_index]['habit']}' отмечена как выполненная!",
                reply_markup=main_menu_keyboard()
            )
        else:
            await update.message.reply_text("Некорректный номер привычки. Попробуйте снова.")
            return ENTER_HABIT_NUMBER
    except ValueError:
        await update.message.reply_text("Введите корректный номер привычки.")
        return ENTER_HABIT_NUMBER

    return ConversationHandler.END

async def delete_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    if user_id in data and data[user_id]:
        habits = "\n".join([f"{i+1}. {habit['habit']} - {'✅' if habit['completed'] else '❌'}"
                            for i, habit in enumerate(data[user_id])])
        await update.callback_query.edit_message_text("Выберите номер привычки, чтобы удалить её:\n" + habits)
    else:
        await update.callback_query.edit_message_text("У вас нет добавленных привычек.", reply_markup=main_menu_keyboard())
        return ConversationHandler.END

async def receive_habit_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    try:
        habit_index = int(update.message.text) - 1
        if 0 <= habit_index < len(data[user_id]):
            deleted_habit = data[user_id].pop(habit_index)
            save_data(data)
            await update.message.reply_text(
                f"Привычка '{deleted_habit['habit']}' удалена!", reply_markup=main_menu_keyboard()
            )
        else:
            await update.message.reply_text("Некорректный номер привычки. Попробуйте снова.")
            return DELETE_HABIT
    except ValueError:
        await update.message.reply_text("Введите корректный номер привычки.")
        return DELETE_HABIT

    return ConversationHandler.END
