import random
from typing  import Tuple

import pygame


def reset_ball(speed: float, width: int, height: int):
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


def main():
    pygame.init()

    width, height = 1000, 600
    wn = pygame.display.set_mode((width, height))
    pygame.display.set_caption('FIRST_PONG_GAME')

    run = True

    # color
    white = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # the ball
    radius = 15
    speed = 0.4
    ball_x, ball_y, vel_x, vel_y = reset_ball(speed, width, height)

    # for the paddles
    paddle_width, paddle_height = 20, 120
    right_paddle_y = left_paddle_y = height / 2 - paddle_height / 2
    left_paddle_x, right_paddle_x = 100 - paddle_width, width - 100
    right_paddle_vel = left_paddle_vel = 0

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

        # ball's movement controls
        if (ball_y <= 0 + radius) or (ball_y >= height - radius):
            vel_y *= -1

        if (ball_x <= 0 + radius) or (ball_x >= width - radius):
            ball_x, ball_y, vel_x, vel_y = reset_ball(speed, width, height)

        ball_x += vel_x
        ball_y += vel_y

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

        if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
            if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
                vel_x *= -1
                ball_x = left_paddle_x +paddle_width

        if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
            if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
                vel_x *= -1
                ball_x = right_paddle_x

        pygame.draw.circle(wn, white, (ball_x, ball_y), radius)
        pygame.draw.rect(wn, RED, pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height))
        pygame.draw.rect(wn, RED, pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height))

       # pygame.draw.line(wn, white, (100, 0), (100, height))
        #pygame.draw.line(wn, white, (width - 100, 0), (width - 100, height))
        pygame.display.update()


if __name__ == '__main__':
    main()