# coding: utf8
import telebot
from telebot import types
import db
import poker_star
from totally_unnecessary import bot_TOKEN

bot = telebot.TeleBot(bot_TOKEN)
deck = poker_star.Deck()


def help():
    return '''
    Я тебе че, поликлиника, блять?
    '''


def actions_markup():
    markup = types.ReplyKeyboardMarkup()
    probability_button = types.KeyboardButton('/Вероятность')
    cards_button = types.KeyboardButton('/Карты')
    markup.row(probability_button, cards_button)
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
    back_button = types.KeyboardButton('Назад')
    markup.row(back_button)
    return markup


@bot.message_handler(commands=['start'])
def start_seq(message):
    db.db_init(str(message.from_user.id))
    bot.send_message(message.chat.id, 'Приступим, напишите известные вам карты', reply_markup=actions_markup())


@bot.message_handler(commands=['Вероятность'])
def probability(message):
    bot.send_message(message.chat.id, 'Выберите комбинацию', reply_markup=combinations_markup())
    bot.register_next_step_handler(message, on_click_probability)


@bot.message_handler(commands=['Карты'])
def probability(message):
    bot.send_message(message.chat.id, f'Ваши карты:\n{db.db_pull_cards(message.from_user.id)}',
                     reply_markup=actions_markup())


def adjust_deck_and_return_known_cards(message):
    deck.recreate_deck()
    known_cards = db.db_pull_cards(message.from_user.id)
    deck.remove_known_cards(known_cards)
    return known_cards


def on_click_probability(message):
    if message.text == 'Пара':
        known_cards = adjust_deck_and_return_known_cards(message)
        bot.send_message(message.chat.id, deck.pair(known_cards, deck.build_all_possible_combinations(known_cards)),
                         reply_markup=actions_markup())
    elif message.text == 'Две пары':
        known_cards = adjust_deck_and_return_known_cards(message)
        bot.send_message(message.chat.id, deck.two_pair(known_cards, deck.build_all_possible_combinations(known_cards)),
                         reply_markup=actions_markup())
    elif message.text == 'Тройня':
        known_cards = adjust_deck_and_return_known_cards(message)
        bot.send_message(message.chat.id, deck.three_of_a_kind(known_cards, deck.build_all_possible_combinations(known_cards)),
                         reply_markup=actions_markup())
    elif message.text == 'Стрит':
        known_cards = adjust_deck_and_return_known_cards(message)
        bot.send_message(message.chat.id, deck.straight(known_cards, deck.build_all_possible_combinations(known_cards)),
                         reply_markup=actions_markup())
    elif message.text == 'Флеш':
        known_cards = adjust_deck_and_return_known_cards(message)
        bot.send_message(message.chat.id, deck.flush(known_cards, deck.build_all_possible_combinations(known_cards)),
                         reply_markup=actions_markup())
    elif message.text == 'Фул Хауз':
        known_cards = adjust_deck_and_return_known_cards(message)
        bot.send_message(message.chat.id, deck.full_house(known_cards, deck.build_all_possible_combinations(known_cards)),
                         reply_markup=actions_markup())
    elif message.text == 'Каре':
        known_cards = adjust_deck_and_return_known_cards(message)
        bot.send_message(message.chat.id, deck.four_of_a_kind(known_cards, deck.build_all_possible_combinations(known_cards)),
                         reply_markup=actions_markup())
    elif message.text == 'Стрит Флеш':
        known_cards = adjust_deck_and_return_known_cards(message)
        bot.send_message(message.chat.id, deck.straight_flush(known_cards, deck.build_all_possible_combinations(known_cards)),
                         reply_markup=actions_markup())
    elif message.text == 'Роял Флеш':
        known_cards = adjust_deck_and_return_known_cards(message)
        bot.send_message(message.chat.id, deck.royal_flush(known_cards, deck.build_all_possible_combinations(known_cards)),
                         reply_markup=actions_markup())
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, '...', reply_markup=actions_markup())


@bot.message_handler(commands=['Справка'])
def probability(message):
    bot.send_message(message.chat.id, help(), reply_markup=actions_markup())


@bot.message_handler(commands=['Очистить'])
def clear(message):
    db.db_clear_cards(message.from_user.id)
    bot.send_message(message.chat.id, 'Очистка выполнена', reply_markup=actions_markup())


def check_for_errors(message):
    '''Всевозможные проверки на ошибки в вводе'''
    text_to_check = message.text.upper().split()
    for word in text_to_check:
        if len(word) > 3:
            return True
        elif word[-1] not in 'ЧБКП':
            return True
    return False


@bot.message_handler()
def main(message):
    if check_for_errors(message):
        bot.send_message(message.chat.id, f'Ошибка связанная с форматом ввода!\n'
                                          f'Для получения более подробной информации обратитесь к справке!',
                         reply_markup=actions_markup())
    else:
        db.db_update_cards(message.from_user.id, message.text)
        bot.send_message(message.chat.id, f'Карты добавлены!', reply_markup=actions_markup())


bot.infinity_polling()