import requests
import lxml
import telebot
import time
import sys
import logging
from telebot import types
import re
import os
import feedparser
from bs4 import BeautifulSoup
import html2text

API_TOKEN = os.getenv("ELMUNDO_BOT")
elmundo_rss = "http://estaticos.elmundo.es/elmundo/rss/{endpoint}.xml"

class Article:
    def __init__(self, title, content, link):
        html_cleaned = clean_content(content)
        print(html_cleaned)
        self.content = parse_to_markdown(html_cleaned)
        print(self.content)
        self.link = link
        self.title = title
        
    def __repr__(self):
        return '*{title}*\n{content}... [Leer más]({link})'.format(content=self.content,
                                                                                    link=self.link,
                                                                                    title=self.title)

def clean_content(content):
    content_fixed = fix_unclosed_html(content)
    content_cleaned = remove_useless_tags(content_fixed)
    return content_cleaned

def fix_unclosed_html(html):
    soup = BeautifulSoup(html)
    result = ""
    for children in soup.body:
        result += str(children)
    return result

def remove_useless_tags(html):
    html = html.replace("<p>","").replace("</p>","")
    return html

def parse_to_markdown(html):
    content_markdownized = html2text.html2text(html)
    return content_markdownized

bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)

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

def obtain_posts(endpoint):
    rss = feedparser.parse(elmundo_rss.format(endpoint=endpoint))
    articles = []
    for item in rss.entries:
        try:
            article = Article(item.title, item.content[0]['value'], item.link)
            print(article)
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
