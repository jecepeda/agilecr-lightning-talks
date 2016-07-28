import requests
import lxml
import telebot
import time
import sys
import logging
from telebot import types
import re
import os
from article import Article
import feedparser

API_TOKEN = os.getenv("ELMUNDO_BOT")
elmundo_rss = "http://estaticos.elmundo.es/elmundo/rss/{endpoint}.xml"

welcome_message = "*Hola, soy ElMundoBot*, tu bot de noticias\n" \
                  "Para poder usarme, debes llamarme en la línea de ordenes con:\n" \
                  "@elmundo\_inlinebot _<nombre de la sección_> para que te busque las últimas noticias.\n" \
                  "Las secciones que dispongo para enseñarte son: \n" \
                  "españa\n" \
                  "Espero serte de gran ayuda! *:)*\n" \
                  "Mi código fuente está en [este repositorio](https://github.com/JCepedaVillamayor/agilecr-lightning-talks)"

bot = telebot.TeleBot(API_TOKEN)
#telebot.logger.setLevel(logging.DEBUG)

@bot.inline_handler(lambda query: re.match("españa",query.query, re.IGNORECASE))
def query_spain_elmundo(inline_query):
    try:
        responses = []
        articles = obtain_posts('espana')
        for index, article in enumerate(articles):
            response = types.InlineQueryResultArticle(str(index),
                                                      article.title,
                                                      types.InputTextMessageContent(str(article), parse_mode="Markdown"))
            responses.append(response)
        bot.answer_inline_query(inline_query.id, responses)
    except Exception as e:
        print(e)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, welcome_message, parse_mode="Markdown")

def obtain_posts(endpoint):
    articles = []
    try:
        rss = feedparser.parse(elmundo_rss.format(endpoint=endpoint))
    except Exception as e:
        article = Article("La pagina de El Mundo no funciona correctamente","Disculpen las molestias","")
        return [article]
    
    for item in rss.entries:
        try:
            article = Article(item.title, item.content[0]['value'], item.link)
            articles.append(article)
        except Exception as e:
            print(e)
            
    return articles

def main_loop():
    bot.polling(True)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print("Bye bye!")
        sys.exit(0)
