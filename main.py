from requests import *
import random
from bs4 import BeautifulSoup as b
from telebot import *


URL ='https://www.anekdot.ru/last/good'
PHOTO_URL = 'https://picsum.photos/1200'
PEOPLE_URL = 'https://thispersondoesnotexist.com/image'
API_TOKEN = '5975641715:AAGoga7BL8_WK568msjmqE-s8rAUHXs4Vr0'
def parsing(url):
    r = get(url)
    soup = b(r.text,'html.parser')
    anecdots = soup.find_all('div',class_='text')#ищем все необходимые тэги 
    return [i.text for i in anecdots]

jokes = parsing(URL)
# random.shuffle(jokes)

bot = TeleBot(API_TOKEN)
@bot.message_handler(commands=['start'])
def hello_user(message):
    new_mess = f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b> .Чтобы увидеть список всех команд, напишите команду /help'
    bot.send_message(message.chat.id,new_mess,parse_mode='html')

@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Посетить вебсайт",url ='https://www.anekdot.ru/last/good'))
    bot.send_message(message.chat.id,'Если хотите посмотреть все анекдоты, переходите на вебсайт',reply_markup=markup)

@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    website = types.KeyboardButton('/website')
    start = types.KeyboardButton('/start')
    joke = types.KeyboardButton('/jokes')
    photos = types.KeyboardButton('/photo')
    random_photos = types.KeyboardButton('/random_photo')
    random_people = types.KeyboardButton('/random_people')
    markup.add(website,start,joke,photos,random_photos,random_people)
    bot.send_message(message.chat.id,'Здесь есть все возможные команды',reply_markup=markup)

@bot.message_handler(commands=['jokes'])
def give_jokes(message):
    random.shuffle(jokes)
    bot.send_message(message.chat.id,jokes[0])
    del jokes[0]

@bot.message_handler(commands=['photo'])
def give_photo(message):
    photo = open('kotik.jpg','rb')
    bot.send_photo(message.chat.id,photo)

@bot.message_handler(commands=['random_photo'])
def send_random_photo(message):
    image = get(PHOTO_URL).content
    if image:
        keyboard = types.InlineKeyboardMarkup()
        like_button = types.InlineKeyboardButton(text='👍',callback_data='like')
        keyboard.add(like_button)
        dislike_button = types.InlineKeyboardButton(text='👎',callback_data='dislike')
        keyboard.add(dislike_button)
        bot.send_photo(message.from_user.id,image,reply_markup=keyboard)


@bot.message_handler(commands=['random_people'])
def send_random_people(message):
    image = get(PEOPLE_URL).content
    if image:
        keyboard = types.InlineKeyboardMarkup()
        like_button = types.InlineKeyboardButton(text='👍',callback_data='like')
        keyboard.add(like_button)
        dislike_button = types.InlineKeyboardButton(text='👎',callback_data='dislike')
        keyboard.add(dislike_button)
        bot.send_photo(message.from_user.id,image,reply_markup=keyboard)
    
def get_likes_and_dislikes(message):
    query = message.data

bot.polling()

# @bot.message_handler(content_types=['text'])
# def get_user_text(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.chat.id,'Доброго дня!',parse_mode='html')
#     elif 'фото' in message.text:
#         photo = open('kotik.jpg','rb')
#         bot.send_photo(message.chat.id,photo)
#     elif message.text.lower() in '123456789':
#         bot.send_message(message.chat.id,jokes[0])
#         del jokes[0]
#     else:
#         bot.send_message(message.chat.id,'Я тебя не понимаю',parse_mode='html')


# @bot.message_handler(content_types=['photo'])#когда мы не знаем, какую команду введет пользователь
# def get_photo(message):
#     bot.send_message(message.chat.id,'Отличное фото!')

