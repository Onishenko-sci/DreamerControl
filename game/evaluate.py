
from stable_baselines3 import PPO
from gymEnv import *


env = room_env('CnnPolicy')
model = PPO.load('CnnModel', env=env)
# Visual evaluation
env.render_mode = 'human'
model.learn(2048)