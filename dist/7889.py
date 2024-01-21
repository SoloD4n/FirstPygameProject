import pygame
from pygame.locals import *
import random

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
screen_width = 800
screen_height = 600

# Определение цветов
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Создание экрана
screen = pygame.display.set_mode((screen_width, screen_height))

# Загрузка изображения флага России
russian_flag = pygame.image.load("map_rus.png")
russian_flag_rect = russian_flag.get_rect()
russian_flag_rect.center = (screen_width // 2, screen_height // 2)

# Загрузка изображения флага США
usa_flag = pygame.image.load("map_usa.png")
usa_flag_rect = usa_flag.get_rect()
usa_flag_rect.center = (screen_width // 2 + 200, screen_height // 2)

# Определение списка европейских стран
european_countries = ['Germany', 'France', 'Spain', 'Italy', 'United Kingdom', 'Netherlands', 'Belgium', 'Switzerland']

# Начальные значения переменных
treasury = 1000000
diplomacy = {'China': 'Friendly', 'France': 'War', 'Spain': 'War', 'Italy': 'War', 'United Kingdom': 'War', 'Netherlands': 'Neutral', 'Belgium': 'Neutral', 'Switzerland': 'Neutral'}
bombs = []

# Функция для обработки движения бомбы
def move_bombs():
    for bomb in bombs:
        bomb[0] += 5  # Инкрементируем позицию по оси X
        if bomb[0] > screen_width:
            bombs.remove(bomb)  # Удаляем бомбу, если она вышла за пределы экрана

# Основной игровой цикл
running = True
while running:
    # Отображение флагов и состояния дипломатических отношений
    screen.fill(black)
    screen.blit(russian_flag, russian_flag_rect)
    screen.blit(usa_flag, usa_flag_rect)
    
    diplomacy_text = pygame.font.SysFont(None, 24).render("Diplomacy:", True, white)
    screen.blit(diplomacy_text, (50, 50))
    
    y = 80
    for country, status in diplomacy.items():
        diplomacy_line = pygame.font.SysFont(None, 18).render(f"{country}: {status}", True, white)
        screen.blit(diplomacy_line, (50, y))
        y += 30
    
    # Отображение казны
    treasury_text = pygame.font.SysFont(None, 24).render(f"Treasury: {treasury}", True, white)
    screen.blit(treasury_text, (screen_width - 200, 50))
    
    # Отображение бомб
    for bomb in bombs:
        pygame.draw.circle(screen, red, (bomb[0], bomb[1]), 10)
    
    # Обработка событий клавиатуры и мыши
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                # Выпуск бомбы
                bomb_x = russian_flag_rect.x + russian_flag_rect.width
                bomb_y = russian_flag_rect.y + russian_flag_rect.height // 2
                bombs.append([bomb_x, bomb_y])
                
                # Уменьшение суммы в казне
                treasury -= 10000
        
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                # Заключение торгового договора
                mouse_pos = pygame.mouse.get_pos()
                if usa_flag_rect.collidepoint(mouse_pos):
                    if treasury >= 100000:
                        treasury -= 100000
                        diplomacy['USA'] = 'Ally'
                    else:
                        print("Недостаточно средств для заключения договора!")
                
                if european_countries.collidepoint(mouse_pos):
                    selected_countries = [country for country, rect in european_countries.items() if rect.collidepoint(mouse_pos)]
                    for country in selected_countries:
                        diplomacy[country] = 'Neutral'

    move_bombs()  # Обработка движения бомб

    pygame.display.update()

# Завершение Pygame
pygame.quit()