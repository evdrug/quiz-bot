import logging
import os

import telegram


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot=None):
        super().__init__()
        self.chat_id = os.getenv('LOGGER_TELEGRAM_CHAT_ID')
        if not tg_bot:
            self.telegram_token = os.getenv('LOGGER_TELEGRAM_TOKEN')
            self.tg_bot = telegram.Bot(token=self.telegram_token)
        else:
            self.tg_bot = tg_bot
        self.formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)
