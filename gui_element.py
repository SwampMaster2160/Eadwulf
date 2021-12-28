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

	def __init__(
			self,
			pos: PixelPos = PixelPos(64, 28),
			size: PixelPos = PixelPos(128, 200),
			color=(31, 31, 31),
			align: GUITextureAlign = GUITextureAlign.CENTRE_CENTRE
	):
		self.pos = pos
		self.size = size
		self.color = color
		self.align = align

	def render(self, gui_renderer: GUIRenderer):
		gui_renderer.render_rect(self.color, self.pos, self.size, self.align)


class ButtonGUIElement(GUIElement):
	TEXT = "Button"
	pos: PixelPos
	size: PixelPos
	align: GUITextureAlign

	def __init__(
			self,
			pos: PixelPos = PixelPos(64, 28),
			size: PixelPos = PixelPos(128, 16),
			align: GUITextureAlign = GUITextureAlign.CENTRE_CENTRE,
			auto_place_y: int = 0
	):
		self.pos = pos + PixelPos(0, auto_place_y * 20)
		self.size = size
		self.align = align

	def is_mouse_over(self, mouse: MouseState) -> bool:
		mouse_pos = mouse.pos_on_gui_surfaces[self.align]
		return self.pos.x < mouse_pos.x < self.pos.x + self.size.x and\
			self.pos.y < mouse_pos.y < self.pos.y + self.size.y

	def click(self, world: World):
		print("Click")
		return GameState.INGAME, self

	def render(self, gui_renderer: GUIRenderer):
		color = (223, 223, 223)
		match self.hover_state:
			case MouseOverState.HOVER_OVER:
				color = (127, 255, 127)
			case MouseOverState.CLICKING:
				color = (63, 255, 63)
		gui_renderer.render_rect(color, self.pos, self.size, self.align)
		gui_renderer.render_string(
			self.TEXT, 1, self.pos + PixelPos(self.size.x // 2, self.size.y // 2), GUITextureAlign.CENTRE_CENTRE
		)
