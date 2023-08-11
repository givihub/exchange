import telebot
import requests
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

keys = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR',
    'биткоин': 'BTC',
    'фунт стерлингов': 'GBP',
    'лира': 'BTC',
    'египетский фунт': 'EGP',
    'бат': 'THB'

}

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    instructions = "Привет! Этот бот позволяет узнать цену на определенное количество валюты.\n\n" \
                   "Для получения цены используйте команду в формате:\n" \
                   "<имя валюты для конвертации> <имя валюты, в которой хотите узнать цену> <количество валюты для конвертации>\n" \
                   "Например: `/convert доллар рубль 100`\n\n Чтоб узнать доступные валюты, введите /values"
    bot.reply_to(message, instructions, parse_mode='Markdown')

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text ='\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def handle_conversion(message):
    try:
        command_parts = message.text.split()[1:]
        if len(command_parts) != 3:
            raise ValueError("Неверный формат команды")

        quote, base, amount = command_parts
        if quote not in keys or base not in keys:
            raise ValueError("Неправильное имя валюты")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={keys[base]}&from={keys[quote]}&amount={amount}"

        headers = {
            "apikey": "vN1pPvmWhtSjTeCuJBuQmT6ghDtkPAzI"
        }

        response = requests.get(url, headers=headers)

        result = response.json()

        if "error" in result:
            error_info = result['error']['info']
            bot.send_message(message.chat.id, f"Ошибка: {error_info}")
        else:
            converted_amount = result['result']
            text = f'Цена {amount} {quote} в {base} - {converted_amount:.2f} {base}'
            bot.send_message(message.chat.id, text)
    except ValueError as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

bot.polling()
