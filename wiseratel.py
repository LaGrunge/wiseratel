import telebot
import random
import os


bot = telebot.TeleBot(os.environ['WISERATEL_TOKEN'])

words = dict()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ну давай начинать')

@bot.message_handler(content_types=['text'])
def send_text(message):
    text = message.text.lower()
    if text == 'привет':
        bot.send_message(message.chat.id, f'Привет {message.from_user.username}')
    elif text == 'пока':
        bot.send_message(message.chat.id, f'Пока {message.from_user.username}')
    elif text == 'слово':
        word, article = random.choice(list(words.items()))
        bot.send_message(message.chat.id, f'{word.upper()} :  {article}')
    elif text == 'статистика':
        bot.send_message(message.chat.id, f'Я знаю {len(words)} словарных статей')
    elif text == 'набор':
        markup = telebot.types.InlineKeyboardMarkup()
        samples = random.sample(list(words.keys()), 10)
        buttons = [telebot.types.InlineKeyboardButton(text=sample.capitalize(), callback_data='add') for sample in samples]
        for button in buttons:
            markup.add(button)
        bot.send_message(message.chat.id, text="Выбирай", reply_markup=markup)
    elif text.startswith('ищи') and len(text) > 4:
        word = message.text[4:].upper()
        if word in words:
            bot.send_message(message.chat.id, f'{word.upper()} :  {words[word]}')
        else:
            bot.send_message(message.chat.id, f'Не знаю, что такое {word.upper()}')

def main():
    words_counter = 0
    with open("data.txt") as data:
        word, article= None, None
        for line in data:
            if len(line) < 2:
                continue

            if "@" in line:
                if word and article:
                    words[word]=article
                    words_counter += 1
                    article = None

                parts = line.split("@")
                ambule = parts[0].split()
                word = " ".join([word.strip("\"...«»'?.,…") for word in ambule if word.isupper()])
                article = parts[1]
            elif word:
                article += line
        print (f"\r{words_counter} loaded")
    
    bot.polling()

main()