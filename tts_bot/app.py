import telebot
import time
import sys
import logging
from telebot import types
import re
import os
from urllib import parse


API_TOKEN = os.getenv('TTS_BOT')

SPANISH = "es"
ENGLISH = "en"
GERMAN = "de"
SPAIN = "es"
MEXICO = "mx"
UK = "uk"
tts_url = "http://translate.google.com/translate_tts?ie=UTF-8&total=1&idx=1&textlen=32&client=tw-ob&q={query}&tl={lang}-{country}"


bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)

@bot.inline_handler(lambda query: re.match("[\w\W]+", query.query))
def query_to_tts(inline_query):
    try:
        query = parse.quote(inline_query.query)
        r = types.InlineQueryResultAudio('1', tts_url.format(query=query, lang=SPANISH, country=SPAIN), 'Español_ES')
        r2 = types.InlineQueryResultAudio('2', tts_url.format(query=query, lang=SPANISH, country=MEXICO), 'Español_MX')
        r3 = types.InlineQueryResultAudio('3', tts_url.format(query=query, lang=ENGLISH, country=UK), 'English_UK')
        
        bot.answer_inline_query(inline_query.id, [r, r2, r3])
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
