
class GameStats():
	'''Armazena dados estatisticos da Invasão Alienigena'''
	
	def __init__(self, ai_settings):
		'''Inicializa os dados estatisticos'''
		
		self.ai_settings = ai_settings
		self.reset_stats()
		
		# Inicia a Invasão Alienigena em um estado inativo
		self.game_active = False
		
		# Pontuação maxima jamais devera ser reiniciada
		self.high_score = 0
		
		
	def reset_stats(self):
		'''Inicializa os dados estatisticos que podem mudar durante o jogo'''
		
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1

