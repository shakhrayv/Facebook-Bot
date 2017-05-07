import nltk
import storage
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
from translation_api import *
import os
import logging
logging.basicConfig(filename="info.log", filemode='w', level=logging.DEBUG)


# Private keys
yandex_api_key = 'trnsl.1.1.20170504T161543Z.1ce6778cb7154603.5f9dbe3d943c4486d33bf509831868ce1f10bdc8'
word_tokenizer = RegexpTokenizer(r'\w+')


def prettify(array, top):
    filter(lambda elem: elem not in ['', ' ', '\n'], array)
    array = array[:top]
    return '\n'.join(map(lambda elem: "{} -> {}".format(elem[0], elem[1]), array))


def check_similarity(word, sample):
    for index, symbol in enumerate(word):
        if index > len(sample) or (symbol != '?' and sample[index] != '?' and symbol != sample[index]):
            return False
    return True if len(sample) == len(word) else False


class Bot:
    def __init__(self):
        logging.info("Bot initialized.")
        self.text = ''
        self.storage = storage.Storage()
        self.translation = None
        self.translation_engine = YandexTranslate(yandex_api_key)

    def execute(self, message, sender):
        logging.info("\nSender: {}\nMessage: {}".format(sender, message))
        cmd = message.split()[0].lower()

        if cmd == 'text':
            if len(message) <= len(cmd) + 1:
                yield "Looks like you forgot to enter the text!\nPrint 'help' for more information."
            else:
                self.text = message[len(cmd) + 1:]
                yield 'Got it!'

        elif cmd == 'word_count':
            if self.text == '':
                yield "Looks like I have no text to analyze!\nPrint 'help' for more information."
            else:
                yield str(len(word_tokenizer.tokenize(self.text)))

        elif cmd == 'sym_count':
            if self.text == '':
                yield "Looks like I have no text to analyze!\nPrint 'help' for more information."
            else:
                yield str(len(self.text))

        elif cmd == 'clear':
            self.text = ''
            try:
                self.storage.clear(sender)
                yield "Cleared!"
            except:
                logging.error("Database error.")
                yield "Database error."

        elif cmd == 'guess':
            if self.guess_by_frequency():
                yield self.text
            else:
                yield "Could not guess due to internal error."

        elif cmd == 'download':
            link = message[len(cmd) + 1:]
            try:
                f = requests.get(link).text
                soup = BeautifulSoup(f, "html.parser")
                self.text = soup.get_text()
                yield 'Download successful.'
            except ConnectionError as conn_e:
                logging.warning("Connection error: {}".format(conn_e.strerror))
                yield "Connection error."
            except TimeoutError as time_e:
                logging.warning("Connection timeout: {}".format(time_e.strerror))
                yield "Connection timeout."
            except Exception as exc:
                logging.warning("Loading error.")
                yield "Could not load page."

        elif cmd == 'word_freq':
            if self.text == '':
                yield "Looks like I have no text to analyze!\nPrint 'help' for more information."
            else:
                top = 5
                try:
                    top = int(message.split()[1])
                except:
                    logging.warning("Incorrect input.")
                yield prettify(nltk.FreqDist(word_tokenizer.tokenize(self.text)).most_common(top + 3), top)

        elif cmd == 'get_text':
            if self.text == '':
                yield "Looks like I don't have any text!\nPrint 'help' for more information."
            else:
                yield self.text

        elif cmd == 'save':
            words = message.split()
            if self.text == '':
                yield "Looks like I don't have any text!\nPrint 'help' for more information."
            elif len(words) < 2:
                yield "The title cannot be empty."
            else:
                try:
                    self.storage.save_text(sender, self.text, words[1])
                    yield "'{}' was successfully saved.".format(words[1])
                except:
                    logging.error("Could not save text")
                    yield "Database error"

        elif cmd == 'share':
            words = message.split()
            if len(words) < 2:
                yield "The title cannot be empty."
            else:
                try:
                    self.storage.share_text(sender, words[1])
                    yield "'{}' was successfully shared.".format(words[1])
                except:
                    logging.error("Could not share text")
                    yield "Database error"

        elif cmd == 'load':
            words = message.split()
            if len(words) < 2:
                yield "The title cannot be empty."
                return
            try:
                text = self.storage.load_text(sender, words[1])
                if not text:
                    yield "Text could not be found."
                else:
                    self.text = text
                    yield "Loaded text: {}".format(self.text)
            except:
                logging.error("Could not load text")
                yield "Database error"

        elif cmd == 'translate':
            words = message.split()
            if len(words) < 2:
                yield "Please specify the language."
            elif words[1] not in self.translation_engine.langs:
                yield "Unavailable translation language.\nSee 'languages' for available languages."
            elif self.text == '':
                yield "Looks like I don't have any text!\nPrint 'help' for more information."
            else:
                try:
                    translation = self.translation_engine.translate(self.text, words[1])
                    self.text = translation['text'][0]
                    yield translation['text'][0]
                except YandexTranslateException:
                    logging.warning("Translation error.")
                    yield "Translation error occurred"

        elif cmd == 'titles':
            try:
                titles = self.storage.titles(sender)

                if titles and len(titles) > 0:
                    yield "Available texts:\n{}".format(', '.join(titles))
                else:
                    yield "No texts available."
            except:
                logging.error("Could not show titles.")
                yield "No"

        elif cmd == 'languages':
            yield "Available translation languages:\n {}".format(', '.join(sorted(self.translation_engine.langs)))

        elif cmd == 'help':
            yield '''
>text <STRING>  
Add the <STRING> parameter as a text

>download <LINK>
Download text from <LINK>

>guess
Mines the text and guesses the words with '?' symbol based on its frequency.

>translate <LANG>
Translate current text into <LANG> language

>languages
Show available languages

>save <TITLE>
Save the current text with the <TITLE> for current user

>share <TITLE>
Shared the text with <TITLE> with all users

>load <TITLE>
Load the text with title <TITLE> for current user

>save_all
Saves all articles for the next session

>word_count
Count the number of words

>sym_count
Count the number of symbols

>word_freq <TOP>
Get <TOP> most frequent words
 '''
        else:
            yield "Command was not detected.\nType 'help' for more information."

    def guess_by_frequency(self):
        input_data = None
        words = None
        to_replace = {}
        try:
            with open(os.path.join(os.path.dirname(__file__), "Lingvo/wordlist.txt"), 'r') as words_file:
                input_data = words_file.read().split()
                words = self.text.split()
        except FileNotFoundError:
            logging.critical("Wordlist could not be found.")
            return False
        frequencies = nltk.FreqDist(words).most_common(len(words))

        # Choosing to replace an element where needed.
        for elem in frequencies:
            word = elem[0]
            if word in to_replace.keys() or '?' not in word:
                continue

            for sample_word in input_data:
                if check_similarity(word, sample_word):
                    to_replace[word] = sample_word
                    break

        # Replacing
        for i in range(len(words)):
            if words[i] in to_replace.keys():
                words[i] = to_replace[words[i]]
        text = nltk.Text(words)
        self.text = nltk.Text(words).name[:-3]
        return True