from parser_city import main, list_of_cities
from check_city import check_this_city
import telebot
from telebot import types
import random

TOKEN = "6944890003:AAHfjSue5XBWpvqmrwtDsK3BSNf5N7bupC4" 
bot = telebot.TeleBot(TOKEN)
game_over = False #глобальная переменная проверки на то, закончилась ли игра
total_score = [0, 0] #глобальная переменна счета. 1 число - текущий счет, 2 число - лучший результат
level = 'low'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item4 = types.KeyboardButton('new game')
    item1 = types.KeyboardButton('score')
    item3 = types.KeyboardButton('level')
    item5 = types.KeyboardButton('give up')
    item2 = types.KeyboardButton('info')

    markup.add(item1,item2, item3, item4, item5)

    hello = "Привет!\nЯ бот для игры в Города.\n\nЕсли хотите начать игру, пришлите мне команду new game!"
    
    bot.send_message(message.chat.id, hello.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_messege(message):
    global game_over
    global total_score
    global level

    if message.text == 'give up':
        bot.reply_to(message, "Тогда я выиграл! \nЕсли хотите начать игру, пришлите мне команду new game!")
        game_over = True
        if total_score[0] > total_score[1]:
            total_score[1] = total_score[0]
            total_score[0] = 0
        else:
            total_score[0] = 0
        return
    
    elif message.text == 'new game':
        game_over = False
        if total_score[0] > total_score[1]:
            total_score[1] = total_score[0]
            total_score[0] = 0
        else:
            total_score[0] = 0
        list_of_cities.clear() #список городов
        bot.reply_to(message, "Назовите любой город!")
        return

    elif message.text == 'info':
        bot.reply_to(message, "Привет! Это тг-бот, игра в 'города' \nОт студента ФГИиБ ИСиТ 3-1б Шункова П.А. \n\nПравила очень просты! - называете город \nна последюю букву предыдущего, \nи пробуете переиграть моего бота) \nВыиграйте, сделав как можно меньше ходов! \nУдачи! 🔥🔥🔥🔥")
        return
    
    elif message.text == 'score':
        if total_score[0] > total_score[1]:
            total_score[1] = total_score[0]
            bot.reply_to(message, f"Ваш текущий счет:  {total_score[0]}\nВаш лучший счет/рекорд:  {total_score[0]}")
        else:
            bot.reply_to(message, f"Ваш текущий счет:  {total_score[0]}\nВаш лучший счет/рекорд:  {total_score[1]}")
        return
    
    elif message.text == 'level':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item6 = types.KeyboardButton('low')
        item7 = types.KeyboardButton('mid')
        item8 = types.KeyboardButton('hard')
        item9 = types.KeyboardButton('exit')
        item10 = types.KeyboardButton('what? levels?')
        
        markup.add(item6,item7, item8, item9, item10)
        bot.send_message(message.chat.id, f'ваш уровень: {level}', reply_markup=markup)

    elif message.text == 'what? levels?':
        bot.reply_to(message, "да! Это уровни игры в 'города' \n\nправила просты: \n-low - играем в классику на последнюю букву \n-mid - играем на предпоследнюю букву \n-hard - вы что тут делаете? как вы, так и бот, \nдолжны угадывать слово на рандомную букву)))")
        return
    
    elif message.text == 'low':
        level = 'low'
        bot.reply_to(message, "Вы выбрали легкий уровень, удачи!")
        return
    
    elif message.text == 'mid':
        level = 'mid'
        bot.reply_to(message, "Вы выбрали средний уровень, удачи!")
        return 
    
    elif message.text == 'hard':
        level = 'hard'
        bot.reply_to(message, "Вы выбрали ,безумный уровень, удачи!")
        return 

    elif message.text == 'exit':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item4 = types.KeyboardButton('new game')
        item1 = types.KeyboardButton('score')
        item3 = types.KeyboardButton('level')
        item5 = types.KeyboardButton('give up')
        item2 = types.KeyboardButton('info')
        markup.add(item1,item2, item3, item4, item5)

        hello = "И снова здравствуйте! \nУстраивает ваш уровень? Ну чтож...\nЕсли хотите начать игру, пришлите мне команду new game!"
        bot.send_message(message.chat.id, hello, reply_markup=markup)

    else:
        get_city(message)
        return


@bot.message_handler(content_types=['text'])
def get_city(message):
    global game_over
    global total_score
    global level

    """
    Я перевожу все города в нижний регистр для того, чтоб сохранять их в список и удобнее
    сравнивать с теми, что уже были. Из-за этого нет привязки к тому, как пользователь напишет название: 
    с большой буквы, капсом и т.д.
    """
    print(message.from_user.first_name)
    print(message.text)

    if game_over == True:
        #bot_messege(message)
        bot.reply_to(message, "Если хотите начать новую игру, используйте специальную команду new game")
        return

    if message.text.lower() == "не знаю":
        bot.reply_to(message, "Тогда я выиграл!")
        if total_score[0] > total_score[1]:
            total_score[1] = total_score[0]
            total_score[0] = 0
        else:
            total_score[0] = 0
        game_over = True
        return
    
    #помещаю в нижний кейс слово юзера для проверки
    users_word = message.text.lower()

    #отделяем букву в соответствии с уровнем сложности
    if list_of_cities:
        letter = ''

        if level == 'low':
            if list_of_cities[-1][-1] == "ь" or list_of_cities[-1][-1] == "ъ":#если последняя буква это ь или ъ
                letter = list_of_cities[-1][-2] #то надо называть город на предпоследнюю
            else:
                letter = list_of_cities[-1][-1]
            
        elif level == 'mid':
            if list_of_cities[-1][-1] == "ь" or list_of_cities[-1][-1] == "ъ":#если последняя буква это ь или ъ
                letter = list_of_cities[-1][-3] #то надо называть город на предпоследнюю
            else:
                letter = list_of_cities[-1][-2]

        elif level == 'hard':
            crazy = random.randint(0, len(list_of_cities[-1]))
            print(crazy, len(list_of_cities[-1]))
            letter = list_of_cities[-1][crazy-1] 
        

        #проверка правильности слова юзера
        if users_word[0] != letter:
            bot.reply_to(message, f"ОШИБКА! Введите название города, которое начинается на {letter.upper()} , \nПоследнее слово: {list_of_cities[-1]}")
            if total_score[0] > total_score[1]:
                total_score[1] = total_score[0]
            total_score[0] -= 1 
            return


    # проверка на то, есть ли такой город, какой назвал юзер
    checking_the_city = check_this_city(users_word)

    if not checking_the_city:
        bot.reply_to(message, "ОШИБКА! Введите корректное название города!\nЕсли вы хотите сдаться, то просто напишите \"не знаю\".")
        if total_score[0] > total_score[1]:
                total_score[1] = total_score[0]
        total_score[0] -= 1
        return
    
    # проверка на то, был ли такой город    
    for i in list_of_cities:
        if i == users_word:
            bot.reply_to(message, "ОШИБКА! Этот город уже был назван!")
            if total_score[0] > total_score[1]:
                total_score[1] = total_score[0]
            total_score[0] -= 1
            return
            
    total_score[0] += 1 # прибавляем текущий счет
    #помещаю город, названный пользователем в список
    list_of_cities.append(users_word)
    print(list_of_cities)

    #если последняя буква это ь или ъ, то надо найти город на предпоследнюю
    #тоже в соответствии с уровнем
    if level == 'low':
        if message.text[-1].upper() == "Ь" or message.text[-1].upper() == "Ъ":
            city = main(message.text[-2].upper())
        else:
            city = main(message.text[-1].upper())

    elif level == 'mid':
        if message.text[-1].upper() == "Ь" or message.text[-1].upper() == "Ъ":
            city = main(message.text[-3].upper())
        else:
            city = main(message.text[-2].upper())
        
    elif level == 'hard':
        crazy = random.randint(0, len(list_of_cities[-1]))
        print(crazy, len(list_of_cities[-1]))
        city = main(message.text[crazy-1].upper())


    if city == None:
        bot.reply_to(message, "Я не знаю больше городов, вы выиграли!")
        game_over = True
        return
    
    bot.reply_to(message, city)

bot.polling()
