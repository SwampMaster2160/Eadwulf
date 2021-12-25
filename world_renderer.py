from pygame.surface import Surface


class WorldRenderer:
	surface: Surface
	texture_dict: dict
	world_origin: tuple
	world_surface_width_in_tiles: int
	
	def render_texture(self, texture, pos: tuple[int, int]):
		self.surface.blit(self.texture_dict[texture], (self.world_origin[0] + pos[0], self.world_origin[1] + pos[1]))
