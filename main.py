import pygame
import random
import time

body = []
body2 = []


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((HEIGHT, 44))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Eat (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = (random.randint(1, 20) * 22)
        self.rect.y = (random.randint(2, 20) * 22)
        self.count = 0

    def new_eat(self):
        self.count += 1
        self.rect.x = (random.randint(1, 20) * 22)
        self.rect.y = (random.randint(2, 20) * 22)


class Head(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(HEAD_GREEN)
        self.rect = self.image.get_rect()
        self.direction = "right"
        self.rect.center = (120, 120)
        self.last_x = 0
        self.last_y = 0

    def update(self):
        self.last_x = self.rect.x
        self.last_y = self.rect.y

        if self.rect.x == eat.rect.x and self.rect.y == eat.rect.y:
            eat.new_eat()
            body.append(Body(len(body)))

        self.direction = direction
        if self.direction == "right":
            self.rect.x += 22
        elif self.direction == 'left':
            self.rect.x -= 22
        elif self.direction == 'up':
            self.rect.y -= 22
        elif self.direction == 'down':
            self.rect.y += 22

        if self.rect.x > WIDTH:
            self.rect.x = 0

        if self.rect.x < 0:
            self.rect.x = WIDTH + 2

        if self.rect.y > HEIGHT:
            self.rect.y = 44

        if self.rect.y < 44:
            self.rect.y = HEIGHT + 2



        # for i in range(len(body)):
        #     if self.rect.x == body[i].rect.x and self.rect.y == body[i].rect.y:
        #         pygame.quit()


class Body(pygame.sprite.Sprite):
    def __init__(self, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        self.rect.x = head.rect.x
        self.rect.y = head.rect.y
        self.last_x = 0
        self.last_y = 0

        self.id = id
        all_sprites.add(self)
        body2.append(self)

    def update(self):
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.rect.x = body[self.id - 1].last_x
        self.rect.y = body[self.id - 1].last_y


WIDTH = 482
HEIGHT = 482 + 44
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
HEAD_GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (40, 40, 40)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

width = height = 20
x = y = 0
screen.fill(GREY)

all_sprites = pygame.sprite.Group()
menu = Menu()
head = Head()
eat = Eat()
all_sprites.add(head)
all_sprites.add(eat)
all_sprites.add(menu)
body.append(head)

y = 44
for col in range(22):
    for string in range(22):
        pygame.draw.rect(screen, BLACK, (x, y, width, height))
        x += 22
    y += 22
    x = 0

f1 = pygame.font.SysFont('arial', 36)
pause_text = f1.render("Pause", True, WHITE)

direction = 'None'
time_sleep = 0.1
flag_for_pause = False


running = True
while running:
    if flag_for_pause:
        screen.blit(pause_text, (190, 5))
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                flag_for_pause = not flag_for_pause

            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    else:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                if direction == "down":
                    pass
                else:
                    direction = "up"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                if direction == "left":
                    pass
                else:
                    direction = "right"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                if direction == "right":
                    pass
                else:
                    direction = "left"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                if direction == "up":
                    pass
                else:
                    direction = "down"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                flag_for_pause = not flag_for_pause

            if event.type == pygame.QUIT:
                running = False

        if eat.count == 20:
            time_sleep = 0.0
        else:
            time_sleep = 0.1

        pygame.draw.rect(screen, BLACK, (body[-1].rect.x, body[-1].rect.y, width, height))
        print(head.rect.x, head.direction)

        all_sprites.update()
        all_sprites.draw(screen)

        count_apples = f1.render(str(eat.count), True, WHITE)
        screen.blit(count_apples, (5, 5))

        new_eat_trecer = pygame.sprite.spritecollide(eat, body2, False)

        if new_eat_trecer:
            eat.rect.x = (random.randint(1, 20) * 22)
            eat.rect.y = (random.randint(1, 20) * 22)

        hits = pygame.sprite.spritecollide(head, body2, False)

        if hits:
            running = False

        pygame.display.flip()
        time.sleep(time_sleep)

pygame.quit()