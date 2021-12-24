from common_data import CommonData

import pygame as pg

from player import PlayerState, CardinalDirection


def tick(common_data: CommonData):
	keys_pressed = pg.key.get_pressed()
	
	# Player
	match common_data.player.player_state:
		case PlayerState.IDLE:
			is_w_pressed = keys_pressed[pg.K_w]
			is_a_pressed = keys_pressed[pg.K_a]
			is_s_pressed = keys_pressed[pg.K_s]
			is_d_pressed = keys_pressed[pg.K_d]
			if is_w_pressed or is_a_pressed or is_s_pressed or is_d_pressed:
				common_data.player.player_state = PlayerState.WALKING
				common_data.player.offset = 1
			if is_w_pressed:
				common_data.player.facing = CardinalDirection.NORTH
			elif is_a_pressed:
				common_data.player.facing = CardinalDirection.WEST
			elif is_s_pressed:
				common_data.player.facing = CardinalDirection.SOUTH
			elif is_d_pressed:
				common_data.player.facing = CardinalDirection.EAST
		case PlayerState.WALKING:
			common_data.player.offset += 1
			if common_data.player.offset > 15:
				common_data.player.player_state = PlayerState.IDLE
				common_data.player.offset = 0
				match common_data.player.facing:
					case CardinalDirection.NORTH:
						common_data.player.y -= 1
					case CardinalDirection.EAST:
						common_data.player.x += 1
					case CardinalDirection.SOUTH:
						common_data.player.y += 1
					case CardinalDirection.WEST:
						common_data.player.x -= 1
