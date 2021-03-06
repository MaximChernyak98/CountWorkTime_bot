import time
from telegram.ext import MessageHandler, Filters
from settings import MYBOT
import config
from interaction.handlers import greeting

def initialization(dp):
    MYBOT.start_polling()
    config.CHAT_ID = 0
    great_handler = MessageHandler(Filters.all, greeting)
    dp.add_handler(great_handler)
    while config.CHAT_ID == 0:
        time.sleep(2)
    dp.remove_handler(great_handler)
