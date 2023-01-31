import pygame


class Card(pygame.sprite.Sprite):
    SIZE = (72, 100)
    NAME_TO_STRENGTH = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 11,
    }

    def __init__(self, name, suit):
        super(Card, self).__init__()
        self.is_hidden = True
        self.name = name
        self.suit = suit

        self.image_front = pygame.image.load(f'images/Cards_Dark/{suit}{name}.png')
        self.image_back = pygame.image.load('images/back.tiff')

        self.image_front = pygame.transform.scale(self.image_front, self.SIZE)
        self.image_back = pygame.transform.scale(self.image_back, self.SIZE)

        self.rect = self.image_front.get_rect()

    @property
    def image(self):
        return self.image_back if self.is_hidden else self.image_front

    @property
    def strength(self):
        strength = self.NAME_TO_STRENGTH.get(self.name, None)
        if strength is None:
            strength = int(self.name)

        return strength

    def set_position(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def rotate(self, angle):
        self.image_front = pygame.transform.rotate(self.image_front, angle)
        self.image_back = pygame.transform.rotate(self.image_back, angle)

    def hide(self):
        self.is_hidden = True

    def show(self):
        self.is_hidden = False

    def display(self, scr, pos=None):
        if pos == None:
            pos = self.rect
        scr.blit(self.image, pos)
    
    def get_rect(self):
        return self.rect

    @classmethod
    def get_strength(cls, card_str):
        strength = cls.NAME_TO_STRENGTH.get(card_str, None)
        if strength is None:
            strength = int(card_str)
        return strength
