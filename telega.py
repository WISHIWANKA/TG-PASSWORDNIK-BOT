import telebot
from Vigener import Vigener
from telebot import types
import MyConfig as config
from Transposition import TransPose
import dbWorker
from passwordGenerator import PasswordGenerator
import string

bot = telebot.TeleBot(config.token)
vig = Vigener()
transpose = TransPose()
password = PasswordGenerator()
password_arr = []


@bot.message_handler(commands=['start'])
def handle_start(message):
    text = "Hello, my name is Passwordnik.\n" \
           "I can encode/decode Vigenere cipher with a given key.\n" \
           "Also, i can reverse your text.\n" \
           "But my main feature is password generation. Try it!!!"
    bot.send_message(message.chat.id, text, reply_markup=start_keyboard())
    print(message.from_user.first_name)


@bot.message_handler(commands=['encode', 'Encode'])
def handle_encoding(message):
    bot.send_message(message.chat.id, "Choose the algorithm", reply_markup=encoding_keyboard())
    dbWorker.set_state(message.chat.id, config.States.S_ENCODE.value)


@bot.message_handler(commands=['decode', 'Decode'])
def handle_decoding(message):
    bot.send_message(message.chat.id, "Choose the algorithm", reply_markup=encoding_keyboard())
    dbWorker.set_state(message.chat.id, config.States.S_DECODE.value)


@bot.message_handler(commands=['CreatePassword', 'createpassword', 'Createpassword'])
def handle_password(message):
    text = "The base of my Password Generation algorithm is ascii_letters.\n" \
           "If you want to use your own symbols, choose \"Custom\" button.\n" \
           "Also, you can add numbers to your password, choose \"Numbers\" button"
    bot.send_message(message.chat.id, text, reply_markup=password_keyboard())
    dbWorker.set_state(message.chat.id, config.States.S_PASSWORD.value)


@bot.message_handler(func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_PASSWORD.value)
def choosingPassword(message):
    if message.text.lower() == 'custom':
        bot.send_message(message.chat.id, "Great, enter your symbols!")
        dbWorker.set_state(message.chat.id, config.States.S_CUSTOM.value)
    elif message.text.lower() == 'numbers':
        password_arr.append(string.digits)
        password_arr.append(string.ascii_letters)
        bot.send_message(message.chat.id, "AAAlright, do you want to add special symbols like \"!@#$&^%$(^%$ \"?",
                         reply_markup=yes_no_keyboard())
        dbWorker.set_state(message.chat.id, config.States.S_NUMBERS.value)
    else:
        bot.send_message(message.chat.id, "I dont understand", reply_markup=password_keyboard())
        return


@bot.message_handler(func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_NUMBERS.value)
def handle_numbers(message):
    if message.text.lower() == 'yes':
        dbWorker.set_state(message.chat.id, config.States.S_YES.value)
        bot.send_message(message.chat.id, "I am waiting for your special symbols")
    elif message.text.lower() == 'no':
        bot.send_message(message.chat.id, 'I have generated five different passwords for you')
        for i in range(5):
            bot.send_message(message.chat.id, password.generate_password(8, password_arr))
        dbWorker.set_state(message.chat.id, config.States.S_START.value)
        bot.send_message(message.chat.id, "I am ready to do another task!", reply_markup=start_keyboard())
    else:
        bot.send_message(message.chat.id, 'I dont understand', reply_markup=yes_no_keyboard())
        return


@bot.message_handler(func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_YES.value)
def yes_handle(message):
    password_arr.append(message.text)
    bot.send_message(message.chat.id, "Here are your five passwords")
    for i in range(5):
        bot.send_message(message.chat.id, password.generate_password(8, password_arr))
    dbWorker.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, "I am ready to do another task!", reply_markup=start_keyboard())


