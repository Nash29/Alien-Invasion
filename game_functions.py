
import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien



def check_keydown_events(event, ai_settings, screen, ship, bullets):
	'''Responde a pressionamentos de tecla'''
	
	if event.key == pygame.K_RIGHT:
		# Move a espaçonave para a direita em 1 pixes
		ship.moving_right = True
			
	elif event.key == pygame.K_LEFT:
		# Move a espaçonave para a esquerda em 1 pixes
		ship.moving_left = True
		
	elif event.key == pygame.K_SPACE:
		# Contem o código usado para disparar um projetil
		fire_bullet(ai_settings, screen, ship, bullets)
		
	elif event.key == pygame.K_q:
		# tecla 'q' encerra o jogo
		sys.exit()
		
		
def fire_bullet(ai_settings, screen, ship, bullets):
	'''Dispara um projetil se o limite ainda não foi alcançado'''
	
	# Cria um novo projetil e o adiciona ao grupo de projeteis
	# se len(bullets) for menor q 3 para de disparar
	if len(bullets) < ai_settings.bullets_allowed: 
			new_bullet = Bullet(ai_settings, screen, ship)
			bullets.add(new_bullet) 


def check_keyup_events(event, ship):
	'''Responde quando não estiver mais precionando a tecla'''
	
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
			
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship,
		aliens, bullets):
	'''Responde a eventos de precionamento de teclas e de mouse.'''
	
	# Observa eventos de teclado e de mouse
	for event in pygame.event.get():
		# QUIT -> sempre que o jogador apertar o botão para sair
		if event.type == pygame.QUIT:
			sys.exit()
			
		# Quando o jogador clica na tecla	
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
				
		
		# Quando o jogador soltar a tecla
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
			
			
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button,
				ship, aliens, bullets, mouse_x, mouse_y)
			

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
		aliens, bullets, mouse_x, mouse_y):
	'''Inicia um novo jogo quando o jogador clicar em Play'''
	
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# Reinicia as configurações do jogo
		ai_settings.initialize_dynamic_settings()
		
		# Oculta o cursor do mouse
		pygame.mouse.set_visible(False)
		
		# Reinicia os dados estatisticos do jogo
		stats.reset_stats()
		stats.game_active = True
		
		# Reinicia as imagens do painel de pontuação
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		# Esvazia a lista de alienigenas e de projeteis
		aliens.empty()
		bullets.empty()
		
		# Cria uma nova frota e centraliza a espaçonave
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	'''Atualiza as imagens na tela e altera para a nova tela'''
	
	# Redesenha a tela a cada passagem pelo laço e adicionamos cor de fundo
	screen.fill(ai_settings.bg_color)
	
	# Redesenha todos os projéteis atrás da espaçonave e dos alienigenas
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	# espaçonave e aliens aparecem sobre bg_color
	ship.blitme()
	aliens.draw(screen)
	
	# Desenha a informação sobre a pontuação
	sb.show_score()
	
	# Desenha o botão Play se o jogo estiver inativo
	if not stats.game_active:
		play_button.draw_button()
				
				
	# Deixa a tela mais recente visivel
	pygame.display.flip()
	
	
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	'''Atualiza a posição dos projeteis e se livra dos projeteis antigos'''
	# Atualiza as posições dos projeteis
	bullets.update()
	
	# Livra-se dos projeteis que desaparecem
	for bullet in bullets.copy():
		# quanto mais a bala sobe mais o valor diminui
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	'''print(len(bullets)) # confere se as balas estão desaparecendo'''
	
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)	
	
		
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	'''Responde a colisão entre projéteis e alienigenas'''
	
	# Remove qualquer projétil e alienigena que tenham colidido
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	
	
	if len(aliens) == 0:
		# Destrói os projeteis existentes, aumenta a velocidade do jogo e cria uma nova frota
		bullets.empty()
		ai_settings.increase_speed()
		
		# Aumenta o nivel
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings, screen, ship, aliens)
		
	
def get_number_aliens_x(ai_settings, alien_width):
	'''Determina o numero do alienigenas que cabem em uma linha'''
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
	
def get_number_rows(ai_settings, ship_height, alien_height):
	'''Determina o numero de linhas com alienigenas que cabem na tela'''
	available_space_y = (ai_settings.screen_height -
							(3 * alien_height) - ship_height)
	
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows


	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	# Cria a primeira linha de alienigenas
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
		
def create_fleet(ai_settings, screen, ship, aliens):
	'''Cria uma frota completa de alienigenas'''
	
	# Cria um alienigena e calcula o numero de alienigenas em uma linha
	# O espaçamento entre os alienigenas é igual a largura de um alienigena
	
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width) 
	number_rows = get_number_rows(ai_settings, ship.rect.height,
		alien.rect.width)
	
	
	# Cria uma frota de alienigenas
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, 
				row_number)
		
		
def check_fleet_edges(ai_settings, aliens):
	'''Responde apropriadamente se algum alienigena alcançou uma borda'''
	
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
			
def change_fleet_direction(ai_settings, aliens):
	'''Faz toda a frota descer e muda a sua direção'''
	
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
	
def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
	'''Responde ao fato de a espaçonave ter sido atingida por um alienigena'''
	
	if stats.ships_left > 0: 
		# Decrementa ships_left
		stats.ships_left -= 1
		
		# Atualiza o painel de ponutações
		sb.prep_ships()
			
		# Esvazia a lista de alienigenas e de projeteis
		aliens.empty()
		bullets.empty()
		
		# Cria uma nova frota e contraliza a espaçonave
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		# Faz uma pausa
		sleep(0.5)
	
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
	'''Verifica se algum alienigena alcançou a parte inferior da tela'''
	
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Trata esser caso do mesmo modo que é feito quando a espaçonave é atingida
			ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
			break

		
def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
	'''
	Verifica se a frota esta em uma das bordas
	  e então atualiza as posições de todos os alienigenas da frota
	'''
	
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	# Verifica se houve colisões entre alienigenas e a espaçonave
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
	
	
	# Verifica se há algum alienigena que atingiu a parte inferior da tela
	check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
	
	
def check_high_score(stats, sb):
	'''Verifica se há uma nova pontuação maxima'''
	
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
	
	
	
	
	
		
