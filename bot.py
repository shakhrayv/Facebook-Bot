import nltk
import requests
from storage import Storage
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup

word_tokenizer = RegexpTokenizer(r'\w+')

class Bot:
    def __init__(self):
        print("INITIALIZED")
        self.text = ''
        self.storage = Storage()

    def execute(self, message, sender):
        cmd = message.split()[0]

        if cmd == '/text':
            if len(message) <= 6:
                return "Looks like you forgot to enter the text!\nPrint 'help' for more information."
            self.text = message[6:]
            return 'Got it!'

        elif cmd == '/word_count':
            if self.text == '':
                return "Looks like I have no text to analyze!\nPrint 'help' for more information."
            return str(len(word_tokenizer.tokenize(message)))

        elif cmd == '/sym_count':
            if self.text == '':
                return "Looks like I have no text to analyze!\nPrint 'help' for more information."
            return str(len(message))

        elif cmd == '/clear':
            self.text = ''
            self.storage.clear(sender)
            return "Cleared!"

        elif cmd == '/quit' or cmd == '/exit':
            self.storage.save()
            return ['Bye bye!'], 1

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
                return 'An error occurred during the connection attempt.\nPlease try again.'

        elif cmd == '/word_freq':
            if self.text == '':
                return "Looks like I have no text to analyze!\nPrint 'help' for more information."
            return str(nltk.FreqDist(word_tokenizer.tokenize(self.text)).most_common(5))

        elif cmd == '/get_text':
            if self.text == '':
                return "Looks like I don't have any text!\nPrint 'help' for more information."
            return self.text[:640]

        elif cmd == '/save':
            if self.text == '':
                return "Looks like I don't have any text!\nPrint 'help' for more information."
            cmds = message.split()
            if len(cmds) < 2:
                return "The title cannot be empty."
            self.storage.save_text(sender, self.text, cmds[1])
            return "Saved " + "'" + cmds[1] + "'"

        elif cmd == '/share':
            cmds = message.split()
            if len(cmds) < 2:
                return "The title cannot be empty."
            self.storage.share_text(sender, cmds[1])
            return "Shared."

        elif cmd == '/load':
            cmds = message.split()
            if len(cmds) < 2:
                return "The title cannot be empty."
            t = self.storage.load_text(sender, cmds[1])
            if len(t) < 1:
                return "The text could not be found."
            self.text = t
            return "Text loaded."

        elif cmd == '/save_all':
            self.storage.save()
            return "Saved."

        elif cmd == '/help':
            return '''
                    /text <STRING>
                    Add the <STRING> parameter as a text


                     /save <TITLE>
                    Save the current text with the <TITLE> for current user


                     /share <TITLE>
                    Shared the text with <TITLE> with all users


                     /load <TITLE>
                    Load the text with title <TITLE> for current user


                     /download <LINK>
                    Download text from <LINK>


                     /word_count
                    Count the number of words


                     /sym_count
                    Count the number of symbols


                     /word_freq <TOP>
                    Get <TOP> most frequent words


                     /sym_freq <TOP>
                    Get <TOP> most frequent symbols


                     /exit and /quit
                    Quit bot with saving


                     /save_all
                    Saves all articles for the next session


                     /help
                    Echo help
            '''


