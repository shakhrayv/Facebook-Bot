import nltk
import storage
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
from translation_api import *


yandex_api_key = 'trnsl.1.1.20170504T161543Z.1ce6778cb7154603.5f9dbe3d943c4486d33bf509831868ce1f10bdc8'
word_tokenizer = RegexpTokenizer(r'\w+')


class Bot:
    def __init__(self):
        print("INITIALIZED")
        self.text = ''
        self.storage = storage.Storage()
        self.translation = None
        self.translation_engine = YandexTranslate(yandex_api_key)

    def store_temp(self, translation):
        self.translation = translation

    def execute(self, message, sender):
        self.sender = sender
        cmd = message.split()[0]

        if cmd == '/text':
            if len(message) <= 6:
                yield "Looks like you forgot to enter the text!\nPrint 'help' for more information."
                return
            self.text = message[6:]
            yield 'Got it!'

        elif cmd == '/word_count':
            if self.text == '':
                yield "Looks like I have no text to analyze!\nPrint 'help' for more information."
                return
            yield str(len(word_tokenizer.tokenize(message)))

        elif cmd == '/sym_count':
            if self.text == '':
                yield "Looks like I have no text to analyze!\nPrint 'help' for more information."
                return
            yield str(len(message))

        elif cmd == '/clear':
            self.text = ''
            self.storage.clear(sender)
            yield "Cleared!"

        elif cmd == '/quit' or cmd == '/exit':
            self.storage.save()
            yield 'Bye!'

        elif cmd == '/sym_freq':
            if self.text == '':
                yield "Looks like I have no text to analyze!\nPrint 'help' for more information."
                return
            yield str(nltk.FreqDist(nltk.Text(self.text)).most_common(10))

        elif cmd == '/download':
            link = message[len(cmd)+1:]
            if 'http://' not in link and 'http://' not in link:
                link = 'https://' + link
            try:
                f = requests.get(link).text
                soup = BeautifulSoup(f, "html.parser")
                self.text = soup.get_text()
                yield 'Download successful.'
            except:
                yield 'An error occurred during the connection attempt.\nPlease try again.'


        elif cmd == '/word_freq':
            if self.text == '':
                yield "Looks like I have no text to analyze!\nPrint 'help' for more information."
                return
            yield str(nltk.FreqDist(word_tokenizer.tokenize(self.text)).most_common(5))

        elif cmd == '/get_text':
            if self.text == '':
                yield "Looks like I don't have any text!\nPrint 'help' for more information."
                return
            yield self.text[:640]

        elif cmd == '/save':
            if self.text == '':
                yield "Looks like I don't have any text!\nPrint 'help' for more information."
                return
            cmds = message.split()
            if len(cmds) < 2:
                yield "The title cannot be empty."
                return
            self.storage.save_text(sender, self.text, cmds[1])
            yield "Saved " + "'" + cmds[1] + "'"

        elif cmd == '/share':
            cmds = message.split()
            if len(cmds) < 2:
                yield "The title cannot be empty."
                return
            self.storage.share_text(sender, cmds[1])
            yield "Shared."


        elif cmd == '/load':
            cmds = message.split()
            if len(cmds) < 2:
                yield "The title cannot be empty."
                return
            t = self.storage.load_text(sender, cmds[1])
            if len(t) < 1:
                yield "The text could not be found."
                return
            self.text = t
            yield "Text loaded."

        elif cmd == '/save_all':
            self.storage.save()
            yield "Saved."

        elif cmd == '/translate':
            cmds = message.split()
            if len(cmds) < 2:
                yield "Please specify the language."
                return
            lang = cmds[1]
            if lang not in self.translation_engine.langs:
                yield "Unavailable translation language.\nSee '/tr_langs' for available languages."
                return
            if self.text == '':
                yield "Looks like I don't have any text!\nPrint 'help' for more information."
                return
            try:
                translation = self.translation_engine.translate(self.text, lang)
                yield translation['text'][0]
            except YandexTranslateException:
                yield "Translation error occurred."

        elif cmd == '/titles':
            yield "Available texts:\n" + ", ".join(self.storage.titles(sender))
        elif cmd == '/languages':
            yield "Available translation languages:\n" + ', '.join(sorted(self.translation_engine.langs))

        elif cmd == '/hi':
            yield "Hi!"

        elif cmd == '/help':
            yield 'help'

        else:
            yield 'Command was not detected.\nType "/help" for more information.'