@bot.message_handler(func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_CUSTOM.value)
def custom_password(message):
    if len(message.text) < 8:
        bot.send_message(message.chat.id, "You have entered less than eight symbols")
        return
    else:
        bot.send_message(message.chat.id, 'Got it!')
        password_arr.append(message.text)
        bot.send_message(message.chat.id, 'Here are your five passwords!')
        for i in range(5):
            bot.send_message(message.chat.id, password.generate_password(8, password_arr))
        dbWorker.set_state(message.chat.id, config.States.S_START.value)
        bot.send_message(message.chat.id, "I am ready to do another task!", reply_markup=start_keyboard())


@bot.message_handler(func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_DECODE.value)
def user_decoding(message):
    if message.text.lower() == "vigenere":
        bot.send_message(message.chat.id, "Enter your keyword, please")
        dbWorker.set_state(message.chat.id, config.States.S_KEYWORD_DECODE.value)
    elif message.text.lower() == "reverse":
        bot.send_message(message.chat.id, "Give me a text to reverse")
        dbWorker.set_state(message.chat.id, config.States.S_REVERSE.value)


@bot.message_handler(func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_ENCODE.value)
def user_encoding(message):
    if message.text.lower() == "vigenere":
        bot.send_message(message.chat.id, "Enter your keyword, please")
        dbWorker.set_state(message.chat.id, config.States.S_KEYWORD.value)
    elif message.text.lower() == "reverse":
        bot.send_message(message.chat.id, "Give me a text to reverse")
        dbWorker.set_state(message.chat.id, config.States.S_REVERSE.value)


@bot.message_handler(func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_REVERSE.value)
def reverse(message):
    bot.send_message(message.chat.id, transpose.reverse(message.text))
    dbWorker.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, "I am ready to do another task!", reply_markup=start_keyboard())


@bot.message_handler(func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_KEYWORD.value)
def user_entering_keyword(message):
    dbWorker.set_keyword(message.chat.id, message.text.lower())
    bot.send_message(message.chat.id,
                     "Alright, your keyword is " + message.text + ". Now give me a text to encode")
    dbWorker.set_state(message.chat.id, config.States.S_VIGENERE.value)


@bot.message_handler(
    func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_KEYWORD_DECODE.value)
def user_entering_keyword_decode(message):
    dbWorker.set_keyword(message.chat.id, message.text.lower())
    bot.send_message(message.chat.id,
                     "Alright, your keyword is " + message.text + ". Now give me a text to decode")
    dbWorker.set_state(message.chat.id, config.States.S_VIGENERE_DECODE.value)


@bot.message_handler(func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_VIGENERE.value)
def user_entering_text_vigenere(message):
    key = dbWorker.get_keyword(message.chat.id)
    encoded = vig.encode(key, message.text)
    bot.send_message(message.chat.id, "Here is your encoded text ")
    bot.send_message(message.chat.id, encoded)
    dbWorker.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, "I am ready to do another task!", reply_markup=start_keyboard())


@bot.message_handler(
    func=lambda message: dbWorker.get_current_state(message.chat.id) == config.States.S_VIGENERE_DECODE.value)
def user_entering_text_vigenere_decode(message):
    key = dbWorker.get_keyword(message.chat.id)
    decoded = vig.decode(key, message.text)
    bot.send_message(message.chat.id, "Here is your decoded text \n")
    bot.send_message(message.chat.id, decoded)
    dbWorker.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, "I am ready to do another task!", reply_markup=start_keyboard())


def start_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_encode = types.KeyboardButton('/Encode')
    button_decode = types.KeyboardButton('/Decode')
    button_generate_password = types.KeyboardButton('/CreatePassword')
    markup.add(button_decode, button_encode, button_generate_password)
    return markup


def encoding_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_vigenere = types.KeyboardButton("Vigenere")
    button_reversing = types.KeyboardButton('Reverse')
    markup.add(button_vigenere, button_reversing)
    return markup


def password_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_custom = types.KeyboardButton("Custom")
    button_numbers = types.KeyboardButton("Numbers")
    markup.add(button_custom, button_numbers)
    return markup


def yes_no_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_yes = types.KeyboardButton("Yes")
    button_no = types.KeyboardButton("No")
    markup.add(button_no, button_yes)
    return markup


bot.polling(none_stop=True)
