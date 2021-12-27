import texture
from tile_pos import TilePos
from world_renderer import WorldRenderer


class Tile:
	TEXTURE = texture.ErrorTexture
	CAN_WALK = 1

	def render(self, world_renderer: WorldRenderer, pos: TilePos):
		world_renderer.render_texture(self.TEXTURE, pos.get_pixel_pos())

	def can_walk(self, player):
		return self.CAN_WALK


class GrassTile(Tile):
	TEXTURE = texture.GrassTexture


class WaterTile(Tile):
	TEXTURE = texture.WaterTexture
	CAN_WALK = 0


class TreeTile(Tile):
	TEXTURE = texture.TreeTexture
	CAN_WALK = 0


class SandTile(Tile):
	TEXTURE = texture.SandTexture


class BlackSandTile(Tile):
	TEXTURE = texture.BlackSandTexture


class GravelTile(Tile):
	TEXTURE = texture.GravelTexture


class PathTile(Tile):
	TEXTURE = texture.PathTexture


class FlowersTile(Tile):
	TEXTURE = texture.FlowersTexture
