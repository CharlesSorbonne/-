import numpy as np

# eviter log(0) ou divise 0
zero_eviter = 1e-10


class Loss(object):
    def forward(self, yhat,y):
        pass

    def backward(self, yhat,y):
        pass

class MSELoss (Loss) :
    def forward(self,yhat,y) :
        """
        in : 
            y : (batch,d)
            yhat : (batch,d)
        out : (batch,1)
        
        """
        return np.linalg.norm (y - yhat,axis=1)**2
    def backward (self, yhat, y):
        """
        in : 
            y : (batch,d)
            yhat : (batch,d)
        out : (batch,d)
        
        """
        return 2*(yhat - y)

class CE(Loss):
    def forward(self, yhat, y):
        """
        in : 
            y : (batch,d) # onehot [0,0,1,0] == classe 2
            yhat : (batch,d) # [p0,p1,p2,p3] proba de softmax
        out : (batch,1)
        
        """
        yhat = np.maximum(yhat,zero_eviter)
        # yhat = np.minimum(yhat,1-zero_eviter) # pas nécessaire 
        # res[np.isnan(res)] = 0                # on ne peut pas traiter Nan comme ca
        return np.sum(-y*np.log(yhat),axis= 1)

    def backward(self, yhat, y):
        """
        in : 
            y : (batch,d)
            yhat : (batch,d)
        out : (batch,d)
        
        """
        yhat = np.maximum(yhat,zero_eviter)
        # yhat = np.minimum(yhat,1-zero_eviter) # pas nécessaire 
        # res[np.isnan(res)] = 0                # on ne peut pas traiter Nan comme ca
        return -y/yhat


class BCE(Loss):
    def forward(self, yhat, y):
        """
        in : 
            y : (batch,d)
            yhat : (batch,d)
        out : (batch,1)
        
        """
        yhat = np.maximum(yhat,zero_eviter)
        yhat = np.minimum(yhat,1-zero_eviter)
        return np.sum(-(y* np.maximum(np.log(yhat), -100) + (1-y)* np.maximum(-100, np.log(1-yhat))),axis= 1)

    def backward(self, yhat, y):
        """
        in : 
            y : (batch,d)
            yhat : (batch,d)
        out : (batch,d)
        
        """
        yhat = np.maximum(yhat,zero_eviter)
        yhat = np.minimum(yhat,1-zero_eviter)
        return - y/(yhat) + (1-y)/(1-yhat) 