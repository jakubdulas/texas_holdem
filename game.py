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
    global gameState, winner_text, total_pot
    if len(set(table_cards)) == 5 and None not in table_cards:
        winners = choose_winner(players, table_cards)
        text = f"${total_pot} wygrywa: "
        winners_text = ""
        win_per_player = round(total_pot/len(winners), 2)
        total_pot = 0

        for winner in winners:
            winners_text += winner.name + " "
            winner.money += win_per_player
        
        winner_text = create_text(text+winners_text)

        for player in players:
            if player.money == 0:
                player.out_of_game = True

        gameState = GameState.ENDED


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
            if not player.out_of_game:
                yield player


def next_players_move_generator():
    """
    yields Player object on demand and starts its move
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


def handle_action(action, player):
    """
    Handles action of a player
    """
    global biggest_call, player_biggest_call, total_pot, players_move, gameState, players_in_game

    if action == Action.CHECK and player.money_in_pot == biggest_call:
        if (player.role == Role.SB and biggest_call < 1) or \
            (player.role == Role.BB and biggest_call < 2):
            return False
        player.check()
        return True
    if action == Action.FOLD:
        if (player.role == Role.SB and biggest_call < 1) or \
            (player.role == Role.BB and biggest_call < 2):
            return False

        players_move = next(players_move_gen)

        if players_move.money == 0:
            gameState = GameState.ALL_IN

        player.fold()
        return False
    if action == Action.RAISE and not any(list(map(lambda x: x.money == 0, players_in_game))):
        total_pot += player.raise_(biggest_call)
        if biggest_call < player.money_in_pot or player.money == 0:
            biggest_call = player.money_in_pot
            player_biggest_call = player

        return True
    if action == Action.CALL:
        m = 0
        if player.role == Role.SB and biggest_call < 1:
            m = player.call(1)
        elif player.role == Role.BB and biggest_call < 2:
            m = player.call(2)
        else:
            m = player.call(biggest_call)

        total_pot += m
        if biggest_call < player.money_in_pot or player.money == 0:
            biggest_call = player.money_in_pot
            player_biggest_call = player

        return True
    return False


def reset_roles(players):
    for player in players:
        player.set_role(None)


def set_roles(players, players_move):
    reset_roles(players)
    players = [player for player in players if not player.out_of_game]
    start = players.index(players_move)
    players_to_get_role = players[start:]
    if len(players_to_get_role) > len(ROLES):
        players_to_get_role = players_to_get_role[:3]
    elif len(players_to_get_role) < len(ROLES):
        stop = len(ROLES) - len(players_to_get_role)
        for player in players[:stop]:
            players_to_get_role.append(player)
    
    for player, role in zip(players_to_get_role, ROLES):
        str_to_role = {
            "DEALER": Role.DEALER,
            "BB": Role.BB,
            "SB": Role.SB,
        }
        role = str_to_role[role]
        player.set_role(role)

    
def reset_game():
    global deck, gameState,total_pot, players, table_cards, dealer_idx, deal_num, biggest_call, \
        player_gen, players_move_gen, t

    deck = []
    for suit in SUITS:
        for name in NAMES:
            deck.append(Card(name, suit))
    random.shuffle(deck)

    for player in players:
        player.reset()

    gameState = GameState.DEALING
    total_pot = 0

    table_cards = [None for _ in range(5)]

    dealer_idx += 1
    if dealer_idx == len(players): dealer_idx = 0
    set_deck_position(deck)
    biggest_call = 0
    deal_num = 0

    t = 0

    player_gen = player_generator()
    players_move_gen = next_players_move_generator()


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
winner_text = None
dealer_idx = 0
iters = 0

# buttons
check_btn = create_button('check', (0, 128, 0))
fold_btn = create_button('fold', (128, 0, 0))
raise_btn = create_button('raise $5', (0, 0, 128))
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
                    
                        if handle_action(action, players_move):
                            players_move = next(players_move_gen)

                            if players_move.money == 0:
                                gameState = GameState.ALL_IN

                            elif players_move == player_biggest_call and action != Action.FOLD:
                                if len(set(table_cards)) == 1:
                                    gameState = GameState.FLOP
                                elif len(set(table_cards)) == 4:
                                    gameState = GameState.TURN
                                elif len(set(table_cards)) == 5 and None in table_cards:
                                    gameState = GameState.RIVER
                        
        scr.blit(background, (0, 0))

        display_in_center(poker_table, scr)

        if GameState.END_GAME_SCREEN == gameState:
            clock.tick(30)
            pygame.display.flip()
            continue

        display_cards(table_cards, scr)
        display_pot(total_pot, scr)

        buttons_rect = display_buttons(buttons, scr)

        for c in deck:
            c.display(scr)

        if gameState == GameState.DEALING:
            try:
                player = next(player_gen)
            except:
                deal_num += 1
                player_gen = player_generator()
                player = next(player_gen)

            if deal_num > 1:
                gameState = GameState.PLAYING
                players_move = next(players_move_gen)
                players_in_game = [player for player in players if not player.out_of_game]

                if dealer_idx >= len(players_in_game):
                    dealer_idx = 0

                while players_in_game[dealer_idx].out_of_game:
                    dealer_idx += 1
                    if dealer_idx == len(players_in_game):
                        dealer_idx = 0
                while players_in_game[dealer_idx] != players_move:
                    players_move.is_its_move = False
                    players_move = next(players_move_gen)
                set_roles(players, players_move)
                player_biggest_call = players_move
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
                card.show()
                table_cards[i] = card
                i += 1
            except:
                gameState = GameState.PLAYING
                flop_gen = flop()
                t = 0
                i = 0
            pygame.time.delay(int(1000*t))
            t=TIME_DELAY

        if gameState == GameState.TURN:
            card = deck.pop(-1)
            card.show()
            table_cards[3] = card
            gameState = GameState.PLAYING

        if gameState == GameState.RIVER:
            card = deck.pop(-1)
            card.show()
            table_cards[4] = card
            gameState = GameState.PLAYING
        
        if gameState == GameState.ALL_IN:
            if None not in table_cards:
                gameState = GameState.PLAYING
                t = 0
            else:
                pygame.time.delay(int(1000*t))
                card = deck.pop(-1)
                idx = table_cards.index(None)
                card.show()
                table_cards[idx] = card
                t=TIME_DELAY

        for p in players:
            p.display(scr)

        if gameState == GameState.ENDED:
            iters += 1
            display_in_center(winner_text, scr, dy=-300)
            if iters == 100:
                reset_game()
                iters = 0
                players_in_game = [player for player in players if not player.out_of_game]
                if len(players_in_game) == 1:
                    gameState = GameState.END_GAME_SCREEN
        else:
            announce_winner()
        
        clock.tick(30)
        pygame.display.flip()

pygame.quit()