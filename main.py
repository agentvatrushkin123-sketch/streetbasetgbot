import telebot
import os
from telebot import types
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("Ошибка: BOT_TOKEN не найден!")
    print("Создайте файл .env с BOT_TOKEN=ваш_токен")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

mp = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
item1 = types.KeyboardButton('🚚Как заказать?')
item2 = types.KeyboardButton('🎯Отзывы')
item3 = types.KeyboardButton('📲Связь с менеджером')
item4 = types.KeyboardButton('🔔Группа')
item5 = types.KeyboardButton('💵Рассчитать стоимость')
item6 = types.KeyboardButton('')
mp.add(item1, item2, item3, item4, item5, item6)

mp2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
item7 = types.KeyboardButton('👟Обувь')
item8 = types.KeyboardButton('👕Верхняя/нижняя одежда')
mp2.add(item7, item8)

mp3 = types.InlineKeyboardMarkup()
item9 = types.InlineKeyboardButton('вернуться к меню', callback_data='menu')
mp3.row(item9)


def send_photo_safe(chat_id, filename):
    """Безопасная отправка фото с проверкой"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            print(f"Текущая директория: {current_dir}")
            print(f"Содержимое директории: {os.listdir(current_dir)}")
            return False
        
        with open(file_path, 'rb') as photo:
            bot.send_photo(chat_id, photo)
        return True
        
    except Exception as e:
        print(f"Ошибка при отправке фото {filename}: {e}")
        return False


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!' '\n' '\n'
                                'Тут ты можешь рассчитать сумму своего заказа💵''\n'
                                'Связаться с менеджером' '\n'
                                '@DostavkaDewu' '\n'
                                'Получить ответы на все свои вопросы🤔'
                     .format(message.from_user), reply_markup=mp)
    bot.register_next_step_handler(message, button_menu)


@bot.message_handler(content_types=['text'])
def button_menu(message):
    if message.text.strip() == '💵Рассчитать стоимость':
        bot.send_message(message.chat.id, 'Выберите категорию товара' '\n'
        'От правильного выбора категории зависит стоимость доставки', reply_markup=mp2)
        bot.register_next_step_handler(message, cost_function)
    elif message.text.strip() == '🚚Как заказать?':
        bot.send_message(message.chat.id, '1.Выберите желаемую вами позицию' '\n' '\n'
'2.Откройте меню с размерами, а также стоимостью в юанях''\n' '\n'
'3.Нажмите линейку, дабы определить ваш конечный размер' '\n' '\n'
'4.После успешного выбора размера вам остаётся лишь узнать его цену в юанях, для этого просто нажмите на него' '\n' '\n'
'P.S. Не забудьте скопировать ссылку или артикул желаемого товара' '\n' '\n' '\n'
'КАК СКОПИРОВАТЬ ССЫЛКУ?' '\n'
'После перехода на страницу позиции вам необходимо нажать на кнопку сверху справа (зачастую она зелёная), во всплывающем окне выбрать пункт "скопировать"')
        
        if not send_photo_safe(message.chat.id, '3.jpg'):
            bot.send_message(message.chat.id, "Фото 3.jpg не найдено")
            
        if not send_photo_safe(message.chat.id, '4.jpg'):
            bot.send_message(message.chat.id, "Фото 4.jpg не найдено")
            
        bot.register_next_step_handler(message, button_menu)
    elif message.text.strip() == '📲Связь с менеджером':
        bot.send_message(message.chat.id, f'📲Связь с менеджером: @DostavkaDewu')
        bot.register_next_step_handler(message, button_menu)
    elif message.text.strip() == '💰Выкупы':
        bot.send_message(message.chat.id, f'💰Выкупы:    https://t.me/STORESTREETBASE')
        bot.register_next_step_handler(message, button_menu)
    elif message.text.strip() == '🎯Отзывы':
        bot.send_message(message.chat.id, f'🎯Отзывы:     https://t.me/STREETBASEOTZIV')
        bot.register_next_step_handler(message, button_menu)
    elif message.text.strip() == '🔔Группа':
        bot.send_message(message.chat.id, f'🔔Группа: https://t.me/STORESTREETBASE')
        bot.register_next_step_handler(message, button_menu)
    else:
        bot.send_message(message.chat.id, 'Упс! Что то пошло не так', reply_markup=mp)
        bot.register_next_step_handler(message, button_menu)


@bot.message_handler(content_types=['text'])
def cost_function(message):
    global cny, dop_price
    cny = 14.3

    if message.text.strip() == '👟Обувь':
        dop_price = 1000
    elif message.text.strip() == '👕Верхняя/нижняя одежда':
        dop_price = 800
    else:
        bot.send_message(message.chat.id, 'Неверный тип товара', reply_markup=mp2)
        bot.register_next_step_handler(message, cost_function)
        return
    
    if not send_photo_safe(message.chat.id, '1.jpg'):
        bot.send_message(message.chat.id, "Фото 1.jpg не найдено")
        
    if not send_photo_safe(message.chat.id, '2.jpg'):
        bot.send_message(message.chat.id, "Фото 2.jpg не найдено")
    
    bot.register_next_step_handler(message, get_cost)
    bot.send_message(message.chat.id, 'Введите цену товара в юанях ¥' '\n'
    '*Пожалуйста ознакомьтесь с инструкцией выше' '\n' '\n'
                     f'Курс юаня {cny}')


@bot.message_handler(content_types=['text'])
def get_cost(message):
    amount = message.text.strip()
    try:
        amount = float(amount)
        if amount <= 0:
            bot.send_message(message.chat.id, 'Неправильно указана стоимость товара' '\n'
                             'Введите ЧИСЛО больше НУЛЯ')
            bot.register_next_step_handler(message, get_cost)
            return
    except ValueError:
        bot.send_message(message.chat.id, 'Неправильно указана стоимость товара' '\n'
                         'Введите ЧИСЛО больше НУЛЯ')
        bot.register_next_step_handler(message, get_cost)
        return
    final_price = amount * cny + dop_price + 1500
    bot.send_message(message.chat.id, f'Итоговая цена: {final_price}₽ ' '\n' '\n' 
    '✈️Доставка до России включена в стоимость.' '\n'
    '🚛 СДЭК до вашего города вы оплачиваете отдельно,' '\n'   
    '(при получении)' '\n'  '\n'    
    'Оформить заказ: @DostavkaDewu', reply_markup=mp3)


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback(callback):
    bot.send_message(callback.message.chat.id, 'Спасибо за использовнаие нашего сервиса!'.format(callback.from_user),
                     reply_markup=mp)
    bot.register_next_step_handler(callback.message, button_menu)


if __name__ == "__main__":
    print("Бот запущен...")
    print(f"Текущая директория: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"Файлы в директории: {os.listdir('.')}")
    bot.polling(none_stop=True)