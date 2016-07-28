import feedparser
from bs4 import BeautifulSoup
import html2text

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
