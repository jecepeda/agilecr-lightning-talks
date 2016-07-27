import telebot
import time
import sys
import logging
from telebot import types
import re
import os

API_TOKEN = os.getenv('HELLO_WORLD_BOT')
bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)


@bot.inline_handler(lambda query: re.match("[\w\W]+", query.query))
def query_to_tts(inline_query):
    try:
        query = inline_query.query
        query = "*{}*".format(query) if re.match("hello", query, re.IGNORECASE) else "*Hello {}*".format(query)
        r1 = types.InlineQueryResultArticle('1', 'HELLO WORLD',
                                            types.InputTextMessageContent(query, parse_mode="Markdown"))
        r2 = types.InlineQueryResultGif('2','https://media.giphy.com/media/Y8ocCgwtdj29O/giphy.gif',
                                        'https://media.giphy.com/media/Y8ocCgwtdj29O/giphy.gif')
        bot.answer_inline_query(inline_query.id, [r1, r2])
    except Exception as e:
        print(e)

def main_loop():
    bot.polling(True)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print("Bye bye!")
        sys.exit(0)
