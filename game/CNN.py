import torch
from torch import nn

from gymEnv import *

# Define model
class CNN(nn.Module):
    def __init__(self, input_shape, out_actions):
        super().__init__()

        # https://poloclub.github.io/cnn-explainer/
        self.conv_block1 = nn.Sequential(
            nn.Conv2d(in_channels=input_shape, out_channels=10, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=10, out_channels=10, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )

        self.conv_block2 = nn.Sequential(
            nn.Conv2d(in_channels=10, out_channels=10, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=10, out_channels=10, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )

        self.layer_stack = nn.Sequential(
            nn.Flatten(), # flatten inputs into a single vector
            # After flattening the matrix into a vector, pass it to the output layer. To determine the input shape, use the print() statement in forward()
            nn.Linear(in_features=10*160*120, out_features=out_actions),
            nn.ReLU(),
            nn.Linear(in_features=out_actions, out_features=out_actions)
        )

    def forward(self, x):
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        # print(x.shape)  # Use this to determine input shape of the output layer.
        x = self.layer_stack(x)
        return x

def torched(state: np.ndarray):
    return (torch.from_numpy(state).permute(2,0,1).type(torch.float32)/255).unsqueeze(dim=0)

def dated(info):
    return torch.tensor([info[0][0], info[0][1], info[1], info[2][0],info[2][1]], dtype=torch.float32).unsqueeze(dim=0)

def create_batch(env, batch_size):
    observation , info = env.reset()
    X_train = torched(observation)
    y_train = dated(info)
    for i in range(batch_size-1):
        observation , info = env.reset()
        X_train = torch.cat((X_train, torched(observation)), dim=0)
        y_train = torch.cat((y_train, dated(info)), dim=0 )
    return X_train, y_train

if __name__ == '__main__':

    model = CNN(3,5)
    loss_fn = nn.MSELoss()
    optim = torch.optim.SGD(model.parameters(), lr=0.1)
    batch_size = 32
    # Setup ep
    epochs = 100

    env = room_env('laser', obstacles_n=0)


    for epoch in range(epochs):

        X_train, y_train = create_batch(env, batch_size)
        y_train = y_train/1000

        model.train()
        y_pred = model(X_train)
        loss = loss_fn(y_pred,y_train)

        #print(f'Predicted: {y_pred[0]}')
        #print(f'Real : {y_train[0]}')

        optim.zero_grad()
        loss.backward()
        optim.step()

        ### Testing
        model.eval()

        X_test,y_test = create_batch(env, batch_size)
        y_test = y_test/1000
        with torch.inference_mode():
            y_test_pred = model(X_test)

            test_loss = loss_fn(y_test_pred,y_test)

        # Print out what's happening every 100 epochs
        if epoch % 1 == 0:
            print(f"Epoch: {epoch} | Loss: {loss:.5f}, | Test loss: {test_loss:.5f}")


    X_test,y_test = create_batch(env, batch_size)
    y_test = y_test/1000
    with torch.inference_mode():
        y_test_pred = model(X_test)

    print(f'Predicted: {y_test_pred[0]}')
    print(f'Real : {y_test[0]}')

    model.state_dict 
    torch.save( model.state_dict(), 'cnn.pt')