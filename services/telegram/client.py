import telebot
from .config import TELEGRAM_API_KEY, TELEGRAM_CHAT_ID


class TeleClient():
    def __init__(self, message):
        self.message = message
        self._run()

    def _run(self):
        self.bot = telebot.TeleBot(TELEGRAM_API_KEY)

    def send_message(self):
        self.bot.send_message(TELEGRAM_CHAT_ID, self.message)
