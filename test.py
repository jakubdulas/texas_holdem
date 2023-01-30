from Card import Card
from Player import Player
from constants import *
import random
import os
from utils import choose_winner, calculate_combination_strength

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


def check_highest_card1():
    player = Player(100)
    hand = [
        Card('8', 'D'),
        Card('K', 'H'),
    ]

    combination = [
        Card('A', 'D'),
        Card('A', 'D'),
        Card('A', 'C'),
        Card('8', 'D'),
        Card('8', 'H'),
    ]

    for card in hand:
        player.add_card(card)
    
    print("High card 1: ", player.choose_high_card(combination) == 13)


def check_highest_card2():
    player = Player(100)
    hand = [
        Card('Q', 'D'),
        Card('K', 'H'),
    ]

    combination = [
        Card('A', 'D'),
        Card('A', 'D'),
        Card('A', 'C'),
        Card('8', 'D'),
        Card('8', 'H'),
    ]

    for card in hand:
        player.add_card(card)
    
    print("High card 2: ", player.choose_high_card(combination) == 13)


def check_highest_card3():
    player = Player(100)
    hand = [
        Card('8', 'D'),
        Card('8', 'H'),
    ]

    combination = [
        Card('A', 'D'),
        Card('A', 'D'),
        Card('A', 'C'),
        Card('8', 'D'),
        Card('8', 'H'),
    ]

    for card in hand:
        player.add_card(card)
    
    print("High card 3: ", player.choose_high_card(combination) == 0)

