'''the_snake.py'''
from random import randint
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 8

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject():
    '''Class'''

    def __init__(self):
        self.position = POSITION
        self.body_color = None

    def draw(self):
        '''Method'''


class Snake(GameObject):
    '''Class'''

    length: int = 1

    def __init__(self):
        super().__init__()
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        '''Method'''
        if self.next_direction:
            self.direction = self.next_direction
        self.next_direction = None

    def reset(self):
        '''Method'''
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions = [POSITION]
        self.direction = RIGHT
        self.position = 0
        self.length = 0

    def get_head_position(self):
        '''Method'''
        return (
            (self.positions[0][0] + self.direction[0] * GRID_SIZE)
            % SCREEN_WIDTH,
            (self.positions[0][1] + self.direction[1] * GRID_SIZE)
            % SCREEN_HEIGHT
        )

    def move(self):
        '''Method'''
        head = self.get_head_position()
        if head in self.positions:
            self.reset()
        else:
            self.positions.insert(0, head)
            if self.position:
                self.position = self.positions.pop(-1)

    def draw(self):
        '''Method'''
        self.move()
        for position in self.positions:
            r = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, r)
            pygame.draw.rect(screen, BORDER_COLOR, r, 1)
        if self.position:
            r = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, r)
        self.position = 1


class Apple(GameObject):
    '''Class'''

    @staticmethod
    def randomize_position():
        '''Method'''
        result = (
            randint(0, SCREEN_WIDTH) * 20 % SCREEN_WIDTH,
            randint(0, SCREEN_HEIGHT) * 20 % SCREEN_HEIGHT
        )
        return result

    def __init__(self):
        super().__init__()
        self.position = None
        self.body_color = APPLE_COLOR

    def draw(self):
        '''Method'''
        self.position = self.randomize_position()
        r = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, APPLE_COLOR, r)
        pygame.draw.rect(screen, BORDER_COLOR, r, 1)


def handle_keys(snake_obj):
    '''Func'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_obj.direction != DOWN:
                snake_obj.next_direction = UP
            elif event.key == pygame.K_DOWN and snake_obj.direction != UP:
                snake_obj.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake_obj.direction != RIGHT:
                snake_obj.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake_obj.direction != LEFT:
                snake_obj.next_direction = RIGHT


def main():
    '''Main function'''
    pygame.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        if not apple.position or snake.length == 0:
            apple.draw()
            snake.length = 1
        if apple.position == snake.positions[0]:
            snake.position = None
            apple.draw()
        snake.draw()
        pygame.display.flip()
        handle_keys(snake)
        snake.update_direction()


if __name__ == '__main__':
    main()
