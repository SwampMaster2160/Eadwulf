import os
import pathlib
import pickle

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

	def new(self, filename: str):
		if len(filename) < 1:
			return 0
		if "/" in filename or "\\" in filename:
			return 0
		try:
			world_path = os.path.join(pathlib.Path.home(), "eadwulf", "world", filename, "chunks")
			os.makedirs(world_path)
		except OSError:
			return 0
		self.name = filename
		self.filepath = filename
		self.chunks = {}
		self.do_save_world = 1
		self.player = Player()
		return 1

	def load(self, path: str):
		self.filepath = path
		self.chunks = {}
		self.player = Player()
		self.do_save_world = 1
		world_path = os.path.join(pathlib.Path.home(), "eadwulf", "world", path, "chunks")
		for chunk_name in os.listdir(os.path.join(world_path)):
			chunk_path = os.path.join(world_path, chunk_name)
			file = open(chunk_path, "rb")
			poses = chunk_name.split("_")
			pos = (int(poses[0]), int(poses[1].split(".")[0]))
			self.chunks[pos] = pickle.load(file)
			file.close()

	def save(self):
		world_path = os.path.join(pathlib.Path.home(), "eadwulf", "world", self.filepath, "chunks")
		os.makedirs(world_path, exist_ok=1)
		for pos, chunk in self.chunks.items():
			filename = f"{pos[0]}_{pos[1]}.ech"
			file = open(os.path.join(world_path, filename), "wb")
			pickle.dump(chunk, file)
			file.close()
