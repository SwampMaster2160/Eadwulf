import texture
from player import Player
from world_renderer import WorldRenderer


class World:
	def render(self, world_renderer: WorldRenderer, player: Player):
		for y in range(player.y - 9, player.y + 10):
			offset = -(world_renderer.world_surface_width_in_tiles // 2) + player.x
			for x in range(offset, world_renderer.world_surface_width_in_tiles + offset):
				if x == 0 or y == 0:
					world_renderer.render_texture(texture.Error, (x * 16, y * 16))
				else:
					world_renderer.render_texture(texture.Grass, (x * 16, y * 16))
