from .paddle import Paddle
from .ball import Ball
import pygame
import random
pygame.init()


BLUE = (10,174,255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED_d = (217,11,32)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

FONT = pygame.font.SysFont('comicsans', 50)
FONT_start = pygame.font.SysFont('comicsans', 37)
FONT_start_small = pygame.font.SysFont('comicsans', 20)


class GameInformation:
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score


class Game:
    """
    To use this class simply initialize and instance and call the .loop() method
    inside of a pygame event loop (i.e while loop). Inside of your event loop
    you can call the .draw() and .move_paddle() methods according to your use case.
    Use the information returned from .loop() to determine when to end the game by calling
    .reset().
    """
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.left_paddle = Paddle(
            10, self.window_height // 2 - Paddle.HEIGHT // 2, BLUE)
        self.right_paddle = Paddle(
            self.window_width - 10 - Paddle.WIDTH, self.window_height // 2 - Paddle.HEIGHT//2, RED_d)
        self.ball = Ball(self.window_width // 2, self.window_height // 2)

        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        self.window = window

    def _draw_score(self):
        left_score_text = self.SCORE_FONT.render(
            f"{self.left_score}", 1, self.WHITE)
        right_score_text = self.SCORE_FONT.render(
            f"{self.right_score}", 1, self.WHITE)
        self.window.blit(left_score_text, (self.window_width //
                                           4 - left_score_text.get_width()//2, 20))
        self.window.blit(right_score_text, (self.window_width * (3/4) -
                                            right_score_text.get_width()//2, 20))

    def _draw_hits(self):
        hits_text_right = self.SCORE_FONT.render(
            f"{self.right_hits}", 1, self.RED)
        hits_text_left = self.SCORE_FONT.render(
            f"{self.left_hits}", 1, self.RED)
        self.window.blit(hits_text_left, (self.window_width //
                                     4 - hits_text_left.get_width()//2, 10))
        self.window.blit(hits_text_right, (self.window_width //
                                          4 * 3- hits_text_left.get_width() // 2, 10))

    def _draw_divider(self):
        for i in range(10, self.window_height, self.window_height//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(
                self.window, self.WHITE, (self.window_width//2 - 5, i, 10, self.window_height//20))

    def _handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        if ball.y + ball.RADIUS >= self.window_height:
            ball.y_vel *= -1
        elif ball.y - ball.RADIUS <= 0:
            ball.y_vel *= -1

        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + Paddle.HEIGHT:
                if ball.x - ball.RADIUS <= left_paddle.x + Paddle.WIDTH and ball.x > 10:
                    ball.x_vel *= -1

                    middle_y = left_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.left_hits += 1

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + Paddle.HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x and ball.x > self.window_width - 28:
                    ball.x_vel *= -1

                    middle_y = right_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.right_hits += 1

    def draw(self, draw_score=True, draw_hits=False):
        self.window.fill(self.BLACK)

        self._draw_divider()

        if draw_score:
            self._draw_score()

        if draw_hits:
            self._draw_hits()

        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(self.window)

        self.ball.draw(self.window)

    def draw_start(self):
        self.window.fill(BLACK)

        start = FONT_start.render('PONG', 1, WHITE)
        intro = FONT_start.render('First to 10 WIN!!!', 1, WHITE)
        space = FONT_start_small.render('Press Space To Start', 1, WHITE)
        credit = FONT_start_small.render('CREDIT to "TECH WITH TIM"', 1, WHITE)
        minh = FONT_start_small.render('Improve by Minh Vy Ha', 1, WHITE)
        self.window.blit(start, (self.window_width // 2 - start.get_width() // 2, 20))
        self.window.blit(intro, (self.window_width // 2 - intro.get_width() // 2, 80))
        self.window.blit(space, (self.window_width // 2 - space.get_width() // 2, 150))
        self.window.blit(credit, (self.window_width // 2 - credit.get_width() // 2, 200))
        self.window.blit(minh, (self.window_width // 2 - minh.get_width() // 2, 250))
        x = self.window_width // 2 - 15 // 2

        for i in range(310, self.window_height - 10, 50):
            pygame.draw.rect(self.window, WHITE, (x, i, 15, 20))
        self.left_paddle.draw(self.window)
        self.right_paddle.draw(self.window)

    def draw_end(self, t=''):
        self.window.fill(BLACK)

        reset = FONT_start_small.render('Press R To Reset', 1, WHITE)
        congrat = FONT_start.render('Congratulation', 1, WHITE)
        self.window.blit(congrat, (self.window_width // 2 - congrat.get_width() // 2, 40))
        self.window.blit(t, (self.window_width // 2 - t.get_width() // 2, 120))

        self.window.blit(reset, (self.window_width // 2 - reset.get_width() // 2, 200))

        self.left_paddle.draw(self.window)
        self.right_paddle.draw(self.window)


    def move_paddle(self, left=True, up=True):
        """
        Move the left or right paddle.

        :returns: boolean indicating if paddle movement is valid. 
                  Movement is invalid if it causes paddle to go 
                  off the screen
        """
        if left:
            if up and self.left_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.right_paddle.move(up)

        return True

    def loop(self):
        """
        Executes a single game loop.

        :returns: GameInformation instance stating score 
                  and hits of each paddle.
        """
        self.ball.move()
        self._handle_collision()

        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.window_width:
            self.ball.reset()
            self.left_score += 1

        game_info = GameInformation(
            self.left_hits, self.right_hits, self.left_score, self.right_score)

        return game_info

    def reset(self):
        """Resets the entire game."""
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
