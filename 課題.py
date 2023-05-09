import pygame
import random

# ウィンドウのサイズ
WIDTH = 800
HEIGHT = 600

# 色
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 自機の画像
player_image = pygame.image.load("player.png")

# 敵機の画像
enemy_image = pygame.image.load("enemy.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        # キーボードの入力に応じて自機を移動させる
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # 自機が画面外に出ないようにする
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 5)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

score = 0
font = pygame.font.Font(None, 36)

for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # 自機と敵機の衝突判定
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        score += 1

        # スコアに応じて自機の画像を変更する
        if score >= 10:
            player.image = pygame.image.load("player2.png")

    # 画面の描画
    screen.fill(WHITE)
    all_sprites.draw(screen)
        # スコアの表示
    score_text = font.render("Score: {}".format(score), True, RED)
    screen.blit(score_text, (10, 10))

    if len(enemies) < 10:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

