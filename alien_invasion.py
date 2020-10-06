
# sys -> Sai do game quando o usuario desistir
import sys

import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf

def run_game():
	
	# Inicializa o jogo e cria um objeto para a tela
	pygame.init()
	
	# pega as o que tiver na classe Settings
	ai_settings = Settings()
	
	# Adicionamos largura e altura
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
		
	pygame.display.set_caption('Alien Invasion')
	
	
	# Cria o botão play
	play_button = Button(ai_settings, screen, 'Play')
	
	
	# Cria uma instancia para armazenar estatisticas do jogo e cria painel de pontuação
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	# Cria uma espaçonave, um grupo de projeteis e um grupo de alienigena
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	
	
	# Cria a frota de alienigenas
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	
	# Inicia o laço principal do jogo
	while True:	
		'''Chama os eventos em game_functions'''
		
		# verifica a entrada do jogador
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
			aliens, bullets)
		
		if stats.game_active:
			# atualiza a posição da nave
			ship.update()
			# e de qualquer projetil que tenha aparecido
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
			# atualiza a posição do alien
			gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
			
		# Desenhamos uma nova tela
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
			play_button)
		
		
		
run_game()

