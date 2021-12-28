from typing import Tuple


class MouseState:
	is_clicked_starting_this_frame: bool = 0
	is_clicked: bool = 0
	pos: Tuple[int, int] = (0, 0)
