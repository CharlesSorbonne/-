from module import Module
import numpy as np

class Sequentiel(Module) :
    def __init__(self,modules):
        self.modules = modules
        self.Z = None # Z = g(a)
        self.A = None # g'(a)
        self._parameters = None
        
    def zero_grad(self):
        ## Annule gradient
        self._gradient = None
        self.Z = None
        self.A = None
        
    def forward(self,X) :
        self.Z = [X] # on considere que la couche initiale : a = z = X 
        self.A = [X]
        self._parameters = []
        for module in self.modules:
            self.A.append(module.A(X))
            X = module.forward(X)
            self.Z.append(X)
            self._parameters.append(module._parameters)
        return X
    
        
    def backward(self,delta,gradient_step=1e-5) : # delta^L deniere couche
        for i in range(1,len(self.modules)+1):
            module = self.modules[-i]
            inputZ = self.Z[-i-1]
            inputA = self.A[-i-1]
            
            #print (1,inputZ.shape,delta.shape,inputA.shape)
            module.backward_update_gradient(inputZ, delta)
            #print (2,module._gradient,module._parameters)
            module.update_parameters(gradient_step=gradient_step)
            #print (3,module._parameters)
            
            delta = module.backward_delta(inputA, delta) # delta^h
            
            module.zero_grad()