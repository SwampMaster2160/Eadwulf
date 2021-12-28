from typing import Sequence


class Keyboard:
	keys_pressed: Sequence[bool]
	keys_pressed_starting_now: dict
	new_text: str

	def __init__(self, keys_pressed, keys_pressed_starting_now, new_text: str):
		self.keys_pressed = keys_pressed
		self.keys_pressed_starting_now = keys_pressed_starting_now
		self.new_text = new_text
