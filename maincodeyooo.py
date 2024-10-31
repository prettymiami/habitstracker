import json
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler, 
    CallbackContext, filters, ContextTypes
)

ENTER_HABIT_NAME, ENTER_HABIT_NUMBER = range(2)

DATAFILE = "data.json"

def load_data():
    try:
        with open(DATAFILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(DATAFILE, 'w') as file:
        json.dump(data, file)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу вам отслеживать привычки. "
        "Введите /add_habit для добавления новой привычки, "
        "/list_habits для просмотра списка привычек, "
        "/mark_habit для отметки выполнения привычки."
    )

async def add_habit(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Введите название привычки, которую хотите добавить:")
    return ENTER_HABIT_NAME

async def receive_habit_name(update: Update, context: CallbackContext) -> int:
    habit_name = update.message.text
    user_id = str(update.message.chat_id)
    data = load_data()

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

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Действие отменено.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token("7331867278:AAEdKpWCoGUkn7ASsjE3TNH3FoQRDWSGiWY").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_habit", add_habit), CommandHandler("mark_habit", mark_habit)],
        states={
            ENTER_HABIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_habit_name)],
            ENTER_HABIT_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_habit_number)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list_habits", list_habits))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == '__main__':
    main()
