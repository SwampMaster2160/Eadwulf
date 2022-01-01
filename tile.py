import texture
from player_state import PlayerState
from tile_pos import TilePos
from world_renderer import WorldRenderer


class Tile:
	TEXTURE = texture.ErrorTexture
	CAN_WALK = 1

	def render(self, world_renderer: WorldRenderer, pos: TilePos, tile_stack, height: int):
		world_renderer.render_texture(self.TEXTURE, pos.get_pixel_pos())

	def can_walk(self, player):
		return self.CAN_WALK


class GroundTile(Tile):
	pass


class ChunkLoadingTile(GroundTile):
	TEXTURE = texture.ChunkLoadingTexture
	CAN_WALK = 0


class GrassTile(GroundTile):
	TEXTURE = texture.GrassTexture


class WaterTile(GroundTile):
	TEXTURE = texture.WaterTexture
	CAN_WALK = 0

	def render(self, world_renderer: WorldRenderer, pos: TilePos, tile_stack, height: int):
		if not height:
			world_renderer.render_texture(texture.WaterNoUnderTexture, pos.get_pixel_pos())
		world_renderer.render_texture(self.TEXTURE, pos.get_pixel_pos())

	def can_walk(self, player):
		return player.player_state == PlayerState.BOAT_IDLE


class TreeTile(Tile):
	TEXTURE = texture.TreeTexture
	CAN_WALK = 0


class BushTile(TreeTile):
	TEXTURE = texture.BushTexture


class SandTile(GroundTile):
	TEXTURE = texture.SandTexture


class BlackSandTile(GroundTile):
	TEXTURE = texture.BlackSandTexture


class GravelTile(GroundTile):
	TEXTURE = texture.GravelTexture


class PathTile(GroundTile):
	TEXTURE = texture.PathTexture


class FlowersTile(Tile):
	TEXTURE = texture.FlowersTexture
