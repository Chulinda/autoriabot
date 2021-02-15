import requests
from bs4 import BeautifulSoup
import telebot
from time import sleep
from random import choice


bot = telebot.TeleBot('1653586848:AAG32NGn83Q0Gti4s7Mjcs36flQimirMOyU')


user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
user_agent = choice(user_agent_list)

headers = {'User-Agent': user_agent}


def get_cars(number_of_cars, url):
    global links
    links = []
    print('//////////////////// URL =  ', url)
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, 'lxml')
    sections = soup.find_all('section',class_ = 'ticket-item new__ticket t' )

    for section in sections:
        link = section.find('div', class_ ='item ticket-title').find('a').get('href')
        links.append(link)
    links = links[0:number_of_cars]



@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'привет')

@bot.message_handler(commands=["search_link"])
def link(message):
    msg = bot.send_message(message.chat.id, 'Введите ссылку')
    bot.register_next_step_handler(msg, search)




    
@bot.message_handler(content_types=["text"])
def main(message):
    global url
    numbers = int(message.text)
    get_cars(numbers, url)
    for i in links:
        bot.send_message(message.chat.id, i)
def search(message):
    global url 
    url = message.text
    
    
if __name__ == '__main__':
    bot.polling(none_stop=True)
