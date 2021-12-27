from gui_renderer import GUIRenderer
from pixel_pos import PixelPos


class GUIElement:
	def render(self, gui_renderer: GUIRenderer):
		pass


class RectGUIElement:
	pos: PixelPos
	size: PixelPos
	color: any

	def render(self, gui_renderer: GUIRenderer):
		pass
