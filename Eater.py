import pygame
import random


pygame.font.init()
pygame.init()
font = pygame.font.SysFont('', 30)
WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
BLACK = 45, 45, 45
BLUE = 90, 90, 200
score = 0
lost_mass = 0


class Player:
    def __init__(self, position, color):
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.size = 20
        self.circle = pygame.draw.circle(window, self.color, (self.x, self.y), self.size)

    def grow(self):
        self.size += 1

    def lose_mass(self):
        global score
        global lost_mass
        chance = random.randint(0, 3500)
        if chance == 1:
            if score > 0:
                self.size -= 1
                score -= 1
                lost_mass += 1

    def score_board(self):
        text = f'Mass: {score}    Lost mass: {lost_mass}'
        show = font.render(text, True, self.color, None)
        center = show.get_rect(center=(WIDTH // 2, 40))
        window.blit(show, center)

    def move(self, speed, keyboard):
        if keyboard[pygame.K_a]:
            if self.x > 0:
                self.x -= speed
        if keyboard[pygame.K_d]:
            if self.x < WIDTH:
                self.x += speed
        if keyboard[pygame.K_w]:
            if self.y > 0:
                self.y -= speed
        if keyboard[pygame.K_s]:
            if self.y < HEIGHT:
                self.y += speed

    def render(self):
        self.circle.x = self.x
        self.circle.y = self.y
        self.circle = pygame.draw.circle(window, self.color, (self.x, self.y), self.size)


class Point:
    def __init__(self, position, color):
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.size = 20
        self.rect = pygame.rect.Rect(self.x, self.y, self.size, self.size)

    def move(self, speed):
        directions = ['right_left', 'left_right', 'up_down', 'down_up']
        direction = random.choice(directions)
        if direction == directions[0]:
            if self.x > 0:
                self.x -= speed
        if direction == directions[1]:
            if self.x < WIDTH:
                self.x += speed
        if direction == directions[2]:
            if self.y > 0:
                self.y -= speed
        if direction == directions[3]:
            if self.y < HEIGHT:
                self.y += speed

    def relocate(self):
        self.x, self.y = random_position()

    def add_point(self, player):
        global score
        if self.rect.colliderect(player.circle):
            score += 1
            player.grow()
            self.relocate()
            self.color = random_color()

    def render(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect = pygame.draw.rect(window, self.color, self.rect)


def random_position():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    positions = (x, y)
    return positions


def random_color():
    color = [0 for _ in range(3)]
    for i in range(len(color)):
        color[i] = random.randint(70, 230)
    return color


def edges():
    pygame.draw.line(window, BLUE, (0, 0), (0, HEIGHT), 4)
    pygame.draw.line(window, BLUE, (0, 0), (WIDTH, 0), 4)
    pygame.draw.line(window, BLUE, (WIDTH - 2, HEIGHT), (WIDTH - 2, 0), 4)
    pygame.draw.line(window, BLUE, (WIDTH, HEIGHT - 2), (0, HEIGHT - 2), 4)


def main():
    is_running = True
    points = [Point(random_position(), random_color()) for _ in range(6)]
    player = Player(random_position(), random_color())
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        keyboard = pygame.key.get_pressed()
        if keyboard[pygame.K_ESCAPE]:
            is_running = False
        window.fill(BLACK)

        for i in range(len(points)):
            points[i].render()
            points[i].move(0.16)
            points[i].add_point(player)

        player.render()
        player.move(0.19, keyboard)
        player.lose_mass()
        player.score_board()

        edges()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
