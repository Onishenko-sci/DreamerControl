import torch
import time
from stable_baselines3 import PPO
import stable_baselines3

start_time = time.time()
iterations = 100000

Log_path = os.path.join('Training', 'logs')

env2 = room_env()
model = PPO('CnnPolicy', env2, verbose=1)

env2.render_mode = None
model.learn(total_timesteps=iterations)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time for {iterations} iterations: {elapsed_time} seconds")


env2.render_mode = 'human'
model.learn(3)

model.save('EasyModel')
torch.save(model.policy.state_dict(),'5inPolisymodel.pt')

