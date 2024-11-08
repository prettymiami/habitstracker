from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from data import load_data, save_data

ENTER_HABIT_NAME, ENTER_HABIT_NUMBER, DELETE_HABIT = range(3)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привет! Я помогу вам отслеживать привычки. "
        "Введите /add_habit для добавления новой привычки, "
        "Введите /list_habits для просмотра списка привычек, "
        "Введите /mark_habit для отметки выполнения привычки. "
        "Введите /delete_habit для удаления привычки."
    )

async def add_habit(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Введите название привычки, которую хотите добавить:")
    return ENTER_HABIT_NAME

async def receive_habit_name(update: Update, context: CallbackContext) -> int:
    habit_name = update.message.text
    user_id = str(update.message.chat_id)
    data = load_data()
    
    if user_id in data and any(habit['habit'] == habit_name for habit in data[user_id]):
        await update.message.reply_text(f"Привычка '{habit_name}' уже существует.")
        return ConversationHandler.END
    else:
        if user_id not in data:
            data[user_id] = []
        data[user_id].append({"habit": habit_name, "completed": False})
        save_data(data)

        await update.message.reply_text(f"Привычка '{habit_name}' добавлена!", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

async def list_habits(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    data = load_data()

    if user_id in data and data[user_id]:
        habits = "\n".join([f"{i+1}. {habit['habit']} - {'✅' if habit['completed'] else '❌'}" 
                            for i, habit in enumerate(data[user_id])])
        await update.message.reply_text("Ваши привычки:\n" + habits)
    else:
        await update.message.reply_text("У вас нет добавленных привычек.")

async def mark_habit(update: Update, context: CallbackContext) -> int:
    user_id = str(update.message.chat_id)
    data = load_data()

    if user_id in data and data[user_id]:
        habits = "\n".join([f"{i+1}. {habit['habit']} - {'✅' if habit['completed'] else '❌'}" 
                            for i, habit in enumerate(data[user_id])])
        await update.message.reply_text("Выберите номер привычки, которую хотите отметить как выполненную:\n" + habits)
        return ENTER_HABIT_NUMBER
    else:
        await update.message.reply_text("У вас нет добавленных привычек.")
        return ConversationHandler.END

async def receive_habit_number(update: Update, context: CallbackContext) -> int:
    user_id = str(update.message.chat_id)
    data = load_data()

    try:
        habit_index = int(update.message.text) - 1
        if 0 <= habit_index < len(data[user_id]):
            data[user_id][habit_index]["completed"] = True
            save_data(data)
            await update.message.reply_text("Привычка отмечена как выполненная!")
        else:
            await update.message.reply_text("Некорректный номер привычки. Попробуйте снова.")
            return ENTER_HABIT_NUMBER
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректный номер.")
        return ENTER_HABIT_NUMBER

    return ConversationHandler.END

async def delete_habit(update: Update, context: CallbackContext) -> int:
    user_id = str(update.message.chat_id)
    data = load_data()

    if user_id in data and data[user_id]:
        habits = "\n".join([f"{i+1}. {habit['habit']} - {'✅' if habit['completed'] else '❌'}" 
                            for i, habit in enumerate(data[user_id])])
        await update.message.reply_text("Выберите номер привычки, которую хотите удалить:\n" + habits)
        return DELETE_HABIT
    else:
        await update.message.reply_text("У вас нет добавленных привычек.")
        return ConversationHandler.END

async def receive_habit_delete(update: Update, context: CallbackContext) -> int:
    user_id = str(update.message.chat_id)
    data = load_data()

    try:
        habit_index = int(update.message.text) - 1
        if 0 <= habit_index < len(data[user_id]):
            deleted_habit = data[user_id].pop(habit_index)
            save_data(data)
            await update.message.reply_text(f"Привычка '{deleted_habit['habit']}' удалена!")
        else:
            await update.message.reply_text("Некорректный номер привычки. Попробуйте снова.")
            return DELETE_HABIT
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректный номер.")
        return DELETE_HABIT

    return ConversationHandler.END
