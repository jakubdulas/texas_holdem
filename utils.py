import pygame
from collections import Counter
from Card import Card
from constants import DECK_POSITION, BTN_SIZE
import matplotlib.pyplot as plt
from IPython import display
from Action import Action


def display_buttons(buttons, scr, dy=250):
    btn_rects = []
    for idx, button in enumerate(buttons):
        width = BTN_SIZE[0]
        total_width = ((len(buttons)-1)*(width))/2
        displacement_x = -total_width + idx*width

        btn_rects.append(display_in_center(
            button, scr, dx=displacement_x, dy=dy))
    return btn_rects


def display_pot(pot, scr):
    """
    Displays total pot.
    """
    text = f"Total pot: ${pot}"
    font = pygame.font.Font(None, 36)
    width, height = font.size(text)[0]+10, 40

    text = font.render(text, 1, (0, 0, 0))

    bar = pygame.Surface((width, height))
    bar.fill((200, 200, 200))

    text_rect = text.get_rect(center=(width/2, height/2))
    bar.blit(text, text_rect)

    display_in_center(bar, scr, dy=-80)


def display_in_center(surface, scr, dx=0, dy=0):
    """
    Displays an object in center with option displacement
    dx (horizontal) and dy (vertical).
    Returns rect object of displayed object
    """
    rect = surface.get_rect()
    w_width, w_height = scr.get_width(), scr.get_height()
    obj_width, obj_height = rect.w, rect.h
    return scr.blit(surface, ((w_width-obj_width)/2+dx,
                              (w_height-obj_height)/2+dy))


def display_cards(list, scr):
    """
    Displays cards in center
    """
    for idx, card in enumerate(list):
        width = Card.SIZE[0]
        total_width = ((len(list)-1)*(width))/2
        displacement_x = -total_width + idx*width

        if card:
            display_in_center(card.image, scr, displacement_x)


def set_deck_position(deck):
    for card in deck:
        card.set_position(DECK_POSITION)


def create_button(text, color, font_size=36, width=None):
    """
    Creates button
    """
    if width is None:
        width, height = BTN_SIZE
    else:
        height = BTN_SIZE[1]

    button = pygame.Surface((width, height))
    button.fill(color)

    font = pygame.font.SysFont(None, font_size)
    text = font.render(text, 1, (255, 255, 255))

    text_rect = text.get_rect(center=(width/2, height/2))
    button.blit(text, text_rect)

    return button


def create_text(text):
    """
    Creates text
    """
    font = pygame.font.SysFont(None, 36)
    text = font.render(text, 1, (241, 225, 127))
    return text


def find_repetitions(cards):
    """
    Returns tuples containing a card and number of its
    repetition if the card occurs more than 2 times.
    """
    names = list(card.name for card in cards)
    counter = Counter(names)
    most_common = list(filter(lambda x: x[1] > 1, counter.most_common(5)))
    most_common.sort(key=lambda x: x[1], reverse=True)
    return most_common


def is_straight(cards):
    """
    Return if cards are a sequence of 5 cards in increasing
    value (Ace can precede 2 and follow up King)
    """
    strengths = [card.strength for card in cards]
    cards = list(sorted(strengths))
    for idx in range(1, 4):
        if cards[idx] - cards[idx-1] != 1:
            return False

    if cards[4] - cards[3] == 1 or cards[4] - cards[0] == 12:
        return True

    return False


def is_flush(cards):
    """
    Returns True if all cards have the same suit.
    Returns False if they are not the same.
    """
    suits = [card.suit for card in cards]
    return len(set(suits)) == 1


def calculate_combination_strength(combination, type):
    """
    Returns strength of a combination.
    """
    if type == 9 or type == 5:
        combination.sort(key=lambda x: x.strength)
        if combination[4].strength - combination[0].strength == 12:
            return combination[3].strength
        return combination[4].strength
    elif type == 8:
        four_of_a_kind = find_repetitions(combination)[0][0]
        return Card.get_strength(four_of_a_kind)
    elif type == 7:
        (three_of_a_kind, _), (pair, _) = find_repetitions(combination)
        toak_val = Card.get_strength(three_of_a_kind)*100
        pair_val = Card.get_strength(pair)
        return toak_val + pair_val
    elif type == 6:
        combination.sort(key=lambda x: x.strength)
        return combination[4].strength
    elif type == 4:
        repetitions = find_repetitions(combination)
        if len(repetitions) == 0:
            return 0
        three_of_a_kind, _ = repetitions[0]
        return Card.get_strength(three_of_a_kind)
    elif type == 3:
        combination.sort(key=lambda x: x.strength, reverse=True)
        repetitions = find_repetitions(combination)
        if len(repetitions) == 0:
            return 0
        (pair1, _), (pair2,  _) = repetitions
        pair1 = Card.get_strength(pair1)*100
        pair2 = Card.get_strength(pair2)
        return pair1 + pair2
    elif type == 2:
        repetitions = find_repetitions(combination)
        if len(repetitions) == 0:
            return 0
        pair, _ = repetitions[0]
        return Card.get_strength(pair)
    return 0


