from typing import Tuple


class PixelPos:
	x: int
	y: int
	
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y
		
	def __add__(self, other):
		return PixelPos(self.x + other.x, self.y + other.y)
	
	def to_tuple(self) -> Tuple[int, int]:
		return self.x, self.y
