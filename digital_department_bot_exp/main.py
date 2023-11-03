import datetime
import telebot
from telebot import types
import threading


def logging(source):
    log = open('log.txt', 'a')
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    log.write(source + ' ' + dt_string + '\n')
    log.close()
def bot_thread(BOT_TOKEN, csvName):
    # Создаем экземпляр бота
    #BOT_TOKEN = '6505669102:AAFhHUU6ZAlnLlFHNlGMABu3dKk-Z4AzdD8'
    bot = telebot.TeleBot(BOT_TOKEN)

    # Читаем FAQ из текстового файла
    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            faq_text = file.read()
        return faq_text

    # Путь к файлу с FAQ
    # faq_file_path = 'faq.txt'
    # faq_text = read_file(faq_file_path)

    duty_officer_path = 'duty_officer.txt'
    duty_officer_text = read_file(duty_officer_path)

    import pandas as pd

    teachers_path = csvName
    teachers = pd.read_csv(teachers_path)

    # Обработчик команды /start
    @bot.message_handler(commands=['start'])
    def start(message):
        # Создаем клавиатуру с кнопками
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        faq_button = types.KeyboardButton('FAQ')
        department_duty_button = types.KeyboardButton('Задать вопрос дежурному')
        subject_question_button = types.KeyboardButton('Задать вопрос по предмету')
        keyboard.add(faq_button, department_duty_button, subject_question_button)

        # Отправляем приветственное сообщение с клавиатурой
        bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=keyboard)


    subsections = ['Сроки обучения', 'Практика', 'Расписание', 'Ассесмент', 'Оценки', 'Итоговая работа']

    # Обработчик кнопки "FAQ"
    @bot.message_handler(func=lambda message: message.text == 'FAQ')
    def faq(message):
        #Cоздаём клавиатуру
        keyboard = types.ReplyKeyboardMarkup(row_width=3)
        buttons = []
        for i in subsections:
            buttons.append(types.KeyboardButton(i))

        for i in buttons:
            keyboard.add(i)

        back_button = types.KeyboardButton('Вернуться в меню')
        keyboard.add(back_button)
        bot.send_message(message.chat.id, 'Выберите подраздел FAQ:', reply_markup=keyboard)
        logging('faq')


    @bot.message_handler(func=lambda message: message.text in subsections)
    def sub_faq(message):
        if message.text == 'Сроки обучения':
            bot.send_message(message.chat.id, read_file('сроки_обучения.txt'))
        elif message.text == 'Практика':
            bot.send_message(message.chat.id, read_file('практика.txt'))
        elif message.text == 'Расписание':
            bot.send_message(message.chat.id, read_file('расписание.txt'))
        elif message.text == 'Ассесмент':
            bot.send_message(message.chat.id, read_file('ассесмент.txt'))
        elif message.text == 'Оценки':
            bot.send_message(message.chat.id, read_file('оценки.txt'))
        elif message.text == 'Итоговая работа':
            bot.send_message(message.chat.id, read_file('итоговая_работа.txt'))
        logging('faqSub')

    # Обработчик кнопки "Задать вопрос дежурному"
    @bot.message_handler(func=lambda message: message.text == 'Задать вопрос дежурному')
    def duty_officer_question(message):
        # Отправляем ссылку в личку
        bot.send_message(message.chat.id, duty_officer_text)
        logging('dutyOfficer')


    # Обработчик кнопки "Задать вопрос по предмету"
    @bot.message_handler(func=lambda message: message.text == 'Задать вопрос по предмету')
    def subject_question(message):
        # Создаем клавиатуру с предметами
        keyboard = types.ReplyKeyboardMarkup(row_width=3)
        buttons = []
        for i in list(teachers['Предмет'].unique()):
            buttons.append(types.KeyboardButton(i))

        for i in buttons:
            keyboard.add(i)

        back_button = types.KeyboardButton('Вернуться в меню')
        keyboard.add(back_button)
        # Отправляем сообщение с выбором предмета
        bot.send_message(message.chat.id, 'Выберите предмет:', reply_markup=keyboard)
        logging('subjects')


    # Обработчик выбора предмета
    @bot.message_handler(func=lambda message: message.text in list(teachers['Предмет'].unique()))
    def choose_teacher(message):
        # Создаем клавиатуру с преподавателями
        keyboard = types.ReplyKeyboardMarkup(row_width=2)

        teachers_by_subject = teachers[teachers['Предмет'] == message.text]
        list_of_teachers = list(teachers_by_subject["ФИО преподавателя"])
        buttons = []

        for i in list_of_teachers:
            buttons.append(types.KeyboardButton(i))

        for i in buttons:
            keyboard.add(i)

        back_button = types.KeyboardButton('Вернуться в меню')
        keyboard.add(back_button)

        # Отправляем сообщение с выбором преподавателя
        bot.send_message(message.chat.id, 'Выберите преподавателя:', reply_markup=keyboard)
        logging('prof')


    # Обработчик выбора преподавателя
    @bot.message_handler(func=lambda message: message.text in list(teachers['ФИО преподавателя']))
    def send_link(message):
        # Отправляем ссылку в личку
        bot.send_message(message.chat.id, teachers.loc[teachers['ФИО преподавателя'] == message.text, 'ссылка'].values[0])
        logging('profSub')


    # Обработчик кнопки "Вернуться в меню"
    @bot.message_handler(func=lambda message: message.text == 'Вернуться в меню')
    def return_to_menu(message):
        # Создаем клавиатуру с кнопками
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        faq_button = types.KeyboardButton('FAQ')
        department_duty_button = types.KeyboardButton('Задать вопрос дежурному')
        subject_question_button = types.KeyboardButton('Задать вопрос по предмету')
        keyboard.add(faq_button, department_duty_button, subject_question_button)

        # Отправляем сообщение с клавиатурой
        bot.send_message(message.chat.id, 'Вернулись в меню!', reply_markup=keyboard)
        logging('menu')


    # Запускаем бота
    bot.polling()


botKeys = ['6565282500:AAFyLrzYqccz6EC3kpVX4kOB4oUmFGN_gIY', '5819227130:AAFKaqatMV3WJuCUT3GKzGVGbCz-S4WZNz0',
           '6173847622:AAF5rMm6pQHIA5hxzuVyGqSfSTrzT1xEThU', '6494006914:AAGjKZs3Lpcf8g2mqXxau2xMgNwzL6cj9UA']
csvArr = ['teachers0.csv', 'teachers1.csv', 'teachers2.csv', 'teachers3.csv']
T = []
for i in range(4):
    T.append(threading.Thread(target=bot_thread, args=(botKeys[i], csvArr[i],)))
    T[i].start()
