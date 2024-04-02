import torch
import time
# pip install stable-baselines3[extra]
from stable_baselines3 import PPO
from gymEnv import *

# Initialization
env = room_env()
#model = PPO('CnnPolicy', env, verbose=1)
model = PPO.load('CnnModel', env=env)
iterations = 4000000
# Learning (with timing)
#env.render_mode = 'human'
env.render_mode = None
start_time = time.time()
model.learn(total_timesteps=iterations)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time for {iterations} iterations: {elapsed_time/3600} hours")
# Saving
model.save('CnnModel')
torch.save(model.policy.state_dict(),'policy.pt')


