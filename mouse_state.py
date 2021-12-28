from typing import Tuple, List

from gui_renderer import GUIRenderer
from pixel_pos import PixelPos


class MouseState:
	is_clicked_starting_this_frame: bool = 0
	is_clicked: bool = 0
	pos: Tuple[int, int] = (0, 0)
	pos_on_gui_surfaces: List[PixelPos] = [None] * 9

	def calculate_surface_poses(self, window_size: Tuple[int, int], renderer: GUIRenderer):
		pixel_size = window_size[1] // 256
		for y in range(3):
			y_offset = self.pos[1] // pixel_size
			match y:
				case 1:
					y_offset = (self.pos[1] - (window_size[1] // 2 - pixel_size * 128)) // pixel_size
				case 2:
					y_offset = (self.pos[1] - (window_size[1] - pixel_size * 256)) // pixel_size
			for x in range(3):
				x_offset = self.pos[0] // pixel_size
				match x:
					case 1:
						x_offset = (self.pos[0] - (window_size[0] // 2 - pixel_size * 128)) // pixel_size
					case 2:
						x_offset = (self.pos[0] - (window_size[0] - pixel_size * 256)) // pixel_size
				self.pos_on_gui_surfaces[y * 3 + x] = PixelPos(x_offset, y_offset)
