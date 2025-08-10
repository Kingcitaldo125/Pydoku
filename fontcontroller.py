import pygame

class FontController(object):
	font_instance = None

	def __init__(self):
		pass

	@classmethod
	def quit(cls):
		if cls.font_instance:
			pygame.font.quit()

	@classmethod
	def get_instance(cls):
		if not cls.font_instance:
			pygame.font.init()
			cls.font_instance = pygame.font.Font('freesansbold.ttf', 50)
		return cls.font_instance
