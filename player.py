from enum import Enum, auto
from typing import Sequence, List

import pygame as pg

import item
import texture
import tile
from gui_renderer import GUIRenderer, GUITextureAlign
from item import Item
from pixel_pos import PixelPos
from tile_pos import TilePos
from world_renderer import WorldRenderer


class PlayerState(Enum):
	IDLE = 0
	WALKING = auto()


class CardinalDirection(Enum):
	NORTH = auto()
	EAST = auto()
	SOUTH = auto()
	WEST = auto()


class Player:
	pos: TilePos = TilePos(0, 0)
	offset: int = 0
	player_state: PlayerState = PlayerState.IDLE
	traveling: CardinalDirection = CardinalDirection.NORTH
	facing: CardinalDirection = CardinalDirection.NORTH

	selected_item: int = 0
	inventory: List[Item] = [item.NullItem()] * 50

	def looking_at_pos(self):
		match self.facing:
			case CardinalDirection.NORTH:
				return self.pos + TilePos(0, -1)
			case CardinalDirection.EAST:
				return self.pos + TilePos(1, 0)
			case CardinalDirection.SOUTH:
				return self.pos + TilePos(0, 1)
			case CardinalDirection.WEST:
				return self.pos + TilePos(-1, 0)

	def traveling_to_pos(self):
		match self.traveling:
			case CardinalDirection.NORTH:
				return self.pos + TilePos(0, -1)
			case CardinalDirection.EAST:
				return self.pos + TilePos(1, 0)
			case CardinalDirection.SOUTH:
				return self.pos + TilePos(0, 1)
			case CardinalDirection.WEST:
				return self.pos + TilePos(-1, 0)

	def __init__(self):
		self.inventory[0] = item.ShovelItem()
		self.inventory[1] = item.HammerItem()
		self.inventory[2] = item.AcornItem()
		self.inventory[3] = item.TileItem(tile.GrassTile())
		self.inventory[4] = item.TileItem(tile.SandTile())
		self.inventory[5] = item.TileItem(tile.BlackSandTile())
		self.inventory[6] = item.TileItem(tile.GravelTile())
		self.inventory[7] = item.TileItem(tile.WaterTile())
		self.inventory[8] = item.TileItem(tile.PathTile())
	
	def tick(self, keys_pressed: Sequence[bool], keys_pressed_this_tick: dict, world):
		if keys_pressed_this_tick[pg.K_LEFT]:
			self.selected_item -= 1
			if self.selected_item % 10 == 9:
				self.selected_item += 10
			if self.selected_item > 49:
				self.selected_item = 9
		if keys_pressed_this_tick[pg.K_RIGHT]:
			self.selected_item += 1
			if self.selected_item % 10 == 0:
				self.selected_item -= 10
			if self.selected_item > 49:
				self.selected_item = 39
		if keys_pressed_this_tick[pg.K_UP]:
			self.selected_item = (self.selected_item - 10) % 50
		if keys_pressed_this_tick[pg.K_DOWN]:
			self.selected_item = (self.selected_item + 10) % 50

		match self.player_state:
			case PlayerState.IDLE:
				if keys_pressed_this_tick[pg.K_RETURN]:
					self.inventory[self.selected_item].use(world[self.looking_at_pos()])
				is_w_pressed = keys_pressed[pg.K_w]
				is_a_pressed = keys_pressed[pg.K_a]
				is_s_pressed = keys_pressed[pg.K_s]
				is_d_pressed = keys_pressed[pg.K_d]
				if is_w_pressed:
					self.traveling = CardinalDirection.NORTH
					if not keys_pressed[pg.K_LCTRL]:
						self.facing = CardinalDirection.NORTH
				elif is_a_pressed:
					self.traveling = CardinalDirection.WEST
					if not keys_pressed[pg.K_LCTRL]:
						self.facing = CardinalDirection.WEST
				elif is_s_pressed:
					self.traveling = CardinalDirection.SOUTH
					if not keys_pressed[pg.K_LCTRL]:
						self.facing = CardinalDirection.SOUTH
				elif is_d_pressed:
					self.traveling = CardinalDirection.EAST
					if not keys_pressed[pg.K_LCTRL]:
						self.facing = CardinalDirection.EAST
				if world[self.traveling_to_pos()].can_walk(self) and\
					(is_w_pressed or is_a_pressed or is_s_pressed or is_d_pressed) and not keys_pressed[pg.K_LSHIFT]:
					self.player_state = PlayerState.WALKING
					self.offset = 1
			case PlayerState.WALKING:
				self.offset += 1
				if self.offset > 15:
					self.player_state = PlayerState.IDLE
					self.offset = 0
					match self.traveling:
						case CardinalDirection.NORTH:
							self.pos.y -= 1
						case CardinalDirection.EAST:
							self.pos.x += 1
						case CardinalDirection.SOUTH:
							self.pos.y += 1
						case CardinalDirection.WEST:
							self.pos.x -= 1
	
	def get_offset_x_and_y(self) -> PixelPos:
		x = 0
		y = 0
		match self.traveling:
			case CardinalDirection.NORTH:
				y = -self.offset
			case CardinalDirection.EAST:
				x = self.offset
			case CardinalDirection.SOUTH:
				y = self.offset
			case CardinalDirection.WEST:
				x = -self.offset
		return PixelPos(x, y)

	def render_gui(self, gui_renderer: GUIRenderer):
		for y in range(5):
			for x in range(10):
				item_index = y * 10 + x
				color = (0, 0, 0, 127)
				if x % 2 != y % 2:
					color = (31, 31, 31, 127)
				render_pos = PixelPos(x * 16, y * 16)
				gui_renderer.render_rect(color, render_pos, PixelPos(16, 16), GUITextureAlign.TOP_LEFT)
				self.inventory[item_index].render(gui_renderer, render_pos)
		gui_renderer.render_texture(
			texture.SelectTexture,
			PixelPos(self.selected_item % 10 * 16, self.selected_item // 10 * 16),
			GUITextureAlign.TOP_LEFT
		)

	def render(self, world_renderer: WorldRenderer):
		player_texture = None
		match self.facing:
			case CardinalDirection.NORTH:
				player_texture = texture.PlayerNorthTexture
			case CardinalDirection.EAST:
				player_texture = texture.PlayerEastTexture
			case CardinalDirection.SOUTH:
				player_texture = texture.PlayerSouthTexture
			case CardinalDirection.WEST:
				player_texture = texture.PlayerWestTexture
		world_renderer.render_texture(player_texture, self.get_offset_x_and_y() + self.pos.get_pixel_pos())
