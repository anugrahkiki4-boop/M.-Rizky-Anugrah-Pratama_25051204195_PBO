import pygame
import random
pygame.init()

WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Box")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

class GameObject:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))

class Pemain(GameObject):
    def __init__(self):
        super().__init__(WIDTH//2, HEIGHT-50, 40, 40, (0, 255, 0))
        self.speed = 5

class Musuh(GameObject):
    def __init__(self, level):
        x = random.randint(0, WIDTH-40)
        super().__init__(x, 0, 40, 40, (255, 0, 0))
        self.speed = random.randint(2, 5) + level

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH-40)

class Peluru(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 5, 10, (255, 255, 0))
        self.speed = 7

    def update(self):
        self.y -= self.speed

def show_game_over():
    while True:
        screen.fill((0, 0, 0))

        font_big = pygame.font.SysFont(None, 60)
        font_small = pygame.font.SysFont(None, 25)

        text1 = font_big.render("GAME OVER", True, (255, 0, 0))
        text2 = font_small.render("Tekan R untuk coba lagi", True, (255, 255, 255))
        text3 = font_small.render("Tekan Q untuk keluar", True, (255, 255, 255))

        screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 60))
        screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2))
        screen.blit(text3, (WIDTH//2 - text3.get_width()//2, HEIGHT//2 + 30))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

def reset_game():
    global player, enemies, bullets, score, lives, level, last_shot

    player = Pemain()
    enemies = [Musuh(level) for _ in range(3)]
    bullets = []
    score = 0
    lives = 3
    level = 1
    last_shot = pygame.time.get_ticks()

player = Pemain()
level = 1
lives = 3
score = 0

enemies = [Musuh(level) for _ in range(3)]
bullets = []

shoot_delay = 300
last_shot = pygame.time.get_ticks()
running = True

while running:
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.speed

    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.w:
        player.x += player.speed

    if current_time - last_shot > shoot_delay:
        bullets.append(Peluru(player.x + player.w//2, player.y))
        last_shot = current_time

    for bullet in bullets:
        bullet.update()

    for enemy in enemies:
        enemy.update()

    for bullet in bullets[:]:
        for enemy in enemies:
            if (bullet.x < enemy.x + enemy.w and
                bullet.x + bullet.w > enemy.x and
                bullet.y < enemy.y + enemy.h and
                bullet.y + bullet.h > enemy.y):

                if bullet in bullets:
                    bullets.remove(bullet)

                enemy.y = 0
                enemy.x = random.randint(0, WIDTH-40)

                score += 2

    bullets = [b for b in bullets if b.y > 0]

    for enemy in enemies:
        if (player.x < enemy.x + enemy.w and
            player.x + player.w > enemy.x and
            player.y < enemy.y + enemy.h and
            player.y + player.h > enemy.y):
            lives -= 1
            enemy.y = 0
            enemy.x = random.randint(0, WIDTH-40)

            if lives <= 0:
                retry = show_game_over()
                if retry:
                    reset_game()
                else:
                    running = False

    if score >= level * 20:
        level += 1
        enemies.append(Musuh(level))

    player.draw()

    for enemy in enemies:
        enemy.draw()

    for bullet in bullets:
        bullet.draw()

    text_score = font.render(f"Score: {score}", True, (255, 255, 255))
    text_lives = font.render(f"Lives: {lives}", True, (255, 255, 255))
    text_level = font.render(f"Level: {level}", True, (255, 255, 255))

    screen.blit(text_score, (10, 10))
    screen.blit(text_lives, (10, 40))
    screen.blit(text_level, (10, 70))

    pygame.display.update()
    clock.tick(60)

pygame.quit()