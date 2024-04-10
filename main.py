# coding: utf8
import telebot
from telebot import types
import poker_star
from totally_unnecessary import bot_TOKEN

bot = telebot.TeleBot(bot_TOKEN)
deck = poker_star.Deck()

def help():
    return '''
    Тут когда-нибудь будет справка


    '''

def actions_markup():
    markup = types.ReplyKeyboardMarkup()
    probability_button = types.KeyboardButton('/Вероятность')
    markup.row(probability_button)
    add_button = types.KeyboardButton('/Справка')
    clear_button = types.KeyboardButton('/Очистить')
    markup.row(add_button, clear_button)
    return markup


def combinations_markup():
    markup = types.ReplyKeyboardMarkup()
    pair_button = types.KeyboardButton('Пара')
    two_pairs_button = types.KeyboardButton('Две пары')
    three_of_a_kind_button = types.KeyboardButton('Тройня')
    markup.row(pair_button, two_pairs_button, three_of_a_kind_button)
    straight_button = types.KeyboardButton('Стрит')
    flash_button = types.KeyboardButton('Флеш')
    full_house_button = types.KeyboardButton('Фул Хауз')
    markup.row(straight_button, flash_button, full_house_button)
    four_of_a_kind_button = types.KeyboardButton('Каре')
    straight_flush_button = types.KeyboardButton('Стрит Флеш')
    royal_flush_button = types.KeyboardButton('Роял Флеш')
    markup.row(four_of_a_kind_button, straight_flush_button, royal_flush_button)
    return markup


@bot.message_handler(commands=['start'])
def start_seq(message):
    bot.send_message(message.chat.id, 'Приступим, напишите известные вам карты', reply_markup=actions_markup())


@bot.message_handler(commands=['Вероятность'])
def probability(message):
    bot.send_message(message.chat.id, 'Выберите комбинацию', reply_markup=combinations_markup())
    bot.register_next_step_handler(message, on_click_probability)


def on_click_probability(message):
    if message.text == 'Пара':
        bot.send_message(message.chat.id, deck.pair(), reply_markup=actions_markup())
    elif message.text == 'Две пары':
        bot.send_message(message.chat.id, deck.two_pair(), reply_markup=actions_markup())
    elif message.text == 'Тройня':
        bot.send_message(message.chat.id, deck.three_of_a_kind(), reply_markup=actions_markup())
    elif message.text == 'Стрит':
        bot.send_message(message.chat.id, deck.straight(), reply_markup=actions_markup())
    elif message.text == 'Флеш':
        bot.send_message(message.chat.id, deck.flush(), reply_markup=actions_markup())
    elif message.text == 'Фул Хауз':
        bot.send_message(message.chat.id, deck.full_house(), reply_markup=actions_markup())
    elif message.text == 'Каре':
        bot.send_message(message.chat.id, deck.four_of_a_kind(), reply_markup=actions_markup())
    elif message.text == 'Стрит Флеш':
        bot.send_message(message.chat.id, deck.straight_flush(), reply_markup=actions_markup())
    elif message.text == 'Роял Флеш':
        bot.send_message(message.chat.id, deck.royal_flush(), reply_markup=actions_markup())


@bot.message_handler(commands=['Справка'])
def probability(message):
    bot.send_message(message.chat.id, help(), reply_markup=actions_markup())


@bot.message_handler(commands=['Очистить'])
def clear(message):
    deck.known_cards = []
    deck.recreate_deck()
    bot.send_message(message.chat.id, 'Очистка выполнена', reply_markup=actions_markup())


@bot.message_handler()
def main(message):
    translate_result = deck.translate_user_input(message.text)
    if translate_result == 'error 101':
        bot.send_message(message.chat.id, deck.error_message(translate_result), reply_markup=actions_markup())
    elif translate_result == 'error 102':
        bot.send_message(message.chat.id, deck.error_message(translate_result), reply_markup=actions_markup())
    else:
        deck.remove_known_cards()
        deck.build_all_possible_combinations()
        bot.send_message(message.chat.id, f'Карты добавлены!\nВот известные вам карты:\n{deck.known_cards}',
                         reply_markup=actions_markup())


bot.infinity_polling()