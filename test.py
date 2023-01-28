from Card import Card
from Player import Player
from constants import *
import random
import os

os.system('clear')


def display_cards(table, cards):
    print("Table:")
    for card in table:
        print(card.name, card.suit)

    print("\nMy cards:")
    for card in cards:
        print(card.name, card.suit)

def check_fh():
    results = []
    my_cards = [
        Card('K', 'D'),
        Card('K', 'D'),
    ]

    table = [
        Card('A', 'H'),
        Card('K', 'C'),
        Card('A', 'C'),
        Card('A', 'S'),
        Card('10', 'H'),
    ]

    for _ in range(100):
        random.shuffle(table)
        random.shuffle(my_cards)
        player = Player(100)


        for card in my_cards:
            player.add_card(card)
        
        _, points = player.get_combination_and_hand_value(table)

        if points == 7:
            results.append(True)
        else:
            results.append(False)
            break

    print("Full House: ", all(results))


def check_straight():
    results = []
    player = Player(100)
    my_cards = [
        Card('K', 'D'),
        Card('J', 'D'),
    ]

    table = [
        Card('A', 'H'),
        Card('10', 'C'),
        Card('A', 'C'),
        Card('Q', 'S'),
        Card('10', 'H'),
    ]

    for _ in range(100):
        random.shuffle(table)
        random.shuffle(my_cards)
        player = Player(100)


        for card in my_cards:
            player.add_card(card)
        
        _, points = player.get_combination_and_hand_value(table)

        if points == 5:
            results.append(True)
        else:
            results.append(False)
            break

    print("Straight: ", all(results))


def check_flush_straight():
    results = []
    my_cards = [
        Card('K', 'D'),
        Card('J', 'D'),
    ]

    table = [
        Card('A', 'D'),
        Card('10', 'D'),
        Card('A', 'C'),
        Card('Q', 'D'),
        Card('10', 'H'),
    ]

    for _ in range(100):
        random.shuffle(table)
        random.shuffle(my_cards)
        player = Player(100)

        for card in my_cards:
            player.add_card(card)
        
        _, points = player.get_combination_and_hand_value(table)

        if points == 9:
            results.append(True)
        else:
            results.append(False)
            break

    print("Flush Straight: ", all(results))


def check_flush():
    results = []
    my_cards = [
        Card('2', 'D'),
        Card('3', 'D'),
    ]

    table = [
        Card('A', 'D'),
        Card('10', 'D'),
        Card('A', 'C'),
        Card('Q', 'D'),
        Card('10', 'H'),
    ]

    for _ in range(100):
        random.shuffle(table)
        random.shuffle(my_cards)
        player = Player(100)

        for card in my_cards:
            player.add_card(card)
        
        _, points = player.get_combination_and_hand_value(table)

        if points == 6:
            results.append(True)
        else:
            results.append(False)
            break

    print("Flush: ", all(results))


def check_4of_a_kind():
    results = []
    player = Player(100)
    my_cards = [
        Card('2', 'D'),
        Card('2', 'D'),
    ]

    table = [
        Card('2', 'D'),
        Card('2', 'D'),
        Card('A', 'C'),
        Card('A', 'D'),
        Card('10', 'H'),
    ]

    for _ in range(100):
        random.shuffle(table)
        random.shuffle(my_cards)
        player = Player(100)

        for card in my_cards:
            player.add_card(card)
        
        _, points = player.get_combination_and_hand_value(table)

        if points == 8:
            results.append(True)
        else:
            results.append(False)
            break

    print("Flush: ", all(results))


def check_3of_a_kind():
    results = []
    player = Player(100)
    my_cards = [
        Card('2', 'C'),
        Card('2', 'H'),
    ]

    table = [
        Card('2', 'D'),
        Card('8', 'D'),
        Card('A', 'C'),
        Card('4', 'D'),
        Card('10', 'H'),
    ]

    for _ in range(100):
        random.shuffle(table)
        random.shuffle(my_cards)
        player = Player(100)

        for card in my_cards:
            player.add_card(card)
        
        _, points = player.get_combination_and_hand_value(table)

        if points == 4:
            results.append(True)
        else:
            results.append(False)
            break

    print("Three of a kind: ", all(results))


def check_2_pairs():
    results = []
    player = Player(100)
    my_cards = [
        Card('2', 'D'),
        Card('2', 'H'),
    ]

    table = [
        Card('5', 'D'),
        Card('8', 'D'),
        Card('A', 'C'),
        Card('5', 'D'),
        Card('10', 'H'),
    ]

    for _ in range(100):
        random.shuffle(table)
        random.shuffle(my_cards)
        player = Player(100)

        for card in my_cards:
            player.add_card(card)
        
        _, points = player.get_combination_and_hand_value(table)

        if points == 3:
            results.append(True)
        else:
            results.append(False)
            break

    print("Two pairs: ", all(results))


def check_pair():
    results = []
    player = Player(100)
    my_cards = [
        Card('2', 'D'),
        Card('A', 'H'),
    ]

    table = [
        Card('J', 'D'),
        Card('8', 'D'),
        Card('A', 'C'),
        Card('5', 'D'),
        Card('10', 'H'),
    ]

    for _ in range(100):
        random.shuffle(table)
        random.shuffle(my_cards)
        player = Player(100)

        for card in my_cards:
            player.add_card(card)
        
        _, points = player.get_combination_and_hand_value(table)

        if points == 2:
            results.append(True)
        else:
            results.append(False)
            break

    print("Two pairs: ", all(results))


def check_high_card():
    results = []
    player = Player(100)
    my_cards = [
        Card('2', 'D'),
        Card('A', 'H'),
    ]

    table = [
        Card('J', 'D'),
        Card('8', 'D'),
        Card('3', 'C'),
        Card('5', 'D'),
        Card('10', 'H'),
    ]

    for _ in range(100):
        random.shuffle(table)
        random.shuffle(my_cards)
        player = Player(100)

        for card in my_cards:
            player.add_card(card)
        
        _, points = player.get_combination_and_hand_value(table)

        if points == 1:
            results.append(True)
        else:
            results.append(False)
            break

    print("High card: ", all(results))


check_flush_straight()
check_4of_a_kind()
check_fh()
check_flush()
check_straight()
check_3of_a_kind()
check_2_pairs()
check_pair()
check_high_card()