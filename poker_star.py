# import math
from collections import Counter
import itertools

class Deck:
    def __init__(self):
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т']
        self.suits = ['Черва', 'Буба', 'Крести', 'Пика']
        self.deck = [(value, suit) for suit in self.suits for value in self.values]
        self.known_cards = []
        self.all_possible_combinations = None
        self.card_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'В': 11, 'Д': 12,
                           'К': 13, 'Т': 14}

    def translate_user_input(self, string):
        if len(self.known_cards) >= 6:
            return f'error 102'
        for card in string.upper().split():
            if card[-1] == 'Ч':
                self.known_cards.append((card[0:-1], 'Черва'))
            elif card[-1] == 'Б':
                self.known_cards.append((card[0:-1], 'Буба'))
            elif card[-1] == 'К':
                self.known_cards.append((card[0:-1], 'Крести'))
            elif card[-1] == 'П':
                self.known_cards.append((card[0:-1], 'Пика'))
            else:
                return f'error 101'

    def recreate_deck(self):
        new_deck = [(value, suit) for suit in self.suits for value in self.values]
        self.deck = new_deck
        return

    def remove_known_cards(self):
        self.deck = [card for card in self.deck if card not in self.known_cards]
        return

    def build_all_possible_combinations(self):
        self.all_possible_combinations = list(itertools.combinations(self.deck, 7 - len(self.known_cards)))

    # Функция выводит словарь, где ключ это номинал или масть карты, а значение количество повторений.
    # Аргументы: kinds_or_suits, где 0 это номинал, а 1 это масть. possible_combinations это список оставшихся возможных карт
    # По дефолту функция работает с self.known_cards.
    def count_kinds_or_suits(self, kinds_or_suits, possible_combinations=None):
        if possible_combinations:
            all_cards = [card[kinds_or_suits] for card in self.known_cards]
            for card in possible_combinations:
                all_cards.append(card[kinds_or_suits])
            result = Counter(all_cards)
            return result
        return Counter([card[kinds_or_suits] for card in self.known_cards])

    def is_straight(self, cards):
        # Преобразование карт в их числовые значения
        values = [self.card_order[card[0]] for card in cards]
        # Удаление дубликатов и сортировка
        unique_values = sorted(set(values))
        # Проверка на наличие стрита

        def check_straight(values):
            cycle = 0
            for i in range(len(values) - 4):
                cycle += 1
                if values[i + 4] - values[i] == 4:
                    return True
            return False

        if check_straight(unique_values):
            return True
        # Учет возможности использования Туза как низшей карты
        if 14 in unique_values:
            low_ace_values = [1 if value == 14 else value for value in unique_values]
            low_ace_values = sorted(set(low_ace_values))
            return check_straight(low_ace_values)
        return False

    def is_royal_flush(self, cards):
        def check_flush_and_straight(cards):
            values = [self.card_order[card[0]] for card in cards]
            suits = [card[1] for card in cards]
            if len(set(suits)) != 1:  # Все карты должны быть одной масти для флеша
                return False
            sorted_values = sorted(values)
            if sorted_values[4] - sorted_values[0] == 4:  # Проверка на стрит
                return True
            if sorted_values == [2, 3, 4, 5, 14]:  # Проверка на низкий стрит с Тузом
                return True
            return False
        for five_cards in itertools.combinations(cards, 5):
            if check_flush_and_straight(five_cards):
                if set(self.card_order[card[0]] for card in five_cards) == {10, 11, 12, 13, 14}:
                    return "Роял флеш"
                return "Стрит флеш"
        return False

    def pair(self):
        # Проверка есть ли уже эта комбинация
        test = self.count_kinds_or_suits(0)
        for value in test:
            if test[value] == 2:
                return f'У вас уже есть пара!'
            elif test[value] >= 3:
                return f'У вас уже есть комбинация лучше!'
        # Подсчет вероятности пары
        successes = 0
        for river in self.all_possible_combinations:
            keys = self.count_kinds_or_suits(0, river)
            pair = 0
            failure = False
            for value in keys:
                if keys[value] >= 3:
                    failure = True
                    break
                elif keys[value] == 2:
                    pair += 1
            if failure:
                continue
            elif pair == 1:
                successes += 1
        return f'{round(successes / len(self.all_possible_combinations) * 100, 2)}%'

    def two_pair(self):
        successes = 0
        #Тест на наличие комбинаций похожих
        test = self.count_kinds_or_suits(0)
        pair = 0
        for value in test:
            if test[value] >= 3:
                return f'У вас уже есть комбинация лучше!'
            elif test[value] == 2:
                pair += 1
        if pair >= 2:
            return f'У вас уже есть эта комбинация!'
        #Подсчет вероятностей
        for river in self.all_possible_combinations:
            keys = self.count_kinds_or_suits(0, river)
            pair = 0
            failure = False
            for value in keys:
                if keys[value] >= 3:
                    failure = True
                    break
                elif keys[value] == 2:
                    pair += 1
            if failure:
                continue
            elif pair >= 2:
                successes += 1
        return f'{round(successes / len(self.all_possible_combinations) * 100, 2)}%'

    def three_of_a_kind(self):
        successes = 0
        # Тест на наличие комбинаций похожих
        test = self.count_kinds_or_suits(0)
        three_of_a_kind = 0
        for value in test:
            if test[value] >= 4:
                return f'У вас уже есть комбинация лучше!'
            elif test[value] == 3:
                three_of_a_kind += 1
        if three_of_a_kind == 1:
            return f'У вас уже есть эта комбинация!'
        # Подсчет вероятностей
        for river in self.all_possible_combinations:
            keys = self.count_kinds_or_suits(0, river)
            three_of_a_kind = 0
            failure = False
            for value in keys:
                if keys[value] >= 4:
                    failure = True
                    break
                elif keys[value] == 3:
                    three_of_a_kind += 1
            if failure:
                continue
            elif three_of_a_kind == 1:
                successes += 1
        return f'{round(successes / len(self.all_possible_combinations) * 100, 2)}%'

    def straight(self):
        # Проверка на наличие этой комбинации
        if len(self.known_cards) >= 5:
            if self.is_straight(self.known_cards):
                return f'У вас уже есть стрит!'
        # Вычисление вероятности
        successes = 0
        for river in self.all_possible_combinations:
            all_cards = [card for card in self.known_cards]
            for card in river:
                all_cards.append(card)
            if self.is_straight(all_cards):
                successes += 1
        return f'{round(successes / len(self.all_possible_combinations) * 100, 2)}%'


    def flush(self):
        successes = 0
        # Тест на наличие комбинаций похожих
        test = self.count_kinds_or_suits(1)
        for value in test:
            if test[value] >= 5:
                return f'У вас уже есть эта комбинация!'
        # Подсчет вероятностей
        for river in self.all_possible_combinations:
            keys = self.count_kinds_or_suits(1, river)
            for value in keys:
                if keys[value] >= 5:
                    successes += 1
                    break
        return f'{round(successes / len(self.all_possible_combinations) * 100, 2)}%'
        pass

    def full_house(self):
        successes = 0
        # Тест на наличие комбинаций похожих
        test = self.count_kinds_or_suits(0)
        three_of_a_kind = 0
        pair = 0
        for value in test:
            if test[value] >= 4:
                return f'У вас уже есть комбинация лучше!'
            elif test[value] == 3:
                three_of_a_kind += 1
            elif test[value] == 2:
                pair += 1
        if three_of_a_kind == 1 and pair >= 1:
            return f'У вас уже есть эта комбинация!'
        # Подсчет вероятностей
        for river in self.all_possible_combinations:
            keys = self.count_kinds_or_suits(0, river)
            three_of_a_kind = 0
            pair = 0
            failure = False
            for value in keys:
                if keys[value] >= 4:
                    failure = True
                    break
                elif keys[value] == 3:
                    three_of_a_kind += 1
                elif keys[value] == 2:
                    pair += 1
            if failure:
                continue
            elif three_of_a_kind == 1 and pair >= 1:
                successes += 1
        return f'{round(successes / len(self.all_possible_combinations) * 100, 2)}%'
        pass

    def four_of_a_kind(self):
        successes = 0
        # Тест на наличие комбинаций похожих
        test = self.count_kinds_or_suits(0)
        four_of_a_kind = 0
        for value in test:
            if test[value] == 4:
                four_of_a_kind += 1
        if four_of_a_kind == 1:
            return f'У вас уже есть эта комбинация!'
        # Подсчет вероятностей
        for river in self.all_possible_combinations:
            keys = self.count_kinds_or_suits(0, river)
            four_of_a_kind = 0
            for value in keys:
                if keys[value] == 4:
                    four_of_a_kind += 1
            if four_of_a_kind == 1:
                successes += 1
        return f'{round(successes / len(self.all_possible_combinations) * 100, 2)}%'


    def straight_flush(self):
        # Проверка на наличие этой комбинации
        if len(self.known_cards) >= 5:
            if self.is_royal_flush(self.known_cards) == "Стрит флеш":
                return f'У вас уже есть стрит флеш!!!'
            elif self.is_royal_flush(self.known_cards) == "Роял флеш":
                return f'Ты ебанутый?! Это же РОЯЯЯЯЯЛ!!!'
        # Вычисление вероятности
        successes = 0
        for river in self.all_possible_combinations:
            all_cards = [card for card in self.known_cards]
            for card in river:
                all_cards.append(card)
            if self.is_royal_flush(all_cards) == "Стрит флеш":
                successes += 1
        return f'{round(successes / len(self.all_possible_combinations) * 100, 2)}%'
        pass

    def royal_flush(self):
        # Проверка на наличие этой комбинации
        if len(self.known_cards) >= 5:
            if self.is_royal_flush(self.known_cards) == "Роял флеш":
                return f'Ты ебанутый?! Это же РОЯЯЯЯЯЛ!!!'
        # Вычисление вероятности
        successes = 0
        for river in self.all_possible_combinations:
            all_cards = [card for card in self.known_cards]
            for card in river:
                all_cards.append(card)
            if self.is_royal_flush(all_cards) == "Роял флеш":
                successes += 1
        return f'{round(successes / len(self.all_possible_combinations) * 100, 2)}%'


    def error_message(self, error):
        if error == 'error 101':
            return f'Ошибка в вводе, перезапустите программу!'
        elif error == 'error 102':
            return f'Вам уже известны все карты! Выполните очистку или перезапустите программу!'