def check_choose_winner_fh1():
    p1 = Player(100)
    hand1 = [
        Card('K', 'D'),
        Card('2', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('2', 'D'),
        Card('2', 'C')
    ]

    table = [
        Card('A', 'C'),
        Card('A', 'H'),
        Card('A', 'D'),
        Card('2', 'C'),
        Card('8', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Full House 1: ", choose_winner([p1, p2], table_cards=table) == [p1])


def check_choose_winner_fh2():
    p1 = Player(100)
    hand1 = [
        Card('2', 'D'),
        Card('2', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('K', 'D'),
        Card('K', 'C')
    ]

    table = [
        Card('A', 'C'),
        Card('A', 'H'),
        Card('A', 'D'),
        Card('2', 'C'),
        Card('8', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Full House 2: ", choose_winner([p1, p2], table_cards=table) == [p2])


def check_choose_winner_fh3():
    p1 = Player(100)
    hand1 = [
        Card('2', 'D'),
        Card('2', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('K', 'D'),
        Card('K', 'C')
    ]

    table = [
        Card('A', 'C'),
        Card('A', 'H'),
        Card('A', 'D'),
        Card('2', 'C'),
        Card('8', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Full House 3: ", choose_winner([p1, p2], table_cards=table) == [p2])


def check_choose_winner_fh4():
    p1 = Player(100)
    hand1 = [
        Card('2', 'D'),
        Card('2', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('2', 'H'),
        Card('2', 'S')
    ]

    table = [
        Card('A', 'C'),
        Card('A', 'H'),
        Card('A', 'D'),
        Card('3', 'C'),
        Card('8', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Full House 4: ", choose_winner([p1, p2], table_cards=table) == [p1, p2])


def check_choose_winner_straight1():
    p1 = Player(100)
    hand1 = [
        Card('2', 'D'),
        Card('3', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('2', 'H'),
        Card('7', 'S')
    ]

    table = [
        Card('3', 'C'),
        Card('4', 'H'),
        Card('5', 'D'),
        Card('6', 'C'),
        Card('A', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Straight 1: ", choose_winner([p1, p2], table_cards=table) == [p2])


def check_choose_winner_straight2():
    p1 = Player(100)
    hand1 = [
        Card('2', 'D'),
        Card('3', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('2', 'H'),
        Card('3', 'S')
    ]

    table = [
        Card('3', 'C'),
        Card('4', 'H'),
        Card('5', 'D'),
        Card('6', 'C'),
        Card('A', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Straight 2: ", choose_winner([p1, p2], table_cards=table) == [p1, p2])


def check_choose_winner_straight3():
    p1 = Player(100)
    hand1 = [
        Card('K', 'D'),
        Card('3', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('3', 'H'),
        Card('Q', 'S')
    ]

    table = [
        Card('7', 'C'),
        Card('4', 'H'),
        Card('5', 'D'),
        Card('6', 'C'),
        Card('A', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Straight 3: ", choose_winner([p1, p2], table_cards=table) == [p1])


def check_choose_winner_pair1():
    p1 = Player(100)
    hand1 = [
        Card('K', 'D'),
        Card('K', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('3', 'H'),
        Card('3', 'S')
    ]

    table = [
        Card('7', 'C'),
        Card('Q', 'H'),
        Card('5', 'D'),
        Card('6', 'C'),
        Card('A', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Pair 1: ", choose_winner([p1, p2], table_cards=table) == [p1])


def check_choose_winner_pair2():
    p1 = Player(100)
    hand1 = [
        Card('3', 'D'),
        Card('2', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('4', 'H'),
        Card('2', 'S')
    ]

    table = [
        Card('7', 'C'),
        Card('A', 'H'),
        Card('5', 'D'),
        Card('6', 'C'),
        Card('A', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Pair 2: ", choose_winner([p1, p2], table_cards=table) == [p2])


def check_choose_winner_pair3():
    p1 = Player(100)
    hand1 = [
        Card('3', 'D'),
        Card('9', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('9', 'H'),
        Card('3', 'S')
    ]

    table = [
        Card('2', 'C'),
        Card('6', 'H'),
        Card('9', 'D'),
        Card('10', 'C'),
        Card('K', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Pair 3: ", choose_winner([p1, p2], table_cards=table) == [p1, p2])


def check_choose_winner_two_pairs1():
    p1 = Player(100)
    hand1 = [
        Card('3', 'D'),
        Card('9', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('9', 'H'),
        Card('3', 'S')
    ]

    table = [
        Card('3', 'C'),
        Card('6', 'H'),
        Card('9', 'D'),
        Card('10', 'C'),
        Card('K', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Two Pairs 1: ", choose_winner([p1, p2], table_cards=table) == [p1, p2])


def check_choose_winner_two_pairs2():
    p1 = Player(100)
    hand1 = [
        Card('9', 'D'),
        Card('9', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('9', 'H'),
        Card('3', 'S')
    ]

    table = [
        Card('3', 'C'),
        Card('6', 'H'),
        Card('10', 'D'),
        Card('10', 'C'),
        Card('K', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Two Pairs 2: ", choose_winner([p1, p2], table_cards=table) == [p1])


def check_choose_winner_two_pairs3():
    p1 = Player(100)
    hand1 = [
        Card('2', 'D'),
        Card('A', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('2', 'H'),
        Card('A', 'S')
    ]

    table = [
        Card('3', 'C'),
        Card('6', 'H'),
        Card('10', 'D'),
        Card('10', 'C'),
        Card('K', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Two Pairs 3: ", choose_winner([p1, p2], table_cards=table) == [p1, p2])


def check_choose_winner_three_of_a_kind1():
    p1 = Player(100)
    hand1 = [
        Card('2', 'D'),
        Card('2', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('3', 'H'),
        Card('3', 'S')
    ]

    table = [
        Card('3', 'C'),
        Card('2', 'H'),
        Card('9', 'D'),
        Card('10', 'C'),
        Card('K', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Three of a kind 1: ", choose_winner([p1, p2], table_cards=table) == [p2])


def check_choose_winner_three_of_a_kind2():
    p1 = Player(100)
    hand1 = [
        Card('3', 'D'),
        Card('3', 'C')
    ]

    p2 = Player(100)
    hand2 = [
        Card('3', 'H'),
        Card('3', 'S')
    ]

    table = [
        Card('3', 'C'),
        Card('2', 'H'),
        Card('9', 'D'),
        Card('10', 'C'),
        Card('K', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Three of a kind 2: ", choose_winner([p1, p2], table_cards=table) == [p1, p2])


def check_choose_winner_four_of_a_kind1():
    p1 = Player(100)
    hand1 = [
        Card('3', 'H'),
        Card('3', 'S')
    ]

    p2 = Player(100)
    hand2 = [
        Card('4', 'D'),
        Card('4', 'C')

    ]

    table = [
        Card('3', 'C'),
        Card('3', 'H'),
        Card('4', 'D'),
        Card('4', 'C'),
        Card('K', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Four of a kind 1: ", choose_winner([p1, p2], table_cards=table) == [p2])


def check_choose_winner_four_of_a_kind2():
    p1 = Player(100)
    hand1 = [
        Card('K', 'H'),
        Card('3', 'S')
    ]

    p2 = Player(100)
    hand2 = [
        Card('Q', 'D'),
        Card('4', 'C')

    ]

    table = [
        Card('2', 'C'),
        Card('2', 'H'),
        Card('2', 'D'),
        Card('2', 'C'),
        Card('9', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Four of a kind 2: ", choose_winner([p1, p2], table_cards=table) ==  [p1])


def check_choose_winner_flush1():
    p1 = Player(100)
    hand1 = [
        Card('Q', 'H'),
        Card('3', 'S')
    ]

    p2 = Player(100)
    hand2 = [
        Card('K', 'H'),
        Card('4', 'C')

    ]

    table = [
        Card('2', 'H'),
        Card('4', 'H'),
        Card('6', 'H'),
        Card('J', 'H'),
        Card('9', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner Flush: ", choose_winner([p1, p2], table_cards=table) ==  [p2])


def check_choose_winner_high_card1():
    p1 = Player(100)
    hand1 = [
        Card('Q', 'H'),
        Card('3', 'S')
    ]

    p2 = Player(100)
    hand2 = [
        Card('8', 'C'),
        Card('K', 'H'),
    ]

    table = [
        Card('2', 'H'),
        Card('4', 'S'),
        Card('A', 'C'),
        Card('J', 'H'),
        Card('9', 'C'),
    ]

    for c1, c2 in zip(hand1, hand2):
        p1.add_card(c1)
        p2.add_card(c2)
    
    print("Choose winner High Card: ", choose_winner([p1, p2], table_cards=table) ==  [p2])


check_flush_straight()
check_4of_a_kind()
check_fh()
check_flush()
check_straight()
check_3of_a_kind()
check_2_pairs()
check_pair()
check_high_card()
check_highest_card1()
check_highest_card2()
check_highest_card3()
check_choose_winner_fh1()
check_choose_winner_fh2()
check_choose_winner_fh3()
check_choose_winner_fh4()
check_choose_winner_straight1()
check_choose_winner_straight2()
check_choose_winner_straight3()
check_choose_winner_pair1()
check_choose_winner_pair2()
check_choose_winner_pair3()
check_choose_winner_two_pairs1()
check_choose_winner_two_pairs2()
check_choose_winner_two_pairs3()
check_choose_winner_three_of_a_kind1()
check_choose_winner_three_of_a_kind2()
check_choose_winner_four_of_a_kind1()
check_choose_winner_four_of_a_kind2()
check_choose_winner_flush1()
check_choose_winner_high_card1()