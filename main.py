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


class Poker:
    def __init__(self):
        # setting up screen and background
        self.scr = pygame.display.set_mode(WINDOW_SIZE)
        self.background = pygame.Surface(WINDOW_SIZE)
        self.background.fill((0, 0, 0))
        self.poker_table = pygame.image.load('images/table.tiff')
        
        # delay rate affects time after which cards show up
        self.delay_rate = 5

        # game variables
        self.players = []
        self.flop_gen = self.flop_generator()
        self.gameState = GameState.SHOW_PLAYERS
        self.winner_text = None
        self.dealer_idx = 0
        self.players_move = None
        self.reset_game(True)

        # buttons
        check_btn = create_button('check', (0, 128, 0))
        fold_btn = create_button('fold', (128, 0, 0))
        raise_btn = create_button('raise $5', (0, 0, 128))
        call_btn = create_button('call', (128, 0, 128))
        self.buttons = [
            check_btn,
            fold_btn,
            raise_btn,
            call_btn
        ]
        self.idx_to_action = {
            0: Action.CHECK,
            1: Action.FOLD,
            2: Action.RAISE,
            3: Action.CALL
        }
        self.buttons_rect = []


    def reset_game(self, init=False):
        """
        resets game variables
        """

        # creating a deck
        self.deck = []
        for suit in SUITS:
            for name in NAMES:
                card = Card(name, suit)
                card.hide()
                self.deck.append(card)
        random.shuffle(self.deck)
        set_deck_position(self.deck)

        self.table_cards = [None for _ in range(5)]

        for player in self.players:
            player.reset()

        for player in self.players:
            if player.money == 0:
                player.out_of_game = True

        self.players_in_game = [player for player in self.players if not player.out_of_game]
        

        if not init: 
            self.gameState = GameState.DEALING
            self.dealer_idx += 1
            if self.dealer_idx == len(self.players_in_game):
                self.dealer_idx = 0
            self.player_gen = self.player_generator()
        else:
            self.player_gen = self.player_generator(True)
            
        self.players_move_gen = self.next_players_move_generator()

        self.total_pot = 0
        self.biggest_call = 0
        self.deal_num = 0
        self.player_biggest_call = None
        self.iters = 0
        self.winner_text = None
        # self.players_move = None


    def player_generator(self, create_players = False):
        """
        yields Player object on demand
        """
        if create_players:
            for pos, name in zip(SEATS, PLAYER_NAMES):
                x, y = pos
                player_obj = Player(100, name, x, y)
                yield player_obj
        else:
            for player in self.players:
                if not player.out_of_game:
                    yield player


    def next_players_move_generator(self):
        """
        yields Player object on demand and starts its move
        """
        i = 0
        while True:
            player = self.players[i]
            if not player.out_of_game:
                player.start_move()
                yield player

            if i < len(self.players)-1:
                i += 1
            else:
                i = 0


    def flop_generator(self):
        for _ in range(3):
            yield self.deck.pop(-1)


    def set_roles(self):
        self.reset_roles()
        start = self.players_in_game.index(self.players_move)
        players_to_get_role = self.players_in_game[start:]
        if len(players_to_get_role) > len(ROLES):
            players_to_get_role = players_to_get_role[:3]
        elif len(players_to_get_role) < len(ROLES):
            stop = len(ROLES) - len(players_to_get_role)
            for player in self.players_in_game[:stop]:
                players_to_get_role.append(player)
        
        for player, role in zip(players_to_get_role, ROLES):
            str_to_role = {
                "DEALER": Role.DEALER,
                "BB": Role.BB,
                "SB": Role.SB,
            }
            role = str_to_role[role]
            player.set_role(role)


    def reset_roles(self):
        for player in self.players:
            player.set_role(None)


    def handle_action(self, action):
        """
        Handles action of a player
        """
        if action == Action.CHECK and self.players_move.money_in_pot == self.biggest_call:
            if (self.players_move.role == Role.SB and self.biggest_call < 1) or \
                (self.players_move.role == Role.BB and self.biggest_call < 2):
                return False
            self.players_move.check()

            return True

        if action == Action.FOLD:
            if (self.players_move.role == Role.SB and self.biggest_call < 1) or \
                (self.players_move.role == Role.BB and self.biggest_call < 2):
                return False

            self.players_in_game.pop(self.players_in_game.index(self.players_move))
            self.players_move.fold()

            if len(self.players_in_game) == 1:
                self.gameState = GameState.ENDED

            if self.players_move == self.player_biggest_call:
                self.players_move = next(self.players_move_gen)
                self.player_biggest_call = self.players_move
            else:
                self.players_move = next(self.players_move_gen)

            if self.players_move.money == 0:
                self.gameState = GameState.ALL_IN

            return False

        if action == Action.RAISE and not any(list(map(lambda x: x.money == 0, self.players_in_game))):
            self.total_pot += self.players_move.raise_(self.biggest_call)
            if self.biggest_call < self.players_move.money_in_pot or self.players_move.money == 0:
                self.biggest_call = self.players_move.money_in_pot
                self.player_biggest_call = self.players_move


            return True

        if action == Action.CALL:
            m = 0
            if self.players_move.role == Role.SB and self.biggest_call < 1:
                m = self.players_move.call(1)
            elif self.players_move.role == Role.BB and self.biggest_call < 2:
                m = self.players_move.call(2)
            else:
                m = self.players_move.call(self.biggest_call)

            self.total_pot += m
            if self.biggest_call < self.players_move.money_in_pot or self.players_move.money == 0:
                self.biggest_call = self.players_move.money_in_pot
                self.player_biggest_call = self.players_move

            return True
        return False
    

    def betting(self, action):            
        if self.handle_action(action):
            self.players_move = next(self.players_move_gen)

            if len(set(self.table_cards)) == 5 and None not in self.table_cards and \
                    self.player_biggest_call == self.players_move:
                self.gameState = GameState.ENDED

            if self.players_move.money == 0:
                self.gameState = GameState.ALL_IN

            elif self.players_move == self.player_biggest_call:
                if len(set(self.table_cards)) == 1:
                    self.gameState = GameState.FLOP
                elif len(set(self.table_cards)) == 4:
                    self.gameState = GameState.TURN
                elif len(set(self.table_cards)) == 5 and None in self.table_cards:
                    self.gameState = GameState.RIVER

                    
    def show_players(self):
        try:
            if self.iters % self.delay_rate == 0:
                player = next(self.player_gen)
                self.players.append(player)
        except:
            self.gameState = GameState.DEALING
            self.player_gen = self.player_generator()
            self.iters = 0

        self.iters += 1


    def dealing(self):
        if self.iters % self.delay_rate == 0:
            try:
                player = next(self.player_gen)
            except:
                self.deal_num += 1
                self.player_gen = self.player_generator()
                player = next(self.player_gen)
                self.iters = 0

            if self.deal_num > 1:
                self.gameState = GameState.BETTING
                self.players_move = next(self.players_move_gen)
                self.players_in_game = [player for player in self.players if not player.out_of_game]

                if self.dealer_idx >= len(self.players_in_game):
                    self.dealer_idx = 0

                while self.players_in_game[self.dealer_idx].out_of_game:
                    self.dealer_idx += 1
                    if self.dealer_idx == len(self.players_in_game):
                        self.dealer_idx = 0
                while self.players_in_game[self.dealer_idx] != self.players_move:
                    self.players_move.is_its_move = False
                    self.players_move = next(self.players_move_gen)

                self.set_roles()

                self.player_biggest_call = self.players_move
            else:
                card = self.deck.pop(-1)
                player.add_card(card)

        self.iters += 1


    def flop(self):
        if self.iters % self.delay_rate == 0:
            try:
                card = next(self.flop_gen)
                card.show()
                idx = self.table_cards.index(None)
                self.table_cards[idx] = card
            except:
                self.gameState = GameState.BETTING
                self.flop_gen = self.flop_generator()
                self.iters = 0
        self.iters += 1


    def turn(self):
        card = self.deck.pop(-1)
        card.show()
        self.table_cards[3] = card
        self.gameState = GameState.BETTING


    def river(self):
        card = self.deck.pop(-1)
        card.show()
        self.table_cards[4] = card
        self.gameState = GameState.BETTING


    def all_in(self):
        if None not in self.table_cards:
            self.gameState = GameState.ENDED
            self.iters = 0
        else:
            if self.iters % self.delay_rate == 0:
                card = self.deck.pop(-1)
                idx = self.table_cards.index(None)
                card.show()
                self.table_cards[idx] = card
        self.iters += 1


    def display_objects(self):
        # displaying objects on the screen
        self.scr.blit(self.background, (0, 0))
        display_in_center(self.poker_table, self.scr)

        if self.gameState == GameState.END_GAME_SCREEN:
            clock.tick(30)
            pygame.display.flip()
            return
        
        display_cards(self.table_cards, self.scr)
        display_pot(self.total_pot, self.scr)

        if self.players_move is not None:
            if not self.players_move.is_bot:
                self.buttons_rect = display_buttons(self.buttons, self.scr)

        for p in self.players:
            p.display(self.scr)
        
        for c in self.deck:
            c.display(self.scr)


    def show_all_cards(self):
        for player in self.players_in_game:
            player.show_hand()


    def announce_winner(self):
        if len(self.players_in_game) == 1:
            winner = self.players_in_game[0]

            text = f"${self.total_pot} wins: " + winner.name
            win = self.total_pot

            winner.money += win
            
            self.winner_text = create_text(text)
        else: 
            self.show_all_cards()
            winners = choose_winner(self.players_in_game, self.table_cards)
            text = f"${self.total_pot} wins: "
            winners_text = ""
            win_per_player = round(self.total_pot/len(winners), 2)

            for winner in winners:
                winners_text += winner.name + " "
                winner.money += win_per_player
            
            self.winner_text = create_text(text+winners_text)


    def game_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if self.gameState == GameState.BETTING:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_rects = [btn for btn in self.buttons_rect
                                if btn.collidepoint(pos)]

                    if len(clicked_rects):
                        idx = self.buttons_rect.index(clicked_rects[0])
                        action = self.idx_to_action[idx]
                        self.betting(action)
                        self.iters = 0
        
        if self.gameState == GameState.BETTING:
            self.iters += 1
            if self.players_move.is_bot and self.iters % 20 == 0:
                action = self.players_move.take_action()
                self.betting(action)
                self.iters = 0

        self.display_objects()

        if self.gameState == GameState.SHOW_PLAYERS:
            self.show_players()

        if self.gameState == GameState.DEALING:
            self.dealing()

        if self.gameState == GameState.FLOP:
            self.flop()

        if self.gameState == GameState.TURN:
            self.turn()

        if self.gameState == GameState.RIVER:
            self.river()
        
        if self.gameState == GameState.ALL_IN:
            self.all_in()

        if self.gameState == GameState.ENDED:
            if not self.winner_text:
                self.announce_winner()
            self.iters += 1
            display_in_center(self.winner_text, self.scr, dy=-300)
            if self.iters == 100:
                self.reset_game()
                if len(self.players_in_game) == 1:
                    self.gameState = GameState.END_GAME_SCREEN



if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    poker = Poker()
    
    while True:
        poker.game_step()
        
        clock.tick(30)
        pygame.display.flip()

pygame.quit()