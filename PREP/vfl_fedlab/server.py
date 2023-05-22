from torch import nn
import torch as t
from torch.nn import functional as F


class ModelHead(nn.Module):
    def __init__(self):
        super(ModelHead, self).__init__()
        
        self.fc = t.nn.Sequential(
            nn.Linear(8, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.fc(x)
        return x.flatten()
    