#
running = True
while running:
    print(f'Здарова, отец.')
    user_input = input(f'Какие карты известны?\n:')
    deck = Deck()
    deck.translate_user_input(user_input)
    deck.remove_known_cards()
    deck.build_all_possible_combinations()

    print(f'{len(deck.all_possible_combinations)}\nall possible combination built!')
    while running:
        user_input = input(f'Че делаем?\n:')
        if user_input == 'стоп':
            running = False
            break
        elif user_input == 'помощь':
            print(f'These are all the possible commands:\n')
        elif user_input == 'добавить':
            user_input = input('\n:')
            deck.translate_user_input(user_input)
            print(deck.known_cards)
        elif user_input == 'заново':
            deck.recreate_deck()
            deck.known_cards = []
        elif user_input == 'пара':
            print(deck.pair())
        elif user_input == 'две пары':
            print(deck.two_pair())
        elif user_input == 'тройня':
            print(deck.three_of_a_kind())
        elif user_input == 'фул хауз':
            print(deck.full_house())
        elif user_input == 'каре':
            print(deck.four_of_a_kind())
        elif user_input == 'флеш':
            print(deck.flush())
        elif user_input == 'стрит':
            print(deck.straight())
        elif user_input == 'стрит флеш':
            print(deck.straight_flush())
        elif user_input == 'роял':
            print(deck.royal_flush())
        elif user_input == 'общее':
            print(len(list(deck.all_possible_combinations)))
# #

