import texture
from tile_pos import TilePos
from world_renderer import WorldRenderer


class Tile:
	TEXTURE = texture.ErrorTexture

	def render(self, world_renderer: WorldRenderer, pos: TilePos):
		world_renderer.render_texture(self.TEXTURE, pos.get_pixel_pos())


class GrassTile(Tile):
	TEXTURE = texture.GrassTexture


class WaterTile(Tile):
	TEXTURE = texture.WaterTexture


class TreeTile(Tile):
	TEXTURE = texture.TreeTexture


class SandTile(Tile):
	TEXTURE = texture.SandTexture


class BlackSandTile(Tile):
	TEXTURE = texture.BlackSandTexture


class GravelTile(Tile):
	TEXTURE = texture.GravelTexture


class PathTile(Tile):
	TEXTURE = texture.PathTexture
