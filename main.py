from environs import Env
from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler
)


env = Env()
env.read_env()


def start_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Здравствуйте!')


def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)


def main():
    tg_bot_token = env.str('TG_BOT_TOKEN')
    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                          echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
