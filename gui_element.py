import gui_menu
from game_state import GameState
from gui_renderer import GUIRenderer, GUITextureAlign
from keyboard import Keyboard
from mouse_over_state import MouseOverState
from mouse import Mouse
from pixel_pos import PixelPos
from world import World


class GUIElement:
	hover_state: MouseOverState = MouseOverState.NOT_OVER

	def tick(self, keyboard: Keyboard):
		pass

	def click(self, world: World, parent_gui_menu):
		return None

	def click_off(self):
		pass

	def is_mouse_over(self, mouse: Mouse) -> bool:
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
			pos: PixelPos = PixelPos(64, 30),
			size: PixelPos = PixelPos(128, 196),
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
	ENABLED = 1
	pos: PixelPos
	size: PixelPos
	align: GUITextureAlign

	def __init__(
			self,
			pos: PixelPos = PixelPos(64, 30),
			size: PixelPos = PixelPos(128, 16),
			align: GUITextureAlign = GUITextureAlign.CENTRE_CENTRE,
			auto_place_y: int = 0
	):
		self.pos = pos + PixelPos(0, auto_place_y * 20)
		self.size = size
		self.align = align

	def is_mouse_over(self, mouse: Mouse) -> bool:
		mouse_pos = mouse.pos_on_gui_surfaces[self.align]
		return self.pos.x < mouse_pos.x < self.pos.x + self.size.x and\
			self.pos.y < mouse_pos.y < self.pos.y + self.size.y

	def click(self, world: World, parent_gui_menu):
		return None

	def render(self, gui_renderer: GUIRenderer):
		color = (223, 223, 223)
		match self.hover_state:
			case MouseOverState.HOVER_OVER:
				color = (127, 255, 127)
			case MouseOverState.CLICKING:
				color = (63, 255, 63)
		if not self.ENABLED:
			color = (63, 63, 63)
		gui_renderer.render_rect(color, self.pos, self.size, self.align)
		gui_renderer.render_string(
			self.TEXT, 1, self.pos + PixelPos(self.size.x // 2, self.size.y // 2), GUITextureAlign.CENTRE_CENTRE
		)


class ResumeButton(ButtonGUIElement):
	TEXT = "Resume"

	def click(self, world: World, parent_gui_menu):
		return GameState.INGAME, self


class ExitGameButton(ButtonGUIElement):
	TEXT = "Exit Game"

	def click(self, world: World, parent_gui_menu):
		if world.do_save_world:
			world.save()
		world.do_save_world = 0
		return GameState.EXITING, self


class ExitToMainMenuButton(ButtonGUIElement):
	TEXT = "Exit to Main Menu"

	def click(self, world: World, parent_gui_menu):
		if world.do_save_world:
			world.save()
		world.do_save_world = 0
		return GameState.IN_MENU, gui_menu.MainMenuGUIMenu(world)


class NewWorldButton(ButtonGUIElement):
	TEXT = "Create New World"

	def click(self, world: World, parent_gui_menu):
		return GameState.IN_MENU, gui_menu.NewWorldGUIMenu(world)


class LoadWorldGUIButton(ButtonGUIElement):
	TEXT = "Load World"

	def click(self, world: World, parent_gui_menu):
		return GameState.IN_MENU, gui_menu.LoadWorldGUIMenu(world)


class LoadWorldFinalizeGUIButton(ButtonGUIElement):
	world_name: str = ""

	def __init__(
			self,
			world_name: str,
			pos: PixelPos = PixelPos(64, 30),
			size: PixelPos = PixelPos(128, 16),
			align: GUITextureAlign = GUITextureAlign.CENTRE_CENTRE,
			auto_place_y: int = 0
	):
		super().__init__(pos, size, align, auto_place_y)
		self.world_name = world_name

	def click(self, world: World, parent_gui_menu):
		world.load(self.world_name)
		return GameState.INGAME, self

	def render(self, gui_renderer: GUIRenderer):
		color = (223, 223, 223)
		match self.hover_state:
			case MouseOverState.HOVER_OVER:
				color = (127, 255, 127)
			case MouseOverState.CLICKING:
				color = (63, 255, 63)
		if not self.ENABLED:
			color = (63, 63, 63)
		gui_renderer.render_rect(color, self.pos, self.size, self.align)
		gui_renderer.render_string(
			self.world_name,
			1,
			self.pos + PixelPos(self.size.x // 2, self.size.y // 2),
			GUITextureAlign.CENTRE_CENTRE
		)


class NewWorldFinalizeButton(ButtonGUIElement):
	TEXT = "Create New World"

	def click(self, world: World, parent_gui_menu):
		if world.new(
				parent_gui_menu.instance_elements[1].text_entered, parent_gui_menu.instance_elements[2].text_entered
		):
			return GameState.INGAME, self
		return None


class BackToMainMenuButton(ButtonGUIElement):
	TEXT = "Back"

	def click(self, world: World, parent_gui_menu):
		return GameState.IN_MENU, gui_menu.MainMenuGUIMenu(world)


class TextGUIElement(GUIElement):
	pos: PixelPos
	text: str
	align: GUITextureAlign
	centred: bool

	def __init__(
			self,
			text: str,
			pos: PixelPos = PixelPos(128, 22),
			align: GUITextureAlign = GUITextureAlign.CENTRE_CENTRE,
			centred: bool = 1
	):
		self.text = text
		self.pos = pos
		self.align = align
		self.centred = centred

	def render(self, gui_renderer: GUIRenderer):
		gui_renderer.render_string(self.text, self.centred, self.pos, self.align)


class TextEntryGUIElement(GUIElement):
	pos: PixelPos
	size: PixelPos
	align: GUITextureAlign
	info_text: str
	text_entered: str = ""
	selected = 0

	def __init__(
			self,
			info_text: str,
			pos: PixelPos = PixelPos(64, 30),
			size: PixelPos = PixelPos(128, 16),
			align: GUITextureAlign = GUITextureAlign.CENTRE_CENTRE,
			auto_place_y: int = 0
	):
		self.pos = pos + PixelPos(0, auto_place_y * 20)
		self.size = size
		self.align = align
		self.info_text = info_text

	def is_mouse_over(self, mouse: Mouse) -> bool:
		mouse_pos = mouse.pos_on_gui_surfaces[self.align]
		return self.pos.x < mouse_pos.x < self.pos.x + self.size.x and\
			self.pos.y < mouse_pos.y < self.pos.y + self.size.y

	def click(self, world: World, parent_gui_menu):
		self.selected = 1

	def click_off(self):
		self.selected = 0

	def render(self, gui_renderer: GUIRenderer):
		gui_renderer.render_rect((223, 223, 223), self.pos, self.size, self.align)
		width = gui_renderer.render_string(
			self.info_text, 0, self.pos + PixelPos(1, self.size.y // 2), self.align
		) + 1
		color = (255, 255, 255)
		if self.selected:
			color = (63, 255, 63)
		elif self.hover_state == MouseOverState.HOVER_OVER:
			color = (127, 255, 127)
		gui_renderer.render_rect(
			color, self.pos + PixelPos(width, 0), self.size + PixelPos(-width, 0), self.align
		)
		gui_renderer.render_string(
			self.text_entered, 0, self.pos + PixelPos(width + 1, self.size.y // 2), self.align
		)

	def tick(self, keyboard: Keyboard):
		if self.selected:
			for char in keyboard.new_text:
				if self.text_entered and ord(char) == 8:
					self.text_entered = self.text_entered[:-1]
				else:
					self.text_entered += char
