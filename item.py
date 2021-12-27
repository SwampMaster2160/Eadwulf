import texture
from gui_renderer import GUIRenderer, GUITextureAlign
from pixel_pos import PixelPos
from tile_stack import TileStack


class Item:
	TEXTURE = texture.ErrorTexture

	def render(self, gui_renderer: GUIRenderer, pos: PixelPos):
		gui_renderer.render_texture(self.TEXTURE, pos, GUITextureAlign.TOP_LEFT)

	def use(self, use_on: TileStack):
		pass


class NullItem(Item):
	def render(self, gui_renderer: GUIRenderer, pos: PixelPos):
		pass


class ToolItem(Item):
	def use(self, use_on: TileStack):
		if use_on.tiles:
			use_on.tiles.pop()


class ShovelItem(ToolItem):
	TEXTURE = texture.ShovelTexture


class HammerItem(ToolItem):
	TEXTURE = texture.HammerTexture
