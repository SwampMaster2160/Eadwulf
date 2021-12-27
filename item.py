from copy import copy

import texture
import tile
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


class AcornItem(Item):
	TEXTURE = texture.AcornTexture

	def use(self, use_on: TileStack):
		if use_on.tiles and isinstance(use_on.tiles[-1], tile.GrassTile):
			use_on.tiles.append(tile.TreeTile())


class TileItem(Item):
	child: tile.Tile

	def __init__(self, child: tile.Tile):
		self.child = child

	def render(self, gui_renderer: GUIRenderer, pos: PixelPos):
		gui_renderer.render_texture(self.child.TEXTURE, pos, GUITextureAlign.TOP_LEFT)

	def use(self, use_on: TileStack):
		if not use_on.tiles:
			use_on.tiles.append(copy(self.child))
