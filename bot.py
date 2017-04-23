import nltk
import requests
import urllib.request
from storage import Storage
from nltk.corpus import gutenberg
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup

sample = gutenberg.raw('carroll-alice.txt')
word_tokenizer = RegexpTokenizer(r'\w+')

class Bot:

    def __init__(self):
        print("INITIALIZED")
        self.text = ''
        self.available_languages = ['english', 'italian', 'polish', 'spanish']

    def execute(self, message):
        cmd = message.split()[0]

        if cmd == '/text':
            if len(message) <= 6:
                return "Looks like you forgot to enter the text!\nPrint 'help' for more information."
            self.text = message[6:]
            self.language = 'english'
            return 'Got it!'

        elif cmd == '/word_count':
            if self.text == '':
                return "Looks like I have no text to analyze!\nPrint 'help' for more information."
            return len(word_tokenizer.tokenize(message))

        elif cmd == '/clear':
            self.text = ''
            return "Cleared!"

        elif cmd == '/quit' or cmd == '/exit':
            return 'exited'

        elif cmd == '/language':
            if len(message.split()) < 2:
                return "Incorrect format!\nPrint 'help' for more information."
            language = message.split()[1].lower()
            if language in self.available_languages:
                self.language = language
                return "Language successfully changed to " + language + '.'
            return "Incorrect language.\nType '/supported_languages' for more information."

        elif cmd == '/supported_languages':
            return "The following languages are available:\n" + ', '.join([elem[0].upper() + elem[1:] for elem in self.available_languages])

        elif cmd == '/sym_freq':
            if self.text == '':
                return "Looks like I have no text to analyze!\nPrint 'help' for more information."
            return str(nltk.FreqDist(nltk.Text(self.text)).most_common(10))

        elif cmd == '/download':

            link = message[len(cmd)+1:]
            if 'http://' not in link and 'http://' not in link:
                link = 'https://' + link
            try:
                f = requests.get(link).text
                soup = BeautifulSoup(f, "html.parser")
                self.text = soup.get_text()
                return 'Download successful.'
            except:
                return 'An error occured during the connection attempt.\nPlease try again.'

        elif cmd == '/word_freq':
            if self.text == '':
                return "Looks like I have no text to analyze!\nPrint 'help' for more information."
            return str(nltk.FreqDist(word_tokenizer.tokenize(self.text)).most_common(5))

        elif cmd == '/get_text':
            if self.text == '':
                return "Looks like I have no text!\nPrint 'help' for more information."
            return self.text[:640]


