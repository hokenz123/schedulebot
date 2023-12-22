from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import schedule
api_token = "6318109994:AAGo0Mfn7GDNlJJ1adaOZDdEeRsKX9xDeU0"

keyboard = [
    [
        InlineKeyboardButton("Расписание на сегодня", callback_data="today"),
        InlineKeyboardButton("Расписание на завтра", callback_data="next")
    ]
]
reply_markup = InlineKeyboardMarkup(keyboard)
async def start(update: Update, _) -> None:
    await update.message.reply_text("Привет! Пожалуйста выбирете: ", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(text=schedule.get_schedule(query.data), reply_markup=reply_markup)

def print_schedule(date):
    return schedule.get_schedule(date)

def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(api_token).build()
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CallbackQueryHandler(button))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()
