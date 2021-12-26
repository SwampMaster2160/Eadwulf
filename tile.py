import texture
from tile_pos import TilePos
from world_renderer import WorldRenderer


class Tile:
	TEXTURE = texture.Error

	def render(self, world_renderer: WorldRenderer, pos: TilePos):
		world_renderer.render_texture(self.TEXTURE, pos.get_pixel_pos())


class GrassTile(Tile):
	TEXTURE = texture.Grass
