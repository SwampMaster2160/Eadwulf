import os
import pickle

import world
from chunk import Chunk
from keyboard import Keyboard
from player import Player
from tile_pos import TilePos
from tile_stack import TileStack
from world_renderer import WorldRenderer


class World:
	name: str = ""
	filepath: str = ""
	player: Player = Player()
	chunks: dict = {}
	do_save_world: bool = 0

	def tick(self, keyboard: Keyboard):
		self.player.tick(keyboard, self)

	def render(self, world_renderer: WorldRenderer):
		for y in range(self.player.pos.y - 9, self.player.pos.y + 10):
			offset = -(world_renderer.world_surface_width_in_tiles // 2) + self.player.pos.x
			for x in range(offset, world_renderer.world_surface_width_in_tiles + offset):
				pos = TilePos(x, y)
				self[pos].render(world_renderer, pos)
		self.player.render(world_renderer)

	def __getitem__(self, item: TilePos) -> TileStack:
		chunk_pos = item.get_chunk_pos().get_tuple()
		if chunk_pos not in self.chunks:
			self.chunks[chunk_pos] = Chunk(item.get_chunk_pos())
			return self.chunks[chunk_pos][item.get_chunk_offset()]
		return self.chunks[chunk_pos][item.get_chunk_offset()]

	def load(self, path: str):
		self.filepath = path
		self.chunks = {}
		self.player = Player()
		self.do_save_world = 1
		main_dir = os.path.split(os.path.abspath(__file__))[0]
		world_path = os.path.join(main_dir, "playerdata", "world", path, "chunks")
		for chunk_name in os.listdir(os.path.join(world_path)):
			chunk_path = os.path.join(world_path, chunk_name)
			file = open(chunk_path, "rb")
			poses = chunk_name.split("_")
			pos = (int(poses[0]), int(poses[1].split(".")[0]))
			self.chunks[pos] = pickle.load(file)
			file.close()

	def save(self):
		main_dir = os.path.split(os.path.abspath(__file__))[0]
		world_path = os.path.join(main_dir, "playerdata", "world", self.filepath, "chunks")
		os.makedirs(world_path, exist_ok=1)
		for pos, chunk in self.chunks.items():
			filename = f"{pos[0]}_{pos[1]}.ech"
			file = open(os.path.join(world_path, filename), "wb")
			pickle.dump(chunk, file)
			file.close()
