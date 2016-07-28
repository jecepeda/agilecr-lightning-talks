from utils import clean_content, parse_to_markdown

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
