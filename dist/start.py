import pygame
import random

# Инициализация pygame и создание окна игры
pygame.init()
enemy_soldiers = []
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Игра: Россия против США")

# Загрузка изображений
russia_image = pygame.image.load("russia.jpg")
usa_image = pygame.image.load("map_usa.jpg")
soldier_image = pygame.image.load("soldier.png")

def check_collision(soldier_x, soldier_y, enemy_soldiers):
    for enemy_soldier in enemy_soldiers:
        if abs(soldier_x - enemy_soldier[0]) < 10 and abs(soldier_y - enemy_soldier[1]) < 10:
            return True
    return False

def battle(russian_soldiers, enemy_soldiers):
    for russian_soldier in russian_soldiers:
        if check_collision(russian_soldier[0], russian_soldier[1], enemy_soldiers):
            # Российский солдат погибает
            russian_soldiers.remove(russian_soldier)
    for enemy_soldier in enemy_soldiers:
        if check_collision(enemy_soldier[0], enemy_soldier[1], russian_soldiers):
            # Вражеский солдат погибает
            enemy_soldiers.remove(enemy_soldier)

def check_trade_status(country):
    trade_status = diplomatic_relations[country]
    return trade_status



# Инициализация переменных
russia_x, russia_y = 50, 50
money = 1000
soldiers = []
diplomatic_relations = {
    "Germany": "Neutral",
    "China": "Neutral",
    "India": "Neutral"
}

# Главный игровой цикл
running = True
while running:
    # Управление событиями
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                # Заключение торгового соглашения
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Высадка солдатов на территорию США
            mouse_x, mouse_y = event.pos
            if usa_image.get_rect().collidepoint(mouse_x, mouse_y):
                if money >= 100:
                    soldiers.append((mouse_x, mouse_y))
                    money -= 100
    
    # Перемещение России по экрану
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        russia_x -= 5
    elif keys[pygame.K_RIGHT]:
        russia_x += 5
    elif keys[pygame.K_UP]:
        russia_y -= 5
    elif keys[pygame.K_DOWN]:
        russia_y += 5
    
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_t:
            # Заключение торгового соглашения
            selected_country = "Germany"  # Здесь нужно выбрать страну
            trade_status = check_trade_status(selected_country)
            if trade_status == "Neutral":
                diplomatic_relations[selected_country] = "Trade Agreement"
                # Добавьте здесь код для обновления интерфейса и проверки эффектов торгового соглашения
            elif trade_status == "Trade Agreement":
                diplomatic_relations[selected_country] = "Neutral"
                # Добавьте здесь код для обновления интерфейса и проверки эффектов отмены торгового соглашения
    
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            # Высадка войск на территорию России
            enemy_soldier_x = random.randint(0, screen_width)
            enemy_soldier_y = random.randint(0, screen_height)
            enemy_soldiers.append((enemy_soldier_x, enemy_soldier_y))
    


    # Отрисовка экрана
    screen.fill((255, 255, 255))
    screen.blit(russia_image, (russia_x, russia_y))
    screen.blit(usa_image, (600, 200))
    screen.blit(soldier_image, (50, 70))
    
    # Отрисовка солдат
    for soldier in soldiers:
        screen.blit(soldier_image, soldier)
    
    # Отрисовка информации
    font = pygame.font.Font(None, 24)
    text = font.render(f"Казна: {money}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    diplomatic_text = font.render("Дипломатические отношения:", True, (0, 0, 0))
    screen.blit(diplomatic_text, (10, 40))
    i = 1
    for country, status in diplomatic_relations.items():
        diplomatic_status = font.render(f"{country}: {status}", True, (0, 0, 0))
        screen.blit(diplomatic_status, (10, 40 + i * 30))
        i += 1
    battle(soldiers, enemy_soldiers)
    pygame.display.flip()

# Завершение игры
pygame.quit()