import random
import logging

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from loggers import VkLogsHandler
from api_google import get_response_to_message


logger = logging.getLogger('VkLogsHandler')

env = Env()
env.read_env()


def message_handler(
    event,
    vk_api,
    google_project_id,
    language_code='ru_RU',
    logger=None
):
    try:
        reply = get_response_to_message(
            google_project_id,
            event.user_id,
            event.text,
            allow_fallback=False
        )

        if reply:
            vk_api.messages.send(
                user_id=event.user_id,
                message=reply,
                random_id=random.randint(1, 1000)
            )
    except Exception as e:
        if logger:
            logger.exception(e)


def main():
    vk_admin_id = env.str('VK_ADMIN_ID')
    google_project_id = env.str('GOOGLE_PROJECT_ID')
    vk_group_token = env.str('VK_GROUP_TOKEN')

    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()

    logger.setLevel(logging.INFO)
    logger.addHandler(VkLogsHandler(vk_api, vk_admin_id))

    longpoll = VkLongPoll(vk_session)
    logger.info('VK-Бот запущен')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            message_handler(event, vk_api, google_project_id)


if __name__ == '__main__':
    main()
