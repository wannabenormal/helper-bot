import random

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from google.cloud import dialogflow

env = Env()
env.read_env()


def message_handler(event, vk_api, google_project_id, language_code='ru_RU'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        google_project_id,
        event.user_id
    )

    text_input = dialogflow.TextInput(
        text=event.text,
        language_code=language_code
    )
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    vk_api.messages.send(
        user_id=event.user_id,
        message=response.query_result.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


def main():
    google_project_id = env.str('GOOGLE_PROJECT_ID')
    vk_group_token = env.str('VK_GROUP_TOKEN')
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            message_handler(event, vk_api, google_project_id)


if __name__ == '__main__':
    main()
