import pygame
import random
import pygame_gui

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FONT_SIZE = 24
RUSSIA_COLOR = (255, 0, 0)
USA_COLOR = (0, 0, 255)
TREATY_COST = 100
SOLDIER_COST = 500
STATE_ATTACK = "attack"
STATE_DEFEND = "defend"

imagePutin = pygame.image.load('putin.png')

# Получение прямоугольника картинки
image_rect = imagePutin.get_rect()

# Установка позиции картинки в левом верхнем углу экрана
image_rect.topleft = (0, 0)


#Музычка
sound = pygame.mixer.Sound('sound.mp3')
sound.play()

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Russia vs USA")

# Загрузка карты
map_image = pygame.image.load("map.png")
explosion_image = pygame.image.load("explosion.png")

# Загрузка шрифта
font = pygame.font.Font(None, FONT_SIZE)

# Кнопки выбора сложности
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

diff_easy = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((60, 280), (200, 100)),
    text="Легкая",
    manager=manager
)
diff_medium = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((290, 280), (200, 100)),
    text="Средняя",
    manager=manager
)
diff_hard = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((520, 280), (200, 100)),
    text="Сложная",
    manager=manager,
)
chosen = False
clock = pygame.time.Clock()

# Переменные состояния игры
treasury = 0
diplomacy_level = 5
soldiers = []
enemy_soldiers = []
game_state = STATE_ATTACK
attacking_soldiers = []
defending_soldiers = []
attacking_soldier_count = 0
defending_soldier_count = 0
russia_soldier_count = 0
usa_soldier_count = 0
screen.blit(imagePutin, image_rect)

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Загружаем изображение бомбы
        self.image = pygame.image.load("bomb.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y += 5  # Скорость падения бомбы

bomb_group = pygame.sprite.Group()

# Функция для отображения текста на экране
def draw_text(text, x, y, color):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Главный цикл игры
running = True
while running:
    font = pygame.font.Font(None, 50)
    if not chosen:
        diff_text = font.render("Выберите сложность", True, (255, 0, 0))
        screen.blit(diff_text, (220, 220))
    # Обработка событий
    time_delta = clock.tick(60) / 1000.0
        # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_t:
                # Заключение соглашения
                if treasury >= TREATY_COST:
                    treasury -= TREATY_COST
                    diplomacy_level += 1
            elif event.key == pygame.K_SPACE:
            # Высадка солдата
                if treasury >= SOLDIER_COST:
                    treasury -= SOLDIER_COST
                    x = random.randint(0, SCREEN_WIDTH)
                    y = random.randint(0, SCREEN_HEIGHT)
                    soldiers.append((x, y))
            elif event.key == pygame.K_a:
                # Переключение на режим атаки
                game_state = STATE_ATTACK
                attacking_soldier_count = len(soldiers)
                defending_soldier_count = len(enemy_soldiers)
            elif event.key == pygame.K_d:
                # Переключение на режим защиты
                game_state = STATE_DEFEND
                attacking_soldier_count = len(enemy_soldiers)
                defending_soldier_count = len(soldiers)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Создаем новую бомбу и добавляем в группу спрайтов
                bomb = Bomb(mouse_x, mouse_y)
                bomb_group.add(bomb)
            if event.key == pygame.K_y:  # Проверяем нажатие кнопки "Y"
                # Создаем новую бомбу в случайной позиции по оси X
                bomb = Bomb(random.randrange(SCREEN_WIDTH), 0)
                bomb_group.add(bomb)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == STATE_ATTACK:
                # Атака вражеского солдата
                x, y = event.pos
                for enemy_soldier in enemy_soldiers:
                    if abs(enemy_soldier[0] - x) < 10 and abs(enemy_soldier[1] - y) < 10:
                        enemy_soldiers.remove(enemy_soldier)
                        break
            elif game_state == STATE_DEFEND:
                # Защита своего солдата
                x, y = event.pos
                for soldier in soldiers:
                    if abs(soldier[0] - x) < 10 and abs(soldier[1] - y) < 10:
                        soldiers.remove(soldier)
                        break
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Создаем новую бомбу и добавляем в группу спрайтов
            bomb = Bomb(mouse_x, mouse_y)
            bomb_group.add(bomb)

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Проверяем нажатие кнопки мыши
            # Получение позиции клика мыши
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Рисуем изображение взрыва на позиции клика мыши
            screen.blit(explosion_image, (mouse_x, mouse_y))

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Проверяем нажатие левой кнопки мыши
            # Получаем текущие координаты мыши
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Создаем новую бомбу и добавляем в группу спрайтов
            bomb = Bomb(mouse_x, mouse_y)
            bomb_group.add(bomb)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == diff_easy:
                    treasury = 10000
                    chosen = True
                if event.ui_element == diff_medium:
                    treasury = 5000
                    chosen = True
                if event.ui_element == diff_hard:
                    treasury = 1000
                    chosen = True

        manager.process_events(event)
    manager.update(time_delta)
    if not chosen:
        manager.draw_ui(screen)
    # Обновление игры
    pygame.display.flip()
    enemy_soldiers.clear()
    attacking_soldiers.clear()
    defending_soldiers.clear()
    russia_soldier_count = len(soldiers)
    usa_soldier_count = len(enemy_soldiers)
    bomb_group.update()
    bomb_group.draw(screen)

    if game_state == STATE_ATTACK:
        # Высадка войск противника
        for i in range(diplomacy_level):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            enemy_soldiers.append((x, y))
    elif game_state == STATE_DEFEND:
        # Высадка своих войск
        for i in range(diplomacy_level):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            soldiers.append((x, y))

    # Проверка условий победы
    if usa_soldier_count == 0:
        draw_text("Russia Wins!", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, RUSSIA_COLOR)
    elif russia_soldier_count == 0:
        draw_text("USA Wins!", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, USA_COLOR)

    # Отрисовка игры
    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, RUSSIA_COLOR, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50)
    treasury_text = font.render(f"Казна: {treasury}", True, RUSSIA_COLOR)
    diplomacy_text = font.render(f"Дипломатический уровень: {diplomacy_level}", True, RUSSIA_COLOR)
    screen.blit(treasury_text, (10, 10))
    screen.blit(diplomacy_text, (10, 40))

    for soldier in soldiers:
        pygame.draw.circle(screen, USA_COLOR, soldier, 10)

    # Отрисовка карты
    screen.blit(map_image, (0, 0))
    # Отрисовка солдат
    for soldier in soldiers:
        pygame.draw.circle(screen, RUSSIA_COLOR, (soldier[0], soldier[1]), 5)
    for enemy_soldier in enemy_soldiers:
        pygame.draw.circle(screen, USA_COLOR, (enemy_soldier[0], enemy_soldier[1]), 5)
    # Отображение текста
    draw_text("Treasury: {}".format(treasury), 10, 10, (255, 255, 255))
    draw_text("Russia's Soldiers: {}".format(russia_soldier_count), 10, 40, RUSSIA_COLOR)
    draw_text("USA's Soldiers: {}".format(usa_soldier_count), 10, 70, USA_COLOR)
    draw_text("Press 'A' for Attack mode, 'D' for Defend mode", 10, SCREEN_HEIGHT - 30, (255, 255, 255))


    pygame.time.Clock().tick(FPS)