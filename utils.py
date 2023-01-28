import pygame
from collections import Counter
from Card import Card


def move_to_position(obj: pygame.Rect, position, speed=2):
    curr_x, curr_y = (obj.x, obj.y)
    dest_x, dest_y = position
    
    obj.move_ip()

def display_in_center(surface, scr, dx=0, dy=0):
    """
    Displays an object in center with option displacement dx (horizontal) and dy (vertical)
    """
    rect = surface.get_rect()
    w_width, w_height = scr.get_width(), scr.get_height()
    obj_width, obj_height = rect.w, rect.h
    scr.blit(surface, ((w_width-obj_width)/2+dx, (w_height-obj_height)/2+dy))


def display_cards(list, scr):
    """
    Displays cards in center
    """
    for idx, card in enumerate(list):
        spacing = 10
        width = Card.SIZE[0]
        total_width = (len(list)*(width+spacing)-spacing)/2
        displacement_x = -total_width + idx*width+spacing

        if card:
            display_in_center(card.image, scr, displacement_x)


def display_deck(deck, scr):
    for idx, card in enumerate(deck):
        display_in_center(card.image, scr, dx=-card.rect.w/2, dy=-200-idx//2)

def create_button(text, color, size=(200, 100)):
    """
    Creates button
    """
    width, height = size
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
