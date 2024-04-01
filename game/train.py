import torch
import time
# pip install stable-baselines3[extra]
from stable_baselines3 import PPO
from gymEnv import *

# Initialization
env2 = room_env()
model = PPO('CnnPolicy', env2, verbose=1)
iterations = 2048
# Learning (with timing)
env2.render_mode = None
start_time = time.time()
model.learn(total_timesteps=iterations)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time for {iterations} iterations: {elapsed_time/3600} hours")
# Visual evaluation
env2.render_mode = 'human'
model.learn(2048)
# Saving
model.save('CnnModel')
torch.save(model.policy.state_dict(),'policy.pt')

