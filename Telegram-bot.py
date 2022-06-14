import random

import telebot
from khayyam import JalaliDate
from gtts import gTTS
#import qrcode

mybot = telebot.TeleBot('2039927554:AAFrqwyUmMSrd3F_Q6n3LA9s0piw8ZknSvs')

@mybot.message_handler(commands= ['start'])
def send_welcome(message):
    mybot.reply_to(message, f'Hi {message.from_user.first_name}, Welcome to my bot.')
    mybot.send_message(message.chat.id, 'Please send /help if you need help.')

@mybot.message_handler(commands= ['game'])
def play_game(message):
    mybot.reply_to(message, 'guess number between 0-20')
    mybot.register_next_step_handler(message, game) 

mybot.number = random.randint(0, 20)

def game(message):
    if message.text.startswith("/"):
        mybot.send_message(message.chat.id, 'agein send your command.')
    else:
        mymarkup = telebot.types.ReplyKeyboardMarkup(row_width= 1)
        btn1 = telebot.types.KeyboardButton('New Game')
        mymarkup.add(btn1)
        if message.text == 'New Game':
            mybot.number = random.randint(0, 20)
            mes = mybot.send_message(message.chat.id, 'guess new number between 0-20', reply_markup= telebot.types.ReplyKeyboardRemove(selective=True))
            mybot.register_next_step_handler(mes, game)
        elif int(message.text) == mybot.number:
            mybot.reply_to(message, 'Yesss. You Win! ')
            mybot.number = random.randint(0, 20)
            mes = mybot.send_message(message.chat.id, 'if want new game press New Game', reply_markup = mymarkup )
            mybot.register_next_step_handler(mes, game)
        elif int(message.text) < mybot.number:
            mes = mybot.reply_to(message, 'No! guess higher.')
            mybot.register_next_step_handler(mes, game)
        elif int(message.text) > mybot.number:
            mes = mybot.reply_to(message, 'No! guess lower. ')
            mybot.register_next_step_handler(mes, game)
        else:
            mybot.reply_to(message, 'Are you okey?! what are you saying?! ')
        
    
@mybot.message_handler(commands= ['age'])
def show_age(message):
    mybot.reply_to(message, 'Tell me your date of birth (yyyy/mm/dd) to tell you how old are you.')
    mybot.register_next_step_handler(message, ages)

def ages(message):
    date = message.text.split('/')
    difference = JalaliDate.today() - JalaliDate(int(date[0]), int(date[1]), int(date[2]))
    age = {}
    age[0] = difference.days // 365
    if 1 <= int(date[1]) <= 6:
        age[1] = (difference.days % 365 ) // 33
        age[2] = (difference.days % 365) % 33 - 5
    elif 7 <= int(date[1]) <= 11:
        age[1] = (difference.days % 365 ) // 31
        age[2] = (difference.days % 365) % 31 + 1
    elif int(date[1]) == 12:
        age[1] = (difference.days % 365 ) // 30
        age[2] = (difference.days % 365) % 30

    mybot.send_message(message.chat.id, f'you are {age[0]} year {age[1]} month {age[2]} day')

@mybot.message_handler(commands= ['voice'])
def play_voice(message):
    mybot.reply_to(message, 'Type a sentence so I can send it to you as a voice.')
    mybot.register_next_step_handler(message, voice)

def voice(message):
    mytext = message.text
    language = 'en'
    myobj = gTTS(text= mytext, lang= language, slow= False)
    myobj.save('voice.mp3')
    voice = open('voice.mp3','rb')
    mybot.send_voice(message.chat.id, voice= voice)

@mybot.message_handler(commands= ['max'])
def show_max(message):
    mybot.reply_to(message, 'Enter a list of numbers (n1,n2,...) to say the largest number. ')
    mybot.register_next_step_handler(message, max_num)

def max_num(message):
    mytext = message.text.split(',')
    nums = []
    for i in mytext:
        nums.append(int(i))
    mybot.send_message(message.chat.id, f'Maximum num in your list is : {max(nums)}')

@mybot.message_handler(commands= ['argmax'])
def show_arg_max(message):
    mybot.reply_to(message, 'Enter a list of numbers (n1,n2,...) to say the argument of the largest number. ')
    mybot.register_next_step_handler(message, arg_max_num)

def arg_max_num(message):
    mytext = message.text.split(',')
    nums = []
    for i in mytext:
        nums.append(int(i))
    mybot.send_message(message.chat.id, f'Arg of the max num in your list is : {nums.index(max(nums))}')

# @mybot.message_handler(commands= ['qrcode'])
# def send_qrcode(message):
#     mybot.reply_to(message, 'Enter a sentence so l can make the qrcode ')
#     mybot.register_next_step_handler(message, make_qrcode)

# def make_qrcode(message):
    #img = qrcode.make(message.text)
    #img.save('qrcode.png')
    # image = open('qrcode.png', 'rb')
    # mybot.send_photo(message.chat.id, image)

@mybot.message_handler(commands= ['help'])
def show_max(message):
    mybot.reply_to(message, 'Plese send:\n/game if you want help\n/age if you wanna know your age.\n/voice if you want to change your sentence to voice\n/max if you want to the largest number\n/argmax if you want to argument of the largest number')

mybot.polling()