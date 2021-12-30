from enum import Enum, auto


class PlayerState(Enum):
	IDLE = 0
	WALKING = auto()
	BOAT_IDLE = auto()
	BOAT_SAILING = auto()