def compare_full_houses(player_combination_value):
    """
    Compares full houses and returns the players with the strongest ones.
    """
    winners = []
    best_toak_value = -1
    best_pair_value = -1
    for idx, (player, (combination, _)) in enumerate(player_combination_value):
        toak, pair = find_repetitions(combination)

        # assume that first player has the best hand
        if idx == 0:
            best_toak_value = Card.get_strength(toak[0]) * toak[1]
            best_pair_value = Card.get_strength(pair[0]) * pair[1]
            winners.append(player)
            continue

        temp_hand_value = Card.get_strength(toak[0]) * toak[1]

        # if a player has stronger three of a kind,
        # set winners to = [] and add player to winners
        if temp_hand_value > best_toak_value:
            winners = []
            winners.append(player)
            best_toak_value = temp_hand_value

        # if a player has the same three of a kind, compare pairs
        elif temp_hand_value == best_toak_value:
            temp_hand_value = Card.get_strength(pair[0]) * pair[1]

            # if a player has stronger pair,
            # set winners to = [] and add player to winners
            if temp_hand_value > best_pair_value:
                winners = []
                winners.append(player)
                best_pair_value = temp_hand_value

            # if a player has the same pair, compare high cards
            elif temp_hand_value == best_pair_value:
                return compare_high_cards(player_combination_value)
    return winners


def compare_straights(player_combination_value):
    """
    Compares straights
    """

    winners = []
    highest_straight = 0
    for idx, (player, (combination, _)) in enumerate(player_combination_value):
        combination.sort(key=lambda x: x.strength)

        # assume that first player has the best hand
        if idx == 0:
            if combination[4].strength - combination[0].strength == 12:
                highest_straight = combination[3].strength
            else:
                highest_straight = combination[4].strength
            winners.append(player)
            continue

        # set strength of a straight
        if combination[4].strength - combination[0].strength == 12:
            temp_straight = combination[3].strength
        else:
            temp_straight = combination[4].strength

        # if a player has stronger straight,
        # set winners to = [] and add player to winners
        if temp_straight > highest_straight:
            winners = []
            winners.append(player)
            highest_straight = temp_straight

        # if a player has the same straight strength, compare high cards
        elif temp_straight == highest_straight:
            return compare_high_cards(player_combination_value)
    return winners


def compare_straights(player_combination_value):
    """
    Compares straights
    """

    winners = []
    highest_straight = 0
    for idx, (player, (combination, _)) in enumerate(player_combination_value):
        combination.sort(key=lambda x: x.strength)

        # assume that first player has the best hand
        if idx == 0:
            if combination[4].strength - combination[0].strength == 12:
                highest_straight = combination[3].strength
            else:
                highest_straight = combination[4].strength
            winners.append(player)
            continue

        # set strength of a straight
        if combination[4].strength - combination[0].strength == 12:
            temp_straight = combination[3].strength
        else:
            temp_straight = combination[4].strength

        # if a player has stronger straight,
        # set winners to = [] and add player to winners
        if temp_straight > highest_straight:
            winners = []
            winners.append(player)
            highest_straight = temp_straight

        # if a player has the same straight strength, compare high cards
        elif temp_straight == highest_straight:
            return compare_high_cards(player_combination_value)
    return winners


def compare_pairs(player_combination_value):
    """
    Compares pairs
    """
    winners = []
    highest_pair = 0
    for idx, (player, (combination, _)) in enumerate(player_combination_value):

        # assume that the first player has the best hand
        if idx == 0:
            highest_pair = calculate_combination_strength(combination, 2)
            winners.append(player)
            continue

        temp_pair = calculate_combination_strength(combination, 2)

        # if a player has stronger pair,
        # set winners to = [] and add player to winners
        if temp_pair > highest_pair:
            winners = []
            winners.append(player)
            highest_pair = temp_pair

        # if a player has the same pair strength, compare high cards
        elif temp_pair == highest_pair:
            return compare_high_cards(player_combination_value)

    return winners


def compare_two_pairs(player_combination_value):
    """
    Compares two pairs
    """
    winners = []
    highest_two_pairs = 0

    for idx, (player, (combination, _)) in enumerate(player_combination_value):

        # assume that the first player has the best hand
        if idx == 0:
            highest_two_pairs = calculate_combination_strength(combination, 3)
            winners.append(player)
            continue

        temp_pair = calculate_combination_strength(combination, 3)

        # if a player has stronger pairs,
        # set winners to = [] and add player to winners
        if temp_pair > highest_two_pairs:
            winners = []
            winners.append(player)
            highest_two_pairs = temp_pair

        # if a player has the same pairs strength, compare high cards
        elif temp_pair == highest_two_pairs:
            return compare_high_cards(player_combination_value)

    return winners


