# 7103113019:AAHpKoxvUid7mwpeygfgCcDAxcoJW5G7NBo
import json
import random


import telebot
TOKEN = '7103113019:AAHpKoxvUid7mwpeygfgCcDAxcoJW5G7NBo'

bot=telebot.TeleBot(TOKEN)
try:
    with open('user_data.json','r',encoding='utf-8') as file:
        usert_data=json.load(file)
except FileNotFoundError:
    usert_data={}



@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,'Привеит')



@bot.message_handler(commands=['addword'])
def handle_addword(message):
    global usert_data
    chat_id=message.chat.id
    user_dict=usert_data.get(chat_id,{})
    words=message.text.split()[1:]


    if len(words)==2:
        word,translation=words[0].lower(),words[1].lower()


        user_dict[word]=translation

        usert_data[chat_id]=user_dict

        with open('user_data.json', 'w', encoding='utf-8') as file:
            json.dump(usert_data,file,ensure_ascii=False,indent=4)
        bot.send_message(chat_id,f'слово {word} добавлено в словарь')
    else:
        bot.send_message(chat_id, 'Произошла ошибкаб повторите попытку')


@bot.message_handler(commands=['learn'])
def handle_learn(message):
    user_words=usert_data.get(str(message.chat.id),{})
    try:
        words_number=int(message.text.split()[1])
        ask_translation(message.chat.id,user_words,words_number)

    except:
        bot.send_message(message.chat.id,'Используй команду /learn<кол-во изучения слов>')
def ask_translation(chat_id, user_words, words_left):

    if words_left>0:
        word=random.choice(list(user_words.keys()))
        translation=user_words[word]
        bot.send_message(chat_id,f'Напиши перевод слова{word}')

        bot.register_next_step_handler_by_chat_id(chat_id,check_translation,translation,words_left)
    else:
        bot.send_message(chat_id, 'Слова закончелись')

def check_translation(message,expected_translation,words_left):
    user_translation=message.text.strip().lower()
    if user_translation==expected_translation.lower():
        bot.send_message(message.chat.id,"Правильно")
    else:
        bot.send_message(message.chat.id, f'Неправильно.Правильно:{expected_translation}')
    words_left -= 1
    ask_translation(message.chat.id,usert_data[str(message.chat.id)],words_left)





@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id,'Этот бот был создан в качестве тестового бота'
                                     '\n''Команды /help,/learn,/start'
                                     '\n''Создатель:Лёша')


@bot.message_handler(func=lambda message:True)
def handle_all(message):
    if message.text.lower()=='как тебя зовут?':
        bot.send_message(message.chat.id,'У меня пока нет имени')
    elif message.text.lower()=='расскажи о себе':
        bot.send_message(message.chat.id,'я бот')
    elif message.text.lower()=='расскажи шутку':
        bot.send_message(message.chat.id,'Колобок повесился')






if __name__=='__main__':
    bot.polling(non_stop=True)
