from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters
from handlers import (
    start, add_habit, receive_habit_name, list_habits, 
    mark_habit, receive_habit_number, delete_habit, receive_habit_delete,
    ENTER_HABIT_NAME, ENTER_HABIT_NUMBER, DELETE_HABIT
)

def main():
    app = Application.builder().token("7331867278:AAEdKpWCoGUkn7ASsjE3TNH3FoQRDWSGiWY").build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("add_habit", add_habit),
            CommandHandler("mark_habit", mark_habit),
            CommandHandler("delete_habit", delete_habit)
        ],
        states={
            ENTER_HABIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_habit_name)],
            ENTER_HABIT_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_habit_number)],
            DELETE_HABIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_habit_delete)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list_habits", list_habits))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == '__main__':
    main()
