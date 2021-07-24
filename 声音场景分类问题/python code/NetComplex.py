import numpy as np
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(1, 42, 5,padding=2,stride=2)
        self.batch_norm1 = nn.BatchNorm2d (42)
        self.conv2 = nn.Conv2d(42, 42, 3,padding=1,stride=1)
        self.batch_norm2 = nn.BatchNorm2d (42)
        
        self.conv3 = nn.Conv2d(42, 84, 3,padding=1,stride=1)
        self.batch_norm3 = nn.BatchNorm2d (84)
        self.conv4 = nn.Conv2d(84, 84, 3,padding=1,stride=1)
        self.batch_norm4 = nn.BatchNorm2d (84)
        
        self.conv5 = nn.Conv2d(84, 168, 3,padding=1,stride=1)
        self.batch_norm5 = nn.BatchNorm2d (168)
        self.drop1 = nn.Dropout(p=0.3)
        self.conv6 = nn.Conv2d(168, 168, 3,padding=1,stride=1)
        self.batch_norm6 = nn.BatchNorm2d (168)
        self.drop2 = nn.Dropout(p=0.3)
        self.conv7 = nn.Conv2d(168, 168, 3,padding=1,stride=1)
        self.batch_norm7 = nn.BatchNorm2d (168)
        self.drop3 = nn.Dropout(p=0.3)
        self.conv8 = nn.Conv2d(168, 168, 3,padding=1,stride=1)
        self.batch_norm8 = nn.BatchNorm2d (168)
        
        self.conv9 = nn.Conv2d(168, 336, 3,padding=0,stride=1)
        self.batch_norm9 = nn.BatchNorm2d (336)
        self.drop4 = nn.Dropout(p=0.5)
        self.conv10 = nn.Conv2d(336, 336, 1,padding=0,stride=1)
        self.batch_norm10 = nn.BatchNorm2d (336)
        self.drop5 = nn.Dropout(p=0.5)
        
        self.conv11 = nn.Conv2d(336, 10, 1,padding=0,stride=1)
        self.batch_norm11 = nn.BatchNorm2d (10)

    def forward(self, x):
        x = F.relu(self.batch_norm1(self.conv1(x)))
        x = F.relu(self.batch_norm2(self.conv2(x)))
        x = F.max_pool2d(x, (2, 2))
        
        # GaussianNoise(1.00)
        x += 1 * np.random.randn(x.shape)
        
        x = F.relu(self.batch_norm3(self.conv3(x)))
        x = F.relu(self.batch_norm4(self.conv4(x)))
        x = F.max_pool2d(x, (2, 2))
        
        # GaussianNoise(0.75)
        x += 0.75 * np.random.randn(x.shape)
  
        
        x = F.relu(self.batch_norm5(self.conv5(x)))
        x = self.drop1(x)
        x = F.relu(self.batch_norm6(self.conv6(x)))
        x = self.drop2(x)
        x = F.relu(self.batch_norm7(self.conv7(x)))
        x = self.drop3(x)
        x = F.relu(self.batch_norm8(self.conv8(x)))
        x = F.max_pool2d(x, (2, 2))
        
        # GaussianNoise(0.75)
        x += 0.75 * np.random.randn(x.shape)
        
        x = F.elu(self.batch_norm9(self.conv9(x)))
        x = self.drop4(x)
        x = F.elu(self.batch_norm10(self.conv10(x)))
        x = self.drop5(x)
        
        x = self.batch_norm11(self.conv11(x))
        # GaussianNoise(0.3)
        x += 0.3 * np.random.randn(x.shape)
        x = F.avg_pool2d (x)
        
        x = F.softmax (x,dim = 10)
        
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
    