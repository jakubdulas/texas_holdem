import pygame
from collections import Counter
from Card import Card
from constants import DECK_POSITION, BTN_SIZE


def display_buttons(buttons, scr):
    btn_rects = []
    for idx, button in enumerate(buttons):
        width = BTN_SIZE[0]
        total_width = ((len(buttons)-1)*(width))/2
        displacement_x = -total_width + idx*width

        btn_rects.append(display_in_center(button, scr, dx=displacement_x, dy=250))
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
    bar.fill((200, 200 ,200))

    text_rect = text.get_rect(center=(width/2, height/2))
    bar.blit(text, text_rect)

    display_in_center(bar, scr, dy=-80)


def display_in_center(surface, scr, dx=0, dy=0):
    """
    Displays an object in center with option displacement dx (horizontal) and dy (vertical).
    Returns rect object of displayed object
    """
    rect = surface.get_rect()
    w_width, w_height = scr.get_width(), scr.get_height()
    obj_width, obj_height = rect.w, rect.h
    return scr.blit(surface, ((w_width-obj_width)/2+dx, (w_height-obj_height)/2+dy))


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
    for idx, card in enumerate(deck):
        card.set_position(DECK_POSITION)

def create_button(text, color):
    """
    Creates button
    """
    width, height = BTN_SIZE
    button = pygame.Surface((width, height))
    button.fill(color)

    font = pygame.font.Font(None, 36)
    text = font.render(text, 1, (255, 255, 255))

    text_rect = text.get_rect(center=(width/2, height/2))
    button.blit(text, text_rect)

    return button


def find_repetitions(cards):
    """
    Returns tuples containing a card and number of its repetition if the card occurs more than 2 times.
    """
    names = list(card.name for card in cards)
    counter = Counter(names)
    most_common = list(filter(lambda x: x[1] > 1, counter.most_common(5)))
    most_common.sort(key=lambda x: x[1], reverse=True)
    return most_common


def is_straight(cards):
    """
    Return if cards are a sequence of 5 cards in increasing value (Ace can precede 2 and follow up King) 
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
    Returns True if all cards have the same suit. Returns False if they are not the same.
    """
    suits = [card.suit for card in cards]
    return len(set(suits)) == 1


def compare_full_houses(player_list):
    """
    Compares full houses and returns the players with the strongest ones.
    """
    winners = []
    best_toak_value = -1
    best_pair_value = -1
    high_card = -1
    for idx, (player, (combination, _)) in enumerate(player_list):
        toak, pair = find_repetitions(combination)

        if idx == 0:
            best_toak_value = Card.get_strength(toak[0]) * toak[1]
            best_pair_value = Card.get_strength(pair[0]) * pair[1]
            high_card = player.choose_high_card(combination)
            winners.append(player)
            continue

        temp_hand_value = Card.get_strength(toak[0]) * toak[1]

        if temp_hand_value > best_toak_value:
            winners = []
            winners.append(player)
            best_toak_value = temp_hand_value
        elif temp_hand_value == best_toak_value:
            temp_hand_value = Card.get_strength(pair[0]) * pair[1]
            if temp_hand_value > best_pair_value:
                winners = []
                winners.append(player)
                best_pair_value = temp_hand_value
            elif temp_hand_value == best_pair_value:
                temp_high_card = player.choose_high_card(combination)
                if temp_high_card > high_card:
                    winners = []
                    winners.append(player)
                    high_card = temp_high_card
                elif temp_high_card == high_card:
                    winners.append(player)
    return winners
        
def choose_winner(players, table_cards):
    """
    Returns list of winners
    """
    winners = []
    player_list = [(player, player.get_combination_and_hand_value(table_cards)) 
                    for player in players if not player.out_of_game]
    player_list.sort(key=lambda x: x[1][1], reverse=True)
    max_points = player_list[0][1][1]
    player_list = list(filter(lambda x: x[1][1] == max_points, player_list))

    if len(player_list) != 1:
        # if players have full house
        
        if max_points == 7: return compare_full_houses(player_list)


        
    return players[0]
