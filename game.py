"""
Texas Holdem by Jakub Dulas
"""

import pygame
import random
import sys
from constants import *
from utils import *
from Card import Card
from Player import Player


if __name__ == '__main__':
    pygame.init()

    # setting up screen and background
    scr = pygame.display.set_mode(WINDOW_SIZE)
    background = pygame.Surface(WINDOW_SIZE)
    background.fill((0, 0, 0))

    poker_table = pygame.image.load('images/table.png')

    clock = pygame.time.Clock()

    deck = []

    for suit in SUITS:
        for name in NAMES:
            deck.append(Card(name, suit))

    random.shuffle(deck)

    total_pot = 0
    table_cards = []

    for _ in range(5):
        table_cards.append(None)

    width, height = 100, 50

    check_btn = create_button('check', (20, 236, 125))

    players = []


    # deal
    for i in range(2):
        card = deck.pop(0)
        card.show()
        table_cards[i] = card

    for pos, name in zip(SEATS, PLAYER_NAMES):
        x, y = pos
        player = Player(name, 100, x, y)

        for _ in range(2):
            card = deck.pop(0)

            if name == "Kuba":
                card.show()

            player.add_card(card)
            players.append(player)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            character_clicked = False
            # if event.type == pygame.MOUSEBUTTONUP
        
        scr.blit(background, (0, 0))
        display_in_center(poker_table, scr)
        display_cards(table_cards, scr)
        display_deck(deck, scr)

        for player in players:
            player.display(scr)

        scr.blit(check_btn, (500, 600))
        pygame.display.flip()
