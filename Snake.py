import pygame
import random
import time

# تنظیمات اولیه
pygame.init()
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
SPEED = 10    

# رنگ‌ها
WHITE = (250, 250, 250)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# ایجاد پنجره
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# ساعت بازی
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [[WIDTH//2, HEIGHT//2]]
        self.direction = 'RIGHT'
        self.new_block = False

    def move(self):
        x, y = self.body[0]
        if self.direction == 'RIGHT': x += BLOCK_SIZE
        elif self.direction == 'LEFT': x -= BLOCK_SIZE
        elif self.direction == 'UP': y -= BLOCK_SIZE
        elif self.direction == 'DOWN': y += BLOCK_SIZE
        new_head = [x, y]
        
        if self.new_block:
            self.body.insert(0, new_head)
            self.new_block = False
        else:
            self.body.pop()
            self.body.insert(0, new_head)

    def grow(self):
        self.new_block = True

    def draw(self):
        for idx, block in enumerate(self.body):
            color = GREEN if idx == 0 else BLUE
            pygame.draw.rect(screen, color, (block[0], block[1], BLOCK_SIZE-1, BLOCK_SIZE-1))

class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.x = random.randint(0, (WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.y = random.randint(0, (HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

def show_score(score):
    font = pygame.font.SysFont('arial', 30)
    text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(text, (10, 10))

def game_over():
    font = pygame.font.SysFont('arial', 60)
    text = font.render('Game over', True, RED)
    screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 50))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()

def main():
    snake = Snake()
    food = Food()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                    snake.direction = 'RIGHT'
                elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                    snake.direction = 'LEFT'
                elif event.key == pygame.K_UP and snake.direction != 'DOWN':
                    snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                    snake.direction = 'DOWN'

        # حرکت مار
        snake.move()

        # برخورد با دیوار
        head = snake.body[0]
        if head[0] >= WIDTH or head[0] < 0 or head[1] >= HEIGHT or head[1] < 0:
            game_over()

        # برخورد با خودش
        for block in snake.body[1:]:
            if head == block:
                game_over()

        # خوردن غذا
        if head[0] == food.x and head[1] == food.y:
            snake.grow()
            food.spawn()
            score += 1

        # رندر کردن
        screen.fill(WHITE)
        snake.draw()
        food.draw()
        show_score(score)
        pygame.display.update()
        clock.tick(SPEED)

if __name__ == "__main__":
    main()

