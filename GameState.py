from enum import Enum


class GameState(Enum):
  PLAYING = 0
  DEALING = 1
  ENDED = 2
  SHOW_PLAYERS = 3
