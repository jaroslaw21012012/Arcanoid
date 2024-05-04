import random
import sys, pygame, time
from pygame.locals import *
pygame.init()

# --SETTINGS--
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
clock = pygame.time.Clock()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ARCANOID")
points = 0
# --colors--
COLOR1 = (255, 0, 0)
COLOR2 = (0, 255, 0)
COLOR3 = (0, 100, 255)
COLOR4 = (255, 255, 255)
COLOR5 = (0, 0, 0)
BRICK_COLORS = (COLOR1, COLOR2, COLOR3, COLOR4, COLOR5)
# --text--
font = pygame.font.Font("assets/fonts/AGENCYB.TTF", 30)
font_gameover = pygame.font.Font("assets/fonts/AGENCYB.TTF", 60)
    #-gameover-text--
gameover_text_surf = font_gameover.render(f"GAME OVER", True, COLOR4)
gameover_text_rect = gameover_text_surf.get_rect()
gameover_text_rect.midbottom = (400, 250)
    #-restart_btn--
restart_text_surf = font_gameover.render("RESTART", True, COLOR4)
restart_text_rect = restart_text_surf.get_rect()
restart_text_rect.midbottom = (400, 400)
    #-win-text--
win_text_surf = font_gameover.render("YOU WON", True, COLOR4)
win_text_rect = win_text_surf.get_rect()
win_text_rect.midbottom = (400, 250)
# --class--
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size_x = 170
        self.size_y = 30
        self.shape = pygame.Surface((self.size_x, self.size_y))
        self.shape.fill((255, 122, 0))
        self.rect = self.shape.get_rect()
        self.rect.center = (400, 550)

    def draw(self):
        display.blit(self.shape, self.rect)

    def move(self, x):
        self.rect.centerx = x


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 10
        self.size = int(self.radius * 2)
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (400, 510)
        self.in_platform = True
        self.dx = random.choice((-1, 1))
        self.dy = -1
        self.speed = 4

    def draw(self):
        pygame.draw.circle(display, (160, 160, 160), self.rect.center, self.radius)

    def move(self, platform, mode):
        if mode == "game":
            if self.in_platform:
                self.rect.midbottom = platform.rect.midtop
                return
            self.rect.x += self.dx * self.speed
            self.rect.y += self.dy * self.speed
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.dx = -self.dx
            if self.rect.top <= 0:
                self.dy = -self.dy
            if self.rect.colliderect(platform.rect) and self.dy > 0:
                self.detect_collision(platform.rect)



    def detect_collision(self, rect):
        if self.dy > 0:
            self.dy = -self.dy

class BonusBall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 10
        self.size = int(self.radius * 2)
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.x = x
        self.rect.y = y
        self.dx = random.choice((-1, 1))
        self.dy = -1
        self.speed = 4

    def draw(self):
        pygame.draw.circle(display, (0, 255, 255), self.rect.center, self.radius)

    def move(self, platform, mode):
        if mode == "game":
            self.rect.x += self.dx * self.speed
            self.rect.y += self.dy * self.speed
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.dx = -self.dx
            if self.rect.top <= 0:
                self.dy = -self.dy
            if self.rect.colliderect(platform.rect) and self.dy > 0:
                self.detect_collision(platform.rect)

    def detect_collision(self, rect):
        if self.dy > 0:
            self.dy = -self.dy

