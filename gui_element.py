from gui_renderer import GUIRenderer, GUITextureAlign
from pixel_pos import PixelPos


class GUIElement:
	def render(self, gui_renderer: GUIRenderer):
		pass


class RectGUIElement:
	pos: PixelPos
	size: PixelPos
	color: any
	align: GUITextureAlign

	def __init__(self, pos: PixelPos, size: PixelPos, color, align: GUITextureAlign):
		self.pos = pos
		self.size = size
		self.color = color
		self.align = align

	def render(self, gui_renderer: GUIRenderer):
		gui_renderer.render_rect(self.color, self.pos, self.size, self.align)
