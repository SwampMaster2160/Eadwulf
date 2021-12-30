import threading


class SimpleThread(threading.Thread):
	out: any = None
	func: any
	params: tuple

	def __init__(self, func, params: tuple):
		super().__init__()
		self.func = func
		self.params = params

	def run(self) -> None:
		out = self.func(*self.params)