class Brick(pygame.sprite.Sprite):
    def __init__(self, left, top):
        super().__init__()
        self.rect = pygame.Rect(left, top, 75, 25)
        self.color = (91, 127, 0)
        self.hp = 3

    def draw(self):
        pygame.draw.rect(display, self.color, self.rect, border_radius=5)

    def check_collision(self, ball):
        if ball.rect.colliderect(self.rect):
            if ball.dy < 0:
                ball.dy = -ball.dy
            else:
                ball.dy = -ball.dy
            if ball.dx > 0:
                ball.dx = -ball.dx
            else:
                ball.dx = -ball.dx
            return True
        return False


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = 10
        self.speed = 2

    def draw(self):
        pygame.draw.polygon(display, (255, 255, 255), ((self.x - self.radius, self.y - self.radius // 3),
                                                       (self.x + self.radius, self.y - self.radius // 3),
                                                       (self.x - self.radius // 2, self.y + self.radius),
                                                       (self.x, self.y - self.radius),
                                                       (self.x + self.radius // 2, self.y + self.radius),))

    def move(self, mode):
        if mode == "game":
            self.y += self.speed


# --CYCLE--
def game():
    global points
    mode = "game"
    platform = Platform()
    ball = Ball()
    bricks = []
    bonuses = []
    bonus_balls = []
    for y in range(4):
        for x in range(10):
            brick = Brick(x * 80 + 2.5, y * 30 + 3)
            bricks.append(brick)
    while True:
        display.fill((53, 21, 176))
        platform.draw()
        ball.draw()
        points_text_surf = font.render(f"SCORE: {points}", True, COLOR4)
        points_text_rect = points_text_surf.get_rect()
        points_text_rect.midbottom = (70, 580)
        if mode == "game":
            display.blit(points_text_surf, points_text_rect)
        if mode == "end":
            display.blit(gameover_text_surf, gameover_text_rect)
            result_text_surf = font.render(f"You're score: {points}", True, COLOR4)
            result_text_rect = result_text_surf.get_rect()
            result_text_rect.midbottom = (400, 300)
            display.blit(result_text_surf, result_text_rect)
            btn = pygame.draw.rect(display, COLOR5, (result_text_rect.left - 20, restart_text_rect.top - 10, result_text_rect.right - result_text_rect.left + 40, 100), border_radius=10)
            display.blit(restart_text_surf, restart_text_rect)
        if mode == "win":
            display.blit(win_text_surf, win_text_rect)
            btn = pygame.draw.rect(display, COLOR5, (result_text_rect.left - 20, restart_text_rect.top - 10, result_text_rect.right - result_text_rect.left + 40, 100), border_radius=10)
            display.blit(restart_text_surf, restart_text_rect)
        for brick in bricks:
            brick.draw()
            if brick.check_collision(ball):
                brick.hp -= 1
                if brick.hp == 2:
                    brick.color = (145, 196, 5)
                elif brick.hp == 1:
                    brick.color = (189, 255, 7)
                elif brick.hp == 0:
                    bonus = Bonus(brick.rect.centerx, brick.rect.centery)
                    bonuses.append(bonus)
                    bricks.remove(brick)
                    ball.speed += 0.2
                    points += 1
                    break
            for bonus_ball in bonus_balls:
                if brick.check_collision(bonus_ball):
                    bonus = Bonus(brick.rect.centerx, brick.rect.centery)
                    bonuses.append(bonus)
                    brick.hp -= 1
                    if brick.hp == 2:
                        brick.color = (145, 196, 5)
                    elif brick.hp == 1:
                        brick.color = (189, 255, 7)
                    elif brick.hp == 0:
                        bricks.remove(brick)
                        points += 1
                        break
        for bonus in bonuses:
            bonus.draw()
            bonus.move(mode)
            if bonus.y >= SCREEN_HEIGHT:
                bonuses.remove(bonus)
            elif platform.rect.collidepoint(bonus.x, bonus.y):
                bonuses.remove(bonus)
                bonus_ball = BonusBall(ball.rect.x, ball.rect.y)
                bonus_balls.append(bonus_ball)
        for bonus_ball in bonus_balls:
            bonus_ball.draw()
            bonus_ball.move(platform, mode)
            if bonus_ball.rect.y >= SCREEN_HEIGHT:
                bonus_balls.remove(bonus_ball)
        ball.move(platform, mode)

        if ball.rect.bottom >= SCREEN_HEIGHT:
            mode = "end"
        elif len(bricks) == 0:
            mode = "win"




        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEMOTION and mode == "game":
                platform.move(event.pos[0])
            elif event.type == MOUSEBUTTONDOWN and mode == "game":
                if ball.in_platform:
                    ball.in_platform = False
            elif event.type == MOUSEBUTTONDOWN and (mode == "end" or mode == "win") and btn.collidepoint(event.pos):
                ball.in_platform = True
                bonuses = []
                bonus_balls = []
                bricks = []
                for y in range(4):
                    for x in range(10):
                        brick = Brick(x * 80 + 2.5, y * 30 + 3)
                        bricks.append(brick)
                points = 0
                mode = "game"

        pygame.display.update()
        clock.tick(FPS)










if __name__ == '__main__':
    game()