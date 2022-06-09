import functools

from environs import Env
from telegram.ext import (
    Updater,
    CommandHandler,
    Filters,
    MessageHandler
)
from google.cloud import dialogflow


env = Env()
env.read_env()


def start_handler(update, context):
    update.message.reply_text('Здравствуйте!')


def message_handler(update, context, google_project_id, language_code='ru_RU'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        google_project_id,
        update.effective_user.id
    )

    text_input = dialogflow.TextInput(
        text=update.message.text,
        language_code=language_code
    )
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    update.message.reply_text(response.query_result.fulfillment_text)


def main():
    google_project_id = env.str('GOOGLE_PROJECT_ID')
    language_code = env.str('LANGUAGE_CODE', 'ru_RU')
    tg_bot_token = env.str('TG_BOT_TOKEN')
    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            functools.partial(
                message_handler,
                google_project_id=google_project_id,
                language_code=language_code
            )
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
