import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont(None, 40)

GRAVITY = 0.15
BIRD_JUMP = -4
PIPE_SPEED = 3
PIPE_GAP = 180

def get_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.vel_y = 0
        self.wing_images = [pygame.image.load(r"C:\Users\Somashekar\OneDrive\Desktop\Flappy Bird\sprite_0.png").convert_alpha(),
                            pygame.image.load(r"C:\Users\Somashekar\OneDrive\Desktop\Flappy Bird\sprite_1.png").convert_alpha()]
        self.current_wing_image = 0
        self.rect = self.wing_images[self.current_wing_image].get_rect(center=(self.x, self.y))
        self.flap_timer = 0
        self.flap_delay = 5  # Adjust the delay for wing flapping animation

    def jump(self):
        self.vel_y = BIRD_JUMP

    def move(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        self.rect.centery = self.y

    def draw(self):
        # Flap wings every few frames
        if self.flap_timer % self.flap_delay == 0:
            self.current_wing_image = (self.current_wing_image + 1) % len(self.wing_images)
        WIN.blit(self.wing_images[self.current_wing_image], self.rect)
        self.flap_timer += 1

    def collide(self, pipes):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            return True
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect_top) or self.rect.colliderect(pipe.rect_bottom):
                return True
        return False

class Pipe:
    def __init__(self, x):
        self.x = x
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.image.load(r"C:\Users\Somashekar\OneDrive\Desktop\Flappy Bird\pipe2.png").convert_alpha()
        self.PIPE_BOTTOM = pygame.image.load(r"C:\Users\Somashekar\OneDrive\Desktop\Flappy Bird\pipe.png").convert_alpha()
        self.passed = False
        self.set_height()

    def set_height(self):
        self.top = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.bottom = self.top + PIPE_GAP
        self.rect_top = self.PIPE_TOP.get_rect(midbottom=(self.x, self.top))
        self.rect_bottom = self.PIPE_BOTTOM.get_rect(midtop=(self.x, self.bottom))

    def move(self):
        self.x -= PIPE_SPEED
        self.rect_top = self.PIPE_TOP.get_rect(midbottom=(self.x, self.top))
        self.rect_bottom = self.PIPE_BOTTOM.get_rect(midtop=(self.x, self.bottom))

    def draw(self):
        WIN.blit(self.PIPE_TOP, self.rect_top)
        WIN.blit(self.PIPE_BOTTOM, self.rect_bottom)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    WIN.blit(text_surface, text_rect)

def main():
    bird = Bird()
    pipes = [Pipe(WIDTH)]
    score = 0
    best_score = get_high_score()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()

        add_pipe = False
        for pipe in pipes:
            pipe.move()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes.remove(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            if pipe.passed and pipe.x < 0:
                pipes.remove(pipe)
                score += 1

            if pipe.rect_top.colliderect(bird.rect) or pipe.rect_bottom.colliderect(bird.rect):
                running = False

        if add_pipe:
            pipes.append(Pipe(WIDTH))

        if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
            running = False

        if score > best_score:
            best_score = score
            save_high_score(best_score)

        WIN.fill(WHITE)
        for pipe in pipes:
            pipe.draw()
        bird.draw()
        draw_text(f"Score: {score}", FONT, BLACK, 50, 50)
        draw_text(f"Best Score: {best_score}", FONT, BLACK, WIDTH - 100, 50)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
