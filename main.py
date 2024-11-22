from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler
from handlers import start, main_menu_handler, receive_habit_name, receive_habit_number, receive_habit_delete
from handlers import list_habits, mark_habit, delete_habit
from data import load_data
from telegram.ext import MessageHandler, filters

def main():
    app = Application.builder().token("7331867278:AAEdKpWCoGUkn7ASsjE3TNH3FoQRDWSGiWY").build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(main_menu_handler)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_habit_name)],  
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_habit_number)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_habit_delete)], 
        },
        fallbacks=[CallbackQueryHandler(main_menu_handler)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    
    app.run_polling()

if __name__ == '__main__':
    main()
