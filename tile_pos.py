import random

from chunk_pos import ChunkPos
from pixel_pos import PixelPos


class TilePos:
	x: int
	y: int
	
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

	def __add__(self, other):
		return TilePos(self.x + other.x, self.y + other.y)
		
	def get_pixel_pos(self) -> PixelPos:
		return PixelPos(self.x * 16, self.y * 16)

	def get_chunk_pos(self) -> ChunkPos:
		return ChunkPos(self.x // 64, self.y // 64)

	def get_chunk_offset(self):
		return TilePos(self.x % 64, self.y % 64)

	def random(self, seed: int,  layer: int) -> float:
		random.seed(hash((self.x, self.y, seed, layer)))
		return random.random()

	def perlin(self, seed: int, layer_min: int, layer_max: int, layer_offset: int) -> float:
		height = 0.
		for layer in range(layer_min, layer_max):
			layer_size = 1 << layer
			layer_start_x = self.x // layer_size * layer_size
			layer_start_y = self.y // layer_size * layer_size
			layer_start = TilePos(layer_start_x, layer_start_y)

			height_0 = layer_start.random(seed, layer - layer_min + layer_offset)
			height_1 = (layer_start + TilePos(layer_size, 0)).random(seed, layer - layer_min + layer_offset)
			height_2 = (layer_start + TilePos(0, layer_size)).random(seed, layer - layer_min + layer_offset)
			height_3 = (layer_start + TilePos(layer_size, layer_size)).random(seed, layer - layer_min + layer_offset)

			x_gradient_0 = (height_1 - height_0) / layer_size
			p_0 = x_gradient_0 * self.x + (height_0 - x_gradient_0 * layer_start_x)
			x_gradient_1 = (height_3 - height_2) / layer_size
			p_1 = x_gradient_1 * self.x + (height_2 - x_gradient_1 * layer_start_x)

			y_gradient = (p_1 - p_0) / layer_size
			layer_height = y_gradient * self.y + (p_0 - y_gradient * layer_start_y)

			height += layer_height * layer_size
		return height
