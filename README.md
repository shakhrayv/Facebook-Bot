# Facebook-Bot

## Prerequisites
The **Facebook Bot for Facebook Messenger** helps you organize, analyze, translate and share any kind of text or messages.<br>
<br>The project was created as part of the home assignment during the Python course at MIPT University.
<br> The code was written by Vladislav Shakhray.<br>The program is licensed under the terms of GNU Public License.
<br><br>
## Requirements
1. Python 3.4.1 or later
> Note: the bot was tested using Python 3.6.0
2. Python modules: [Flask](http://flask.pocoo.org) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/#Download)
3. [nltk](http://www.nltk.org/install.html) and [nltk data](http://www.nltk.org/data.html)
4. [ngrok](https://ngrok.com/download)

## Usage
<br>
*Important:*In order to communicate with the bot, go to its [Facebook Page](https://www.facebook.com/mipt.bot) and write it a message.<br><br>
The bot accepts the commands as a Facebook Messenger message.<br>
The following commands are available:
* **```text <STRING>```**  <br> Add the **```<STRING>```** parameter as a text<br><br>
* **```download <LINK>```**<br>Download text from **```<LINK>```**<br><br>
* **```guess```**<br>Mines the text and guesses the words with '?' symbol based on its frequency.<br><br>
* **```translate <LANG>```**<br>Translate current text into  ```<LANG>``` language<br><br>
* **```languages```**<br>Show available languages<br><br>
* **```save <TITLE>```**<br>Save the current text with the **```<TITLE>```** for current user<br><br>
* **```share <TITLE>```**<br>Shared the text with **```<TITLE>```** with all users<br><br>
* **```load <TITLE>```**<br>Load the text with title **```<TITLE>```** for current user<br><br>
* **```save_all```**<br>Saves all articles for the next session<br><br>
* **```word_count```**<br>Count the number of words<br><br>
* **```sym_count```**<br>Count the number of symbols<br><br>
* **```word_freq <TOP>```**<br>Get **```<TOP>```** most frequent words<br><br>
* **```sym_freq <TOP>```**<br>Get **```<TOP>```** most frequent symbols<br><br>
* **```help```**<br>Echo help<br><br>

## Screenshots
<img src="https://ibin.co/3LKoNy8rzeWD.jpg" width="220"/> <img src="https://ibin.co/3LKp2rydacB3.jpg" width="220"/> 
