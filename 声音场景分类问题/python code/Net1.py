import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self, nb_calsse):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)
        
        # taille :
        #   128*431 --conv(-2) --> 126*429 --pooling(//2) --> 63*214 --conv(-2) --> 61*212 --pooling(//2) --> 30*106 = 3180
        self.fc1 = nn.Linear(16*3180, 120) 
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, nb_calsse)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x): # nombre de feature
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
