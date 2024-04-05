import time
import pygame
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import cv2

from classes import *


key_to_action = {
    0: pygame.K_UP,
    1: pygame.K_RIGHT,
    2: pygame.K_LEFT,
    4: pygame.K_SPACE
}

class room_env(gym.Env):
    def __init__(self, mode='CnnPolicy'):
        self.mode = mode
        self.game = Game('laser', 0)
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=255, shape=( 100, 100, 1 ), dtype=np.uint8)

        if mode == 'MlpPolicy':
            self.observation_space = spaces.Box(low=0, high=361, shape=(5, ), dtype=np.int16)

        self.terminated = False
        self.truncated = False
        self.render_mode = None
        self.info = {}
        self.temp = 0
        self.valid_timestep = 25
        self.dist = 0
        self.prev_dist = 0
        self.reward = 0


    def step(self, action):
        # Make step
        self.game.do_event(key_to_action[action])
        space.step(1)
        # Create observation
        self.game.draw()

        cadr = np.transpose(np.array(pygame.surfarray.pixels3d(screen)), axes=(0, 1, 2))

        self.observation = (cadr[:,:,0])[:,:,np.newaxis]

        self.reward_a = 0
        self.reward_b = 0
        self.reward_c = 0
        self.reward_d = 0

        # Lose condition
        if self.game.lose or self.timestep_passed>200:
            self.reward_a = -100
            self.terminated = True

        # Distance reward and punishment
        self.dist = abs(self.game.robot.body.position-self.game.laser.center)
        if self.dist > self.prev_dist:
            self.reward_b = -1
        elif self.dist < self.prev_dist:
            self.reward_b = 1
        else:
            self.reward_b = 0
        self.prev_dist = self.dist


        # Win condition
        if self.game.robot_touch_laser():
            self.reward_c = 100
            self.terminated = True

        # Punishment for wasting time
        self.timestep_passed += 1
        self.reward_d = -self.timestep_passed // self.valid_timestep + 1

        self.reward = self.reward_a + self.reward_b + self.reward_c + self.reward_d
        
        if self.render_mode == 'human':
            #print('Action ', action)
            print('Reward: ', self.reward)
            self.render()

        #Change observation to Robot pos, Robot angle, Lazer pos
        if self.mode == 'MlpPolicy':
            self.observation = self.short_obs()

        return self.observation, self.reward, self.terminated, self.truncated, self.info

    def short_obs(self):
      robot_pos = self.game.robot.body.position
      robot_angle = int(360*self.game.robot.body.angle/(2*math.pi))
      if robot_angle > 360: robot_angle= robot_angle-360
      if robot_angle < 0: robot_angle= robot_angle+360
      laser_pos = self.game.laser.center
      short_observation = np.array([robot_pos[0],robot_pos[1],robot_angle,laser_pos[0],laser_pos[1]], dtype=int)
      return short_observation

    def reset(self, seed=None, options=None):
        self.temp = self.temp + 1
        #print(self.temp)

        super().reset(seed=seed)
        self.game.reset_game()
        self.game.draw()

        cadr = np.transpose(np.array(pygame.surfarray.pixels3d(screen)), axes=(0, 1, 2))
        self.observation = (cadr[:,:,0])[:,:,np.newaxis]

        # Reset reward
        self.timestep_passed = 0
        self.terminated = False
        self.truncated = False

        if self.render_mode == 'human':
            self.render()

        if self.mode == 'MlpPolicy':
            self.observation = self.short_obs()

        return self.observation, self.info

    def render(self):
        pygame.display.flip()
        clock.tick(30)


    def close(self):
        pygame.quit()
