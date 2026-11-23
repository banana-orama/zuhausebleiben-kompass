#!/usr/bin/env python3
"""Strip fetched practical-source HTML pages to plain text."""
import re
from html.parser import HTMLParser


class TextExtract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
        self.block = {'p', 'div', 'li', 'tr', 'h1', 'h2', 'h3', 'h4', 'h5',
                      'h6', 'section', 'article', 'br', 'td', 'th',
                      'blockquote', 'figcaption'}

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript', 'svg', 'nav', 'footer'):
            self.skip += 1
        if tag in self.block:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'svg', 'nav', 'footer'):
            self.skip = max(0, self.skip - 1)
        if tag in self.block:
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


NAMES = ['lifta-weg', 'hiro-ge', 'tke-mf', 'tke-vor', 'tlgurus', 'siemer-weg']

for name in NAMES:
    raw = open(f'{name}.html', encoding='utf-8', errors='replace').read()
    p = TextExtract()
    p.feed(raw)
    text = ''.join(p.parts)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text).strip()
    open(f'{name}.txt', 'w', encoding='utf-8').write(text)
    print(f'{name}.txt: {len(text)} chars')