def compare_three_of_a_kind(player_combination_value):
    """
    Compares three of a kind
    """
    winners = []
    highest_score = 0

    for idx, (player, (combination, _)) in enumerate(player_combination_value):

        # assume that the first player has the best hand
        if idx == 0:
            highest_score = calculate_combination_strength(combination, 4)
            winners.append(player)
            continue

        temp_pair = calculate_combination_strength(combination, 4)

        # if a player has stronger three of a kind,
        # set winners to = [] and add player to winners
        if temp_pair > highest_score:
            winners = []
            winners.append(player)
            highest_score = temp_pair

        # if a player has the same three of a kind strength, compare high cards
        elif temp_pair == highest_score:
            return compare_high_cards(player_combination_value)

    return winners


def compare_four_of_a_kind(player_combination_value):
    """
    Compares four of a kind
    """
    winners = []
    highest_score = 0

    for idx, (player, (combination, _)) in enumerate(player_combination_value):

        # assume that the first player has the best hand
        if idx == 0:
            highest_score = calculate_combination_strength(combination, 8)
            winners.append(player)
            continue

        temp_pair = calculate_combination_strength(combination, 8)

        # if a player has stronger four of a kind,
        # set winners to = [] and add player to winners
        if temp_pair > highest_score:
            winners = []
            winners.append(player)
            highest_score = temp_pair

        # if a player has the same four of a kind strength, compare high cards
        elif temp_pair == highest_score:
            return compare_high_cards(player_combination_value)

    return winners


def compare_flushes(player_combination_value):
    """
    Compares flushes
    """
    winners = []
    highest_score = 0

    for idx, (player, (combination, _)) in enumerate(player_combination_value):

        # assume that the first player has the best hand
        if idx == 0:
            highest_score = calculate_combination_strength(combination, 6)
            winners.append(player)
            continue

        temp_flush = calculate_combination_strength(combination, 6)

        # if a player has stronger flush,
        # set winners to = [] and add player to winners
        if temp_flush > highest_score:
            winners = []
            winners.append(player)
            highest_score = temp_flush

        # if a player has the same flush strength, compare high cards
        elif temp_flush == highest_score:
            return compare_high_cards(player_combination_value)

    return winners


def compare_high_cards(player_combination_value):
    """
    Compares high cards
    """
    winners = []
    high_card = -1
    second_card = -1

    for idx, (player, (combination, _)) in enumerate(
                                           player_combination_value):
        temp_high_card = player.choose_high_card(combination)

        if idx == 0:
            high_card = temp_high_card
            if player.hand[0].strength == high_card:
                second_card = player.hand[1].strength
            else:
                second_card = player.hand[0].strength
            winners.append(player)
            continue

        # if a player has a higher card,
        # set winners to = [] and add player to winners
        if temp_high_card > high_card:
            winners = []
            winners.append(player)
            high_card = temp_high_card

        # if a player has the same card hight, add player to winners
        elif temp_high_card == high_card and high_card != 0:
            if player.hand[0].strength == high_card:
                temp_second_card = player.hand[1].strength
            else:
                temp_second_card = player.hand[0].strength

            if temp_second_card > second_card:
                winners = []
                winners.append(player)
            elif temp_second_card == second_card:
                winners.append(player)

        elif temp_high_card == high_card and high_card == 0:
            winners.append(player)

    return winners


def choose_winner(players, table_cards):
    """
    Returns list of winners
    """
    player_combination_value = [(player, player.get_combination_and_hand_value
                                 (table_cards)) for player in players]

    player_combination_value.sort(key=lambda x: x[1][1], reverse=True)
    max_points = player_combination_value[0][1][1]

    player_combination_value = list(filter(
        lambda x: x[1][1] == max_points, player_combination_value))

    if len(player_combination_value) != 1:
        if max_points == 7:
            return compare_full_houses(player_combination_value)
        if max_points == 6:
            return compare_flushes(player_combination_value)
        elif max_points == 8:
            return compare_four_of_a_kind(player_combination_value)
        elif max_points == 5 or max_points == 9:
            return compare_straights(player_combination_value)
        elif max_points == 4:
            return compare_three_of_a_kind(player_combination_value)
        elif max_points == 3:
            return compare_two_pairs(player_combination_value)
        elif max_points == 2:
            return compare_pairs(player_combination_value)
        elif max_points == 1:
            return compare_high_cards(player_combination_value)

    return [player_combination_value[0][0]]


def plot(balances, mean_income):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Money')
    plt.plot(balances)
    plt.plot(mean_income)
    plt.ylim(ymin=0)
    plt.text(len(balances)-1, balances[-1], str(balances[-1]))
    plt.text(len(mean_income)-1, mean_income[-1], str(mean_income[-1]))
    plt.show(block=False)
    plt.pause(.1)


def plot_bars(taken_actions):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Actions')
    plt.ylabel('Number of taken actions')
    taken_actions = Counter(taken_actions).most_common(3)
    xs, ys = zip(*taken_actions)
    xs = list(xs)

    for idx, x in enumerate(xs):
        if x == Action.CALL:
            xs[idx] = 'Call'
        elif x == Action.RAISE:
            xs[idx] = 'Raise'
        elif x == Action.FOLD:
            xs[idx] = 'Fold'

    plt.bar(xs, ys, width=0.4)
    plt.ylim(ymin=0)
    plt.show(block=False)
    plt.pause(.1)
