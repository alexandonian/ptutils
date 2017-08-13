import torch.nn as nn
import torch.optim as optim
from ptutils.nn import model

class Monkey(model.Model):

    def __init__(self):
        self.model = model.CNN()
        self.lr = 1e-3
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), self.lr)

    def fit(self, input, target):
        output = self.model(input)

        self.optimizer.zero_grad()
        loss = self.criterion(output, target)
        loss.backwards()
        self.optimizer.step()
