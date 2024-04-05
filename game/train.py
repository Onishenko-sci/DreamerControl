import torch
import time
# pip install stable-baselines3[extra]
from stable_baselines3 import PPO
from stable_baselines3 import DQN
from gymEnv import *

policy = 'CnnPolicy'
iterations = 1000000
file_name = 'CnnModelDQN'

# Initialization
env = room_env(policy)

model = DQN(policy, env, verbose=1, buffer_size=200000)
#model = PPO(policy, env, verbose=1, ent_coef= 0.1)
#model = PPO.load(file_name, env=env)

# Learning (with timing)
env.render_mode = None
start_time = time.time()
model.learn(total_timesteps=iterations)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time for {iterations} iterations: {elapsed_time/3600} hours")
# Saving
model.save(file_name)


