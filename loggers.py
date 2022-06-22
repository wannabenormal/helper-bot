import logging
import random


class TgLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


class VkLogsHandler(logging.Handler):
    def __init__(self, vk_api, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vk_api = vk_api
        self.user_id = user_id

    def emit(self, record):
        log_entry = self.format(record)
        self.vk_api.messages.send(
            user_id=self.user_id,
            message=log_entry,
            random_id=random.randint(1, 1000)
        )
