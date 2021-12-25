import texture
from player import Player
from tile_pos import TilePos
from world_renderer import WorldRenderer


class World:
	def render(self, world_renderer: WorldRenderer, player: Player):
		for y in range(player.pos.y - 9, player.pos.y + 10):
			offset = -(world_renderer.world_surface_width_in_tiles // 2) + player.pos.x
			for x in range(offset, world_renderer.world_surface_width_in_tiles + offset):
				pos = TilePos(x, y)
				if x == 0 or y == 0:
					world_renderer.render_texture(texture.Error, pos.get_pixel_pos())
				else:
					world_renderer.render_texture(texture.Grass, pos.get_pixel_pos())
