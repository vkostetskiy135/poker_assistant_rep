# import math
from collections import Counter
import itertools


class Deck:
    def __init__(self):
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т']
        self.suits = ['Черва', 'Буба', 'Крести', 'Пика']
        self.deck = [(value, suit) for suit in self.suits for value in self.values]
        self.card_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'В': 11, 'Д': 12,
                           'К': 13, 'Т': 14}

    def recreate_deck(self):
        new_deck = [(value, suit) for suit in self.suits for value in self.values]
        self.deck = new_deck
        return

    def remove_known_cards(self, known_cards):
        self.deck = [card for card in self.deck if card not in known_cards]
        return

    def build_all_possible_combinations(self, known_cards):
        return list(itertools.combinations(self.deck, 7 - len(known_cards)))

    # Функция выводит словарь, где ключ это номинал или масть карты, а значение количество повторений.
    # Аргументы: kinds_or_suits, где 0 это номинал, а 1 это масть. possible_combinations это список оставшихся возможных карт
    # По дефолту функция работает с self.known_cards.
    def count_kinds_or_suits(self, kinds_or_suits, known_cards, possible_combinations=None):
        if possible_combinations:
            all_cards = [card[kinds_or_suits] for card in known_cards]
            for card in possible_combinations:
                all_cards.append(card[kinds_or_suits])
            result = Counter(all_cards)
            return result
        return Counter([card[kinds_or_suits] for card in known_cards])

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
        def check_flush_and_straight():
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
            if check_flush_and_straight():
                if set(self.card_order[card[0]] for card in five_cards) == {10, 11, 12, 13, 14}:
                    return "Роял флеш"
                return "Стрит флеш"
        return False

    def pair(self, known_cards, all_possible_combinations):
        # Проверка есть ли уже эта комбинация
        test = self.count_kinds_or_suits(0, known_cards)
        for value in test:
            if test[value] == 2:
                return f'У вас уже есть пара!'
            elif test[value] >= 3:
                return f'У вас уже есть комбинация лучше!'
        # Подсчет вероятности пары
        successes = 0
        for river in all_possible_combinations:
            keys = self.count_kinds_or_suits(0, river, known_cards)
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
        return f'{round(successes / len(all_possible_combinations) * 100, 2)}%'

    def two_pair(self, known_cards, all_possible_combinations):
        successes = 0
        #Тест на наличие комбинаций похожих
        test = self.count_kinds_or_suits(0, known_cards)
        pair = 0
        for value in test:
            if test[value] >= 3:
                return f'У вас уже есть комбинация лучше!'
            elif test[value] == 2:
                pair += 1
        if pair >= 2:
            return f'У вас уже есть эта комбинация!'
        #Подсчет вероятностей
        for river in all_possible_combinations:
            keys = self.count_kinds_or_suits(0, river, known_cards)
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
        return f'{round(successes / len(all_possible_combinations) * 100, 2)}%'

    def three_of_a_kind(self, known_cards, all_possible_combinations):
        successes = 0
        # Тест на наличие комбинаций похожих
        test = self.count_kinds_or_suits(0, known_cards)
        three_of_a_kind = 0
        for value in test:
            if test[value] >= 4:
                return f'У вас уже есть комбинация лучше!'
            elif test[value] == 3:
                three_of_a_kind += 1
        if three_of_a_kind == 1:
            return f'У вас уже есть эта комбинация!'
        # Подсчет вероятностей
        for river in all_possible_combinations:
            keys = self.count_kinds_or_suits(0, river, known_cards)
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
        return f'{round(successes / len(all_possible_combinations) * 100, 2)}%'

    def straight(self, known_cards, all_possible_combinations):
        # Проверка на наличие этой комбинации
        if len(known_cards) >= 5:
            if self.is_straight(known_cards):
                return f'У вас уже есть стрит!'
        # Вычисление вероятности
        successes = 0
        for river in all_possible_combinations:
            all_cards = [card for card in known_cards]
            for card in river:
                all_cards.append(card)
            if self.is_straight(all_cards):
                successes += 1
        return f'{round(successes / len(all_possible_combinations) * 100, 2)}%'

    def flush(self, known_cards, all_possible_combinations):
        successes = 0
        # Тест на наличие комбинаций похожих
        test = self.count_kinds_or_suits(1, known_cards)
        for value in test:
            if test[value] >= 5:
                return f'У вас уже есть эта комбинация!'
        # Подсчет вероятностей
        for river in all_possible_combinations:
            keys = self.count_kinds_or_suits(1, river, known_cards)
            for value in keys:
                if keys[value] >= 5:
                    successes += 1
                    break
        return f'{round(successes / len(all_possible_combinations) * 100, 2)}%'
        pass

    def full_house(self, known_cards, all_possible_combinations):
        successes = 0
        # Тест на наличие комбинаций похожих
        test = self.count_kinds_or_suits(0, known_cards)
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
        for river in all_possible_combinations:
            keys = self.count_kinds_or_suits(0, river, known_cards)
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
        return f'{round(successes / len(all_possible_combinations) * 100, 2)}%'
        pass

    def four_of_a_kind(self, known_cards, all_possible_combinations):
        successes = 0
        # Тест на наличие комбинаций похожих
        test = self.count_kinds_or_suits(0, known_cards)
        four_of_a_kind = 0
        for value in test:
            if test[value] == 4:
                four_of_a_kind += 1
        if four_of_a_kind == 1:
            return f'У вас уже есть эта комбинация!'
        # Подсчет вероятностей
        for river in all_possible_combinations:
            keys = self.count_kinds_or_suits(0, river, known_cards)
            four_of_a_kind = 0
            for value in keys:
                if keys[value] == 4:
                    four_of_a_kind += 1
            if four_of_a_kind == 1:
                successes += 1
        return f'{round(successes / len(all_possible_combinations) * 100, 2)}%'

    def straight_flush(self, known_cards, all_possible_combinations):
        # Проверка на наличие этой комбинации
        if len(known_cards) >= 5:
            if self.is_royal_flush(known_cards) == "Стрит флеш":
                return f'У вас уже есть стрит флеш!!!'
            elif self.is_royal_flush(known_cards) == "Роял флеш":
                return f'Ты ебанутый?! Это же РОЯЯЯЯЯЛ!!!'
        # Вычисление вероятности
        successes = 0
        for river in all_possible_combinations:
            all_cards = [card for card in known_cards]
            for card in river:
                all_cards.append(card)
            if self.is_royal_flush(all_cards) == "Стрит флеш":
                successes += 1
        return f'{round(successes / len(all_possible_combinations) * 100, 2)}%'
        pass

    def royal_flush(self, known_cards, all_possible_combinations):
        # Проверка на наличие этой комбинации
        if len(known_cards) >= 5:
            if self.is_royal_flush(known_cards) == "Роял флеш":
                return f'Ты ебанутый?! Это же РОЯЯЯЯЯЛ!!!'
        # Вычисление вероятности
        successes = 0
        for river in all_possible_combinations:
            all_cards = [card for card in known_cards]
            for card in river:
                all_cards.append(card)
            if self.is_royal_flush(all_cards) == "Роял флеш":
                successes += 1
        return f'{round(successes / len(all_possible_combinations) * 100, 2)}%'
