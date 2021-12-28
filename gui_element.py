from game_state import GameState
from gui_renderer import GUIRenderer, GUITextureAlign
from mouse_over_state import MouseOverState
from mouse_state import MouseState
from pixel_pos import PixelPos
from world import World


class GUIElement:
	hover_state: MouseOverState = MouseOverState.NOT_OVER

	def click(self, world: World):
		return None

	def is_mouse_over(self, mouse: MouseState) -> bool:
		return 0

	def render(self, gui_renderer: GUIRenderer):
		pass


class RectGUIElement(GUIElement):
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


class ButtonGUIElement(GUIElement):
	pos: PixelPos
	size: PixelPos
	align: GUITextureAlign

	def __init__(self, pos: PixelPos, size: PixelPos, align: GUITextureAlign):
		self.pos = pos
		self.size = size
		self.align = align

	def is_mouse_over(self, mouse: MouseState) -> bool:
		return 100 < mouse.pos[0] < 200 and 100 < mouse.pos[1] < 200

	def click(self, world: World):
		print("Click")
		return GameState.INGAME, self

	def render(self, gui_renderer: GUIRenderer):
		color = (63, 63, 63)
		match self.hover_state:
			case MouseOverState.HOVER_OVER:
				color = (63, 63, 127)
			case MouseOverState.CLICKING:
				color = (63, 63, 255)
		gui_renderer.render_rect(color, self.pos, self.size, self.align)
