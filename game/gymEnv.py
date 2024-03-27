import time
import pygame
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from classes import *

key_to_action = {
    0: pygame.K_SPACE,
    1: pygame.K_UP,
    2: pygame.K_RIGHT,
    3: pygame.K_LEFT
}

class room_env(gym.Env):
    def __init__(self, goal, obstacles_n):
        self.game = Game(level=goal, obstacles_n=obstacles_n)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(640, 480, 3), dtype=np.int16)
        self.terminated = False
        self.truncated = False
        self.render_mode = None
        self.info = {}

    def step(self, action):
        # Make step
        self.game.do_event(key_to_action[action])
        space.step(0.1)
        # Create observation
        self.game.draw()
        self.observation = np.transpose(
            np.array(pygame.surfarray.pixels3d(screen)), axes=(0, 1, 2))

        # Punishment for wasting time
        self.timestep_passed += 1
        self.reward = -self.timestep_passed // self.valid_timestep

        if self.timestep_passed > self.valid_timestep*100:
            self.reward = -100
            self.terminated = True

        # Lose condition
        if self.game.lose:
            self.reward = -100
            self.terminated = True

        # Win condition
        if self.game.win_condition():
            self.reward = 1000
            self.terminated = True

        if self.render_mode == 'human':
            self.render()

        return self.observation, self.reward, self.terminated, self.truncated, self.info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game.reset_game()
        self.game.draw()
        self.observation = np.transpose(
            np.array(pygame.surfarray.pixels3d(screen)), axes=(0, 1, 2))

        # reset reward
        self.reward = 0
        self.score = 0
        self.valid_timestep = 100
        self.timestep_passed = 0
        self.terminated = False
        self.truncated = False

        if self.render_mode == 'human':
            self.render()

        self.info = [self.game.robot.body.position, self.game.robot.body.angle, self.game.laser.center]

        return self.observation, self.info

    def render(self, render_mode='human'):
        self.render_mode = render_mode
        pygame.display.flip()
        clock.tick(4)

    def close(self):
        pygame.quit()