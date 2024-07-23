import torch
import torch.nn as nn
import torch.nn.functional as functional

class AlphaZeroNet(nn.Module):
    def __init__(self):
        super(AlphaZeroNet, self).__init__()
        # Convolutional layers
        self.conv1 = nn.Conv2d(18, 256, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(256, 256, kernel_size=3, padding=1)

        self.batchN1 = nn.BatchNorm2d(256)
        self.batchN2 = nn.BatchNorm2d(256)
        self.batchN3 = nn.BatchNorm2d(256)
        self.batchN4 = nn.BatchNorm2d(256)

        # Policy head
        self.policy_conv = nn.Conv2d(256, 2, kernel_size=1)
        self.policy_batchN = nn.BatchNorm2d(2)
        self.policy_fc = nn.Linear(2 * 8 * 8, 1968)  # 1968 = 8*8*3*8
        
        # Value head
        self.value_conv = nn.Conv2d(256, 1, kernel_size=1)
        self.value_batchN = nn.BatchNorm2d(1)
        self.value_fc1 = nn.Linear(8 * 8, 256)
        self.value_fc2 = nn.Linear(256, 1)

    def forward(self, x):
        # Common layers
        x = functional.relu(self.batchN1(self.conv1(x)))
        x = functional.relu(self.batchN2(self.conv2(x)))
        x = functional.relu(self.batchN3(self.conv3(x)))
        x = functional.relu(self.batchN4(self.conv4(x)))

        # Policy head
        policy = functional.relu(self.policy_batchN(self.policy_conv(x)))
        policy = policy.view(-1, 2 * 8 * 8)
        policy = functional.log_softmax(self.policy_fc(policy), dim=1)

        # Value head
        value = functional.relu(self.value_batchN(self.value_conv(x)))
        value = value.view(-1, 8 * 8)
        value = functional.relu(self.value_fc1(value))
        value = torch.tanh(self.value_fc2(value))

        return policy, value

def save_model(model, path):
    torch.save(model.state_dict(), path)

def load_model(path):
    model = AlphaZeroNet()
    model.load_state_dict(torch.load(path))
    model.eval()
    return model

