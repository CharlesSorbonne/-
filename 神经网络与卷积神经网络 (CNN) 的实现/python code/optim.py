import numpy as np

class Optim (object):
    def __init__(self,net,loss,eps):
        self.net = net
        self.loss = loss
        self.eps = eps 
        self.cost = []
    
    def step(self,batch_x,batch_y,gradient_step=1e-5,batch_size = 50) :
        # SGD
        N,d = batch_x.shape[:2]
        batch_size = min(batch_size,N)
        for i in range(N//batch_size):
            output = self.net.forward(batch_x[i*batch_size:(i+1)*batch_size])
            delta = self.loss.backward(output,batch_y[i*batch_size:(i+1)*batch_size])
            self.net.backward(delta,gradient_step=gradient_step)

            self.output = self.net.forward(batch_x)
            self.cost.append(np.mean(self.loss.forward(self.output,batch_y),axis = 0,keepdims = True))
        
    def backward (self,batch_x,batch_y,maxite = 5000,batch_size = 50) :
        for _ in range(maxite):
            self.step (batch_x,batch_y,gradient_step=self.eps,batch_size=batch_size)