import functools
import logging

from environs import Env
from telegram.ext import (
    Updater,
    CommandHandler,
    Filters,
    MessageHandler
)

from loggers import TgLogsHandler
from api_google import get_response_to_message


logger = logging.getLogger('TG_Logger')

env = Env()
env.read_env()


def start_handler(update, context, logger=None):
    try:
        update.message.reply_text('Здравствуйте!')
    except Exception as e:
        if logger:
            logger.exception(e)


def message_handler(
    update,
    context,
    google_project_id,
    language_code='ru_RU',
    logger=None
):
    try:
        reply = get_response_to_message(
            google_project_id,
            update.effective_user.id,
            update.message.text
        )
        update.message.reply_text(reply)

    except Exception as e:
        if logger:
            logger.exception(e)


def main():
    tg_admin_id = env.str('TG_ADMIN_ID')
    google_project_id = env.str('GOOGLE_PROJECT_ID')
    language_code = env.str('LANGUAGE_CODE', 'ru_RU')
    tg_bot_token = env.str('TG_BOT_TOKEN')
    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    logger.setLevel(logging.INFO)
    logger.addHandler(TgLogsHandler(updater.bot, tg_admin_id))

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            functools.partial(
                message_handler,
                google_project_id=google_project_id,
                language_code=language_code,
                logger=logger
            )
        )
    )

    updater.start_polling()
    logger.info('Telegram-Бот запущен')
    updater.idle()


if __name__ == '__main__':
    main()
