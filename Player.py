import pygame
from utils import *
from Role import Role

class Player(pygame.sprite.Sprite):
    def __init__(self, name, money, x, y):
        super(Player, self).__init__()
        self.rect = pygame.Rect(x, y, 50, 50)
        self.hand = []
        self.money = money
        self.name = name
        self.out_of_game = False
        self.is_its_move = False
        self.role = None
        self.money_in_pot = 0

    def display(self, scr):
        x, y = self.rect.x + 20, self.rect.y
        for card in self.hand:
            card.set_position((x, y))
            card.display(scr)
            x -= 40
        
        text = f"{self.name} ${self.money} {self.str_role}"
        font = pygame.font.Font(None, 36)
        width, height = font.size(text)[0]+10, 40

        text = font.render(text, 1, (0, 0, 0))

        bar = pygame.Surface((width, height))

        if not self.is_its_move:
            bar.fill((200, 200 ,200))
        else:
            # if self.out_of_game:
            #     bar.fill((250, 70, 70))
            # else:
            bar.fill((0, 100, 0))

        text_rect = text.get_rect(center=(width/2, height/2))
        bar.blit(text, text_rect)

        x = self.rect.x - bar.get_width()/2 + 50
        scr.blit(bar, (x, y-40))

    def set_role(self, role):
        self.role = role

    @property
    def str_role(self):
        role_to_str = {
            Role.BB: "BB",
            Role.SB: "SB",
            Role.DEALER: "DEALER",
            None: ''
        }
        return role_to_str[self.role]

    def add_card(self, card):
        self.hand.append(card)
        card.rotate(-30 if len(self.hand) == 1 else 30)

    def get_combination_and_hand_value(self, cards):
        """
        Returns the best combination for a player and strength of the combination
        Strengths:
        - 9 - straight flush
        - 8 - four of a kind
        - 7 - full house
        - 6 - flush
        - 5 - straight
        - 4 - three of a kind
        - 3 - two pairs
        - 2 - one pair
        - 1 - high card
        """
        points = 0
        i = 0
        combination = cards.copy()
        best_combination = combination
        for i in range(5):
            for card in self.hand:
                combination = cards.copy()
                combination[i] = card
                new_points = self._get_hand_value(combination)
                if new_points > points:
                    points = new_points
                    best_combination = combination

        i=1
        j=0

        while j != 4:
            combination = cards.copy()
            combination[j] = self.hand[0]
            combination[i] = self.hand[1]

            new_points = self._get_hand_value(combination)
            if new_points > points:
                points = new_points
                best_combination = combination

            if i == 4:
                j += 1
                i = j
            i+=1

        return best_combination, points

    def _get_hand_value(self, combination):
        """
        returns a hand value given a combination
        """
        is_flush_ = is_flush(combination)
        is_straight_ = is_straight(combination)
        most_common = find_repetitions(combination)

        # straight flush
        if is_flush_ and is_straight_: return 9

        # 4 of a kind
        if len(most_common) == 1 and most_common[0][1] == 4: return 8
        
        # full house
        if len(most_common) == 2 and most_common[0][1] + most_common[1][1] == 5: return 7

        # flush
        if is_flush_: return 6

        # straight
        if is_straight_: return 5

        # 3 of a kind
        if len(most_common) == 1 and most_common[0][1] == 3: return 4

        # 2 pairs
        if len(most_common) == 2 and most_common[0][1] + most_common[1][1] == 4: return 3

        # 1 pair
        if len(most_common) == 1 and most_common[0][1] == 2: return 2

        # high card
        return 1

    def set_role(self, role):
        self.role = role

    def finish_move(self):
        self.is_its_move = False

    def start_move(self):
        self.is_its_move = True

    def fold(self):
        self.out_of_game = True
        self.finish_move()

    def call(self, biggest_call):
        """
        return how much money a player gave to pot
        """
        to_call = biggest_call - self.money_in_pot
        self.money_in_pot += to_call
        self.money -= to_call
        self.finish_move()
        return to_call

    def check(self):
        self.finish_move()

    def raise_(self):
        self.finish_move()