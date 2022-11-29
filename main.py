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
    bot.send_photo(message.chat.id,photo,caption = 'Улыбнитесь:) на Вас смотрит милый котик')

@bot.message_handler(commands=['random_photo'])
def send_random_photo(message):
    image = get(PHOTO_URL).content
    if image:
        keyboard = types.InlineKeyboardMarkup()
        like_button = types.InlineKeyboardButton(text='👍',callback_data='like')
        keyboard.add(like_button)
        dislike_button = types.InlineKeyboardButton(text='👎',callback_data='dislike')
        keyboard.add(dislike_button)
        bot.send_photo(message.from_user.id,image,caption = 'Вам нравится это фото?',reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    likes = 0
    dislikes = 0
    with open('like.txt','r') as file:
        for line in file:
            likes = int(line[0].rstrip())
    with open('dislike.txt','r') as data:
        for lines in data:
            dislikes = int(lines[0].rstrip())
    if call.data == 'like':
        likes += 1
        doc = open('like.txt','w')
        doc.write(str(likes))
        bot.send_message(call.message.chat.id,f'Еще {likes} людям понравилось это фото' )
    elif call.data == 'dislike':
        dislikes += 1
        doc1 = open('dislike.txt','w')
        doc1.write(str(dislikes))
        bot.send_message(call.message.chat.id,f'Еще {dislikes} людям не понравилось это фото' )


@bot.message_handler(commands=['random_people'])
def send_random_people(message):
    image = get(PEOPLE_URL).content
    if image:
        keyboard = types.InlineKeyboardMarkup()
        like_button = types.InlineKeyboardButton(text='👍',callback_data='like')
        keyboard.add(like_button)
        dislike_button = types.InlineKeyboardButton(text='👎',callback_data='dislike')
        keyboard.add(dislike_button)
        bot.send_photo(message.from_user.id,image,caption = 'Вам нравится это фото?',reply_markup=keyboard)
            
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    likes = 0
    dislikes = 0
    with open('like.txt','r') as file:
        for line in file:
            likes = int(line[0].rstrip())
    with open('dislike.txt','r') as data:
        for lines in data:
            dislikes = int(lines[0].rstrip())
    if call.data == 'like':
        likes += 1
        doc = open('like.txt','w')
        doc.write(str(likes))
        bot.send_message(call.message.chat.id,f'Еще {likes} людям понравилось это фото' )
    elif call.data == 'dislike':
        dislikes += 1
        doc1 = open('dislike.txt','w')
        doc1.write(str(dislikes))
        bot.send_message(call.message.chat.id,f'Еще {dislikes} людям не понравилось это фото' )
bot.polling()
