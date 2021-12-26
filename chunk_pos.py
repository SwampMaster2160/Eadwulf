from typing import Tuple


class ChunkPos:
	x: int
	y: int

	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

	def get_tuple(self) -> Tuple[int, int]:
		return self.x, self.y
