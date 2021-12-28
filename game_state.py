from enum import Enum, auto


class GameState(Enum):
	INGAME = auto()
	IN_MENU = auto()
	EXITING = auto()
