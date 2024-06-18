import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, ConversionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'For start, please, enter your message as follow: \n<value_1> \
<value_2> <amount> \n To see all available values: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available values'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Too many signs. Try again, please')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f"User's error \n{e}")
    except Exception as e:
        bot.reply_to(message, f'Cannot elaborate this request\n{e}')
    else:
        text = f'Price {amount} {quote} in {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
