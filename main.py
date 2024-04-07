import random
from dataclasses import dataclass
from typing import Tuple

import pygame


def reset_ball(speed: float, width: int, height: int):
    """
    :param speed: speed the ball should travel at
    :param width: width of the screen
    :param height: height of the screen
    :return:
    """
    ball_x, ball_y = width / 2, height / 2

    vel_x, vel_y = speed/2, speed/2

    random_value = random.random()
    if random_value > 0.6:
        vel_y += (0.2 * speed)
        vel_x -= (0.2 * speed)
    elif random_value < 0.3:
        vel_y -= (0.2 * speed)
        vel_x += (0.2 * speed)

    if random.random() > 0.5:
        vel_y *= -1

    if random.random() > 0.5:
        vel_x *= -1

    return ball_x, ball_y, vel_x, vel_y


@dataclass
class Ball:
    radius: int
    x: int
    y: int
    speed: float
    vx: float
    vy: float
    screen_width: int
    screen_height: int

    def reset(self):
        ball_x, ball_y, vel_x, vel_y = reset_ball(self.speed, self.screen_width, self.screen_height)
        self.x = ball_x
        self.y = ball_y
        self.vx = vel_x
        self.vy = vel_y

    def time_step(self):
        """ ball's movement controls  """
        if (self.y <= 0 + self.radius) or (self.y >= self.screen_height - self.radius):
            self.vy *= -1

        self.x += self.vx
        self.y += self.vy



class Paddle:
    def __init__(self, x: int, y: int, velocity: float, width: int, height: int, screen_width: int, screen_height):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.width = width
        self.width = height
        self.screen_width = screen_width
        self.screen_height = screen_height


def main():
    pygame.init()

    width, height = 1000, 600
    wn = pygame.display.set_mode((width, height))
    pygame.display.set_caption('FIRST_PONG_GAME')

    run = True

    # color
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # the ball
    ball = Ball(15, 0, 0, 0.4, 0, 0, width, height)
    ball.reset()

    # for the paddles
    paddle_width, paddle_height = 20, 120
    paddle_y = height / 2 - paddle_height / 2
    left_paddle = Paddle(100 - paddle_width, paddle_y, 0, paddle_width, paddle_height, width, height)
    right_paddle = Paddle(width - 100, paddle_y, 0, paddle_width, paddle_height, width, height)

    right_paddle_y = left_paddle_y = height / 2 - paddle_height / 2
    left_paddle_x, right_paddle_x = 100 - paddle_width, width - 100
    right_paddle_vel = left_paddle_vel = 0

    # point counter
    left_points = 0
    right_points = 0
    font = pygame.font.SysFont(None, 48)

    # mainloop
    while run:
        wn.fill(BLACK)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    right_paddle_vel = -0.7
                if i.key == pygame.K_DOWN:
                    right_paddle_vel = 0.7
                if i.key == pygame.K_w:
                    left_paddle_vel = -0.7
                if i.key == pygame.K_s:
                    left_paddle_vel = 0.7
            if i.type == pygame.KEYUP:
                if i.key in [pygame.K_w, pygame.K_s]:
                    left_paddle_vel = 0
                elif i.key in [pygame.K_UP, pygame.K_DOWN]:
                    right_paddle_vel = 0

        if (ball.x <= 0 + ball.radius) or (ball.x >= width - ball.radius):
            if ball.x < width/2:
                right_points += 1
            else:
                left_points += 1
            ball.reset()

        ball.time_step()

        left_paddle_y += left_paddle_vel
        right_paddle_y += right_paddle_vel

        # paddle's movement controls
        if left_paddle_y >= height - paddle_height:
            left_paddle_y = height - paddle_height
        if left_paddle_y <= 0:
            left_paddle_y = 0
        if right_paddle_y >= height - paddle_height:
            right_paddle_y = height - paddle_height
        if right_paddle_y <= 0:
            right_paddle_y = 0

        if left_paddle_x <= ball.x <= left_paddle_x + paddle_width:
            if left_paddle_y <= ball.y <= left_paddle_y + paddle_height:
                ball.vx *= -1
                ball.x = left_paddle_x +paddle_width

        if right_paddle_x <= ball.x <= right_paddle_x + paddle_width:
            if right_paddle_y <= ball.y <= right_paddle_y + paddle_height:
                ball.vx *= -1
                ball.x = right_paddle_x

        pygame.draw.circle(wn, WHITE, (ball.x, ball.y), ball.radius)
        pygame.draw.rect(wn, RED, pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height))
        pygame.draw.rect(wn, RED, pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height))

       # pygame.draw.line(wn, white, (100, 0), (100, height))
        #pygame.draw.line(wn, white, (width - 100, 0), (width - 100, height))

        img = font.render(str(left_points), True, WHITE)
        wn.blit(img, (left_paddle_x, 20))

        img = font.render(str(right_points), True, WHITE)
        wn.blit(img, (right_paddle_x, 20))

        pygame.display.update()


if __name__ == '__main__':
    main()