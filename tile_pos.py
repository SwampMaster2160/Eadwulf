from pixel_pos import PixelPos


class TilePos:
	x: int
	y: int
	
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y
		
	def get_pixel_pos(self) -> PixelPos:
		return PixelPos(self.x * 16, self.y * 16)
