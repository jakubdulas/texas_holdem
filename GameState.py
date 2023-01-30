from enum import Enum


class GameState(Enum):
  PLAYING = 0
  DEALING = 1
  ENDED = 2
  SHOW_PLAYERS = 3
  FLOP = 4
  TURN = 5
  RIVER = 6
  ALL_IN = 7
