from pygame.surface import Surface


class CommonData:
	def __init__(self):
		self.texture_dict = {}
	
	texture_dict: dict
	screen: Surface
	window_size: tuple
