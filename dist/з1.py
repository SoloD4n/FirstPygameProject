import pygame

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
WIDTH = 800
HEIGHT = 600

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра за Россию")

# Загрузка карты
map_image = pygame.image.load("map.png")  # Изображение карты
map_rect = map_image.get_rect()  # Прямоугольник, охватывающий карту

# Переменные для дипломатических отношений
diplomacy_panel = {
    "USA": "Нейтральные",  # Изначально все страны нейтральные
    "China": "Нейтральные",
    "Germany": "Нейтральные"
}

# Координаты и размеры кнопки "T"
button_t_rect = pygame.Rect((10, 10), (50, 50))

# Координаты и размеры страны США
usa_rect = pygame.Rect((300, 200), (100, 100))

# Координаты и размеры кнопки для солдат
button_soldier_rect = pygame.Rect((700, 10), (50, 50))

# Список вражеских войск
enemy_troops = []

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Проверяем, нажата ли кнопка "T"
                if button_t_rect.collidepoint(event.pos):
                    # Заключение торговых соглашений
                    for country, status in diplomacy_panel.items():
                        if country == "USA":
                            diplomacy_panel[country] = "Дружественные"
                        else:
                            diplomacy_panel[country] = "Враждебные"
                # Проверяем, нажата ли кнопка для солдат
                elif button_soldier_rect.collidepoint(event.pos):
                    # Создание вражеских войск
                    enemy_troops.append(pygame.Rect((500, 400), (50, 50)))

    # Отрисовка компонентов игры
    screen.blit(map_image, map_rect)  # Отрисовка карты
    pygame.draw.rect(screen, (0, 0, 255), button_t_rect)  # Отрисовка кнопки "T"
    pygame.draw.rect(screen, (255, 0, 0), usa_rect)  # Отрисовка страны США
    pygame.draw.rect(screen, (0, 255, 0), button_soldier_rect)  # Отрисовка кнопки для солдат
    
    # Отрисовка вражеских войск
    for enemy in enemy_troops:
        pygame.draw.rect(screen, (255, 255, 0), enemy)
    
    pygame.display.flip()  # Обновление экрана

# Завершение Pygame
pygame.quit()