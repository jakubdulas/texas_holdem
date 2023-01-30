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
from GameState import GameState
from Action import Action
from Role import Role


def announce_winner():
    global gameState
    if len(set(table_cards)) == 5 and None not in table_cards:
        pass

def flop():
    global deck
    for _ in range(3):
        yield deck.pop(-1)


def player_generator(players=[]):
    """
    yields Player object on demand
    """
    if not players:
        for pos, name in zip(SEATS, PLAYER_NAMES):
            x, y = pos
            player_obj = Player(100, name, x, y)
            players.append(player_obj)
            yield player_obj
    else:
        for player in players:
            yield player


def next_players_move_generator():
    """
    yields Player object on demand
    """
    global players
    i = 0
    while True:
        player = players[i]
        if not player.out_of_game:
            player.start_move()
            yield player

        if i < len(players)-1:
            i += 1
        else:
            i = 0


def get_next_player(player):
    """
    returns next player
    """
    global players
    idx = players.index(player)
    if idx < len(players) - 1:
        return players[idx+1]
    return players[0]


def handle_action(action, player):
    """
    Handles action of a player
    """
    global biggest_call, player_biggest_call, total_pot

    if action == Action.CHECK:
        player.check()
    if action == Action.FOLD:
        player.fold()
        player_biggest_call = get_next_player(player)
    if action == Action.RAISE:
        player.raise_()
    if action == Action.CALL:
        m = 0
        if player.role == Role.SB and biggest_call < 1:
            m = player.call(1)
        elif player.role == Role.BB and biggest_call < 2:
            m = player.call(2)
        else:
            m = player.call(biggest_call)

        total_pot += m
        if biggest_call < player.money_in_pot:
            biggest_call = player.money_in_pot
            player_biggest_call = player


def reset_roles(players):
    for player in players:
        player.set_role(None)


def set_roles(players, players_move):
    reset_roles(players)
    start = players.index(players_move)
    players_to_get_role = players[start:]
    if len(players_to_get_role) > len(ROLES):
        for player in players[:len(players_to_get_role)-len(ROLES)]:
            players_to_get_role.append(player)
    
    for player, role in zip(players_to_get_role, ROLES):
        str_to_role = {
            "DEALER": Role.DEALER,
            "BB": Role.BB,
            "SB": Role.SB,
        }
        role = str_to_role[role]
        player.set_role(role)


pygame.init()
clock = pygame.time.Clock()

# sets initial gamestate to shoow players
gameState = GameState.SHOW_PLAYERS

# setting up screen and background
scr = pygame.display.set_mode(WINDOW_SIZE)
background = pygame.Surface(WINDOW_SIZE)
background.fill((0, 0, 0))

# adding table
poker_table = pygame.image.load('images/table.tiff')

# creating deck
deck = []
for suit in SUITS:
    for name in NAMES:
        deck.append(Card(name, suit))
random.shuffle(deck)

# setting position of the deck
set_deck_position(deck)

# game variables
total_pot = 0
players = []
table_cards = [None for _ in range(5)]
player_gen = player_generator()
players_move_gen = next_players_move_generator()
flop_gen = flop()
deal_num = 0
t = 0
biggest_call = 0
player_biggest_call = None
i = 0

# buttons
check_btn = create_button('check', (0, 128, 0))
fold_btn = create_button('fold', (128, 0, 0))
raise_btn = create_button('raise', (0, 0, 128))
call_btn = create_button('call', (128, 0, 128))
buttons = [
    check_btn,
    fold_btn,
    raise_btn,
    call_btn
]
idx_to_action = {
    0: Action.CHECK,
    1: Action.FOLD,
    2: Action.RAISE,
    3: Action.CALL
}
buttons_rect = []


if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if gameState == GameState.PLAYING:
                if event.type == pygame.MOUSEBUTTONUP:
                    players_in_game = [player for player in players if not player.out_of_game]

                    pos = pygame.mouse.get_pos()
                    clicked_rects = [btn for btn in buttons_rect
                                if btn.collidepoint(pos)]

                    if len(clicked_rects):
                        idx = buttons_rect.index(clicked_rects[0])
                        action = idx_to_action[idx]
                    
                        handle_action(action, players_move)
                        players_move = next(players_move_gen)

                        if players_move == player_biggest_call and action != Action.FOLD:
                            if len(set(table_cards)) == 1:
                                gameState = GameState.FLOP
                            elif len(set(table_cards)) == 4:
                                gameState = GameState.TURN
                            elif len(set(table_cards)) == 5 and None in table_cards:
                                gameState = GameState.RIVER
                        
        scr.blit(background, (0, 0))

        display_in_center(poker_table, scr)
        display_cards(table_cards, scr)
        display_pot(total_pot, scr)

        buttons_rect = display_buttons(buttons, scr)

        for c in deck:
            c.display(scr)

        if gameState == GameState.DEALING:
            try:
                player = next(player_gen)
                # print(player.name)
            except:
                deal_num += 1
                player_gen = player_generator()
                player = next(player_gen)

            if deal_num > 1:
                gameState = GameState.PLAYING
                players_move = next(players_move_gen)
                set_roles(players, players_move)
                player_biggest_call = player
            else:
                card = deck.pop(-1)
                player.add_card(card)
                pygame.time.delay(int(1000*t))
                t=TIME_DELAY

        if gameState == GameState.SHOW_PLAYERS:
            try:
                player = next(player_gen)
                players.append(player)
            except:
                gameState = GameState.DEALING
                player_gen = player_generator()
                t = 0

            pygame.time.delay(int(1000*t))
            t=TIME_DELAY

        if gameState == GameState.FLOP:
            try:
                card = next(flop_gen)
                table_cards[i] = card
                i += 1
            except:
                gameState = GameState.PLAYING
                flop_gen = flop()
                t = 0
            pygame.time.delay(int(1000*t))
            t=TIME_DELAY

        if gameState == GameState.TURN:
            card = deck.pop(-1)
            table_cards[3] = card
            gameState = GameState.PLAYING

        if gameState == GameState.RIVER:
            card = deck.pop(-1)
            table_cards[4] = card
            gameState = GameState.PLAYING

        for p in players:
            p.display(scr)

        announce_winner()
        
        clock.tick(30)
        pygame.display.flip()

pygame.quit()