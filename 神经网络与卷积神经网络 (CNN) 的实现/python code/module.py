import numpy as np

class Module(object):
    def __init__(self):
        self._parameters = None
        self._gradient = None

    def zero_grad(self):
        ## Annule gradient
        self._gradient = None
        pass

    def forward(self,X) :
        if self._input != X.shape[1]:
            print ("Dimension Error !")
            exit(0)
        """
        in : 
            X : (batch,input)
        out : 
            Z : (batch,output)
        
        """
        vfunc = np.vectorize(self.g)
        return vfunc(X@self._parameters)
    
    def A (self,X) :
        if self._input != X.shape[1]:
            print ("Dimension Error !")
            exit(0)
        """
        in : 
            X : (batch,input)
        out : 
            A : (batch,output)
        
        """
        return X@self._parameters
    

    def update_parameters(self, gradient_step=1e-5):
        ## Calcule la mise a jour des parametres selon le gradient calcule et le pas de gradient_step
        self._parameters -= gradient_step*self._gradient

        
    def backward_update_gradient(self, input, delta):
        ## Met a jour la valeur du gradient
        """
        in : 
            input : (batch,input) Z^(h-1)
            delta : (batch,output)  delta^(h) # (1,output) pour chaqu'un et on a batch echantillion
            
        out : 
            gradient : (input,output)
        
        """
        self._gradient = input.T@delta
        

    def backward_delta(self, input, delta):
        ## Calcul la derivee de l'erreur
        """
        in : 
            input : (batch,input) A^(h)
            delta : (batch,output) delta^(h+1)
            parameters : (input,output) h+1 couche
        out : 
            delta : (batch,input) delta^(h)
        
        """
        """
        deltain =  np.zeros((input.shape[0],self._input))
        for n in range (input.shape[0]):
            for i in range(self._input) :
                for j in range(self._output) :
                    deltain[n,i] += delta[n,j]*self._parameters[i,j]*self.g_gradient(input[n,i])
        """
        return delta@(self._parameters.T)*self.g_gradient(input)



####################
###### Linear ######
####################



class Linear (Module) :
    def __init__(self,input,output,Nan_eviter=1e-1,Positive_parameters=False):
        if Positive_parameters :
            self._parameters = np.random.random((input,output))*Nan_eviter
        else :
            self._parameters = 2*(np.random.random((input,output))-0.5)*Nan_eviter
        self._gradient = np.zeros((input,output))
        self._input = input #int 
        self._output = output #int
    
    def g(self,x):
        return x
        
    def g_gradient (self,x) :
        return 1



class Sigmoide (Linear):
    def g(self,x):
        return 1/(1+np.exp(-x))
        
    def g_gradient (self,x) :
        return self.g(x)*(1-self.g(x))


class TanH (Linear):
    def g(self,x):
        return np.tanh(x)
        
    def g_gradient (self,x) :
        return 1-np.tanh(x)**2


class Softmax (Linear) :
    def forward(self,X) :
        if self._input != X.shape[1]:
            exit(0)
        """
        in : 
            X : (batch,input)
        out : 
            Z : (batch,output)
        
        """
        return self.g(X@self._parameters)
    
    def g(self,x, axis=1):
        # pour lutter contre la saturation (overflow)
        row_max = x.max()
        row_max=row_max.reshape(-1, 1)
        x = x - row_max
        x_exp = np.exp(x)
        x_sum = np.sum(x_exp, axis=axis, keepdims=True)
        s = x_exp / x_sum
        return s
        
    def g_gradient (self,x) :
        # on ne compte le gradient de softmax
        return 1


class ReLU (Linear):
    def g(self,x):
        return np.maximum(0,x)
        
    def g_gradient (self,x) :
        return (x>=0)*1




#################
###### CNN ######
#################


class Conv1D (Module):
    def __init__(self,chan_in,chan_out,k_size,stride=1,Nan_eviter=1e-1,Positive_parameters=False):
        if Positive_parameters :
            self._parameters = np.random.random((k_size,chan_in,chan_out))*Nan_eviter
        else :
            self._parameters = 2*(np.random.random((k_size,chan_in,chan_out))-0.5)*Nan_eviter
        self._gradient = np.zeros((k_size,chan_in,chan_out))
        self.chan_in = chan_in
        self.chan_out = chan_out
        self.k_size = k_size
        self.stride = stride

    def Convolution (self,X) :
        """
        in :
            X : (batch,length,chan_in)
        out :
            Z : (batch, (length-k_size)/stride +1,chan_out).
        """
        batch,length,chan_in = X.shape
        
        if chan_in != self.chan_in :
            print ("Dimension Error !")
            exit(0)
            
        """
        res = np.zeros((batch, (l - self.k_size)//self.stride + 1, self.chan_out))
        for n in range(batch):
            X0 = X[n] # dim (length,chan_in)
            for f in range(self.chan_out): 
                W = self._parameters[:,:,f] # dim (k_size,chan_in)
                for i in range(0,res.shape[1]):
                    j = i*self.stride
                    X1 = X0[j:j+self.k_size] # dim (k_size,chan_in)
                    res[n,i,f] = (X1 * W).sum()
        return res
                
        """
        resultat = None
        for chan_o in range(self.chan_out):
            resChaqueChaine = None
            for i in range((length-self.k_size)//self.stride +1) :
                tmp = np.sum(np.sum(X[:,i:(i+self.k_size),:] * self._parameters[:,:,chan_o],axis = 2,keepdims=True),axis = 1,keepdims=True)
                if resChaqueChaine is None :
                    resChaqueChaine = tmp
                else :
                    resChaqueChaine = np.concatenate((resChaqueChaine,tmp),axis = 1)
            if resultat is None:
                resultat = resChaqueChaine
            else :
                resultat = np.concatenate((resultat,resChaqueChaine),axis = 2)
        return resultat
    
    
    def forward(self,X) :
        """
        in :
            X : (batch,length,chan_in)
        out :
            Z : (batch, (length-k_size)/stride +1,chan_out).
        """
        batch,length,chan_in = X.shape
        if chan_in != self.chan_in :
            print ("Dimension Error !")
            exit(0)
        return self.Convolution(X)

    
    def A (self,X) :
        """
        in :
            X : (batch,length,chan_in)
        out :
            A : (batch,(length-k_size)/stride +1,chan_out)
        """
        batch,length,chan_in = X.shape
        if chan_in != self.chan_in :
            print ("Dimension Error !")
            exit(0)
        return self.Convolution(X)
    

    def update_parameters(self, gradient_step=1e-5):
        ## Calcule la mise a jour des parametres selon le gradient calcule et le pas de gradient_step
        self._parameters -= gradient_step*self._gradient

        
    def backward_update_gradient(self, input, delta):
        ## Met a jour la valeur du gradient
        """
        in : 
            input : (batch,length,chan_in)                      Z^(h-1)
            delta : (batch,(length-k_size)/stride +1,chan_out)  delta^(h)
        out : 
            gradient : (k_size,chan_in,chan_out)
        
        dérivation de oi par rapport à W = X successif
        """
        self._gradient = np.zeros((self.k_size,self.chan_in,self.chan_out))
        
        batch, length_out, chan_out = delta.shape
            
        for n in range(batch):
            for o in range(chan_out):
                for l in range(length_out):
                    Xs = input[n, (l*self.stride):(l*self.stride+self.k_size), :] # dim (k_size, chan_in)
                    
                    self._gradient[:,:,o] += Xs*delta[n,l,o] # delta[n,l,o] = float : dim 1
        

    def backward_delta(self, input, delta):
        ## Calcul la derivee de l'erreur
        """
        in : 
            input : (batch,length,chan_in)                         A^(h)
            delta : (batch,(length-k_size)/stride +1,chan_out)
            parameters : (k_size,chan_in,chan_out)                 h+1 couche
        out : 
            delta : (batch,length,chan_in) delta^(h)
        
        dérivation de oi par rapport à X = W pas successif
        """
        batch, length_out, chan_out = delta.shape
        
        res = np.zeros(input.shape)

        for n in range(batch):
            for o in range(chan_out):
                Ws = self._parameters[:,:,o] # dim (k_size, chan_in)
                for l in range(length_out):
                    # version simple pour tous les stride (pas néccessaire de calcule pour chaque Xi la valeur de delta)
                    res[n, (l*self.stride):(l*self.stride+self.k_size),:] += Ws*delta[n,l,o] # delta[n,l,o] = float : dim 1
        return res




class MaxPool1D(Module):
    def __init__(self,k_size,stride=None):
        self.k_size = k_size
        
        if stride :
            self.stride = stride
        else : 
            self.stride = k_size
        
        self.maxind = None

        self._parameters = [] # pas de paramètre, juste pour bien former
    
    
    def forward(self,X):
        """
        in :
            X : (batch,length,chan_in)
        out :
            Z : (batch, (length-k_size)/stride +1,chan_in)
            maxind : (batch, (length-k_size)/stride +1,chan_in) : np.argmax pour chaque Zi
        """
        batch,length,chan_in = X.shape
        length_out = (length-self.k_size)//self.stride + 1
        
        res = np.zeros((batch, length_out, chan_in))
        self.maxind = np.zeros(res.shape)

        for l in range(length_out):
            self.maxind[:,l] = np.argmax(X[:, (l*self.stride):(l*self.stride+self.k_size)],axis=1) + l * self.stride
            res[:,l,:] = np.max(X[:,(l*self.stride):(l*self.stride+self.k_size)], axis=1)
            
        self.maxind = np.int0(self.maxind)
        
        return res


    def A (self,X) :
        """
        in :
            X : (batch,length,chan_in)
        out :
            Z : (batch, (length-k_size)/stride +1,chan_in)
            maxind : (batch, (length-k_size)/stride +1,chan_in) : np.argmax pour chaque Zi
        """
        return self.forward(X)

    
    def update_parameters(self, gradient_step=1e-5):
        """
        MaxPooling n'a pas de paramètre
        """  
        pass
        

    def backward_update_gradient(self, input, delta):
        """
        MaxPooling n'a pas de paramètre
        """       
        pass

    
    def backward_delta(self, input, delta):
        ## Calcul la derivee de l'erreur
        """
        in : 
            input : (batch,length,chan_in) 
            delta : (batch,(length-k_size)/stride +1,chan_in)
            maxind : (batch, (length-k_size)/stride +1,chan_in)
        out : 
            delta : (batch,length,chan_in) delta^(h)
        
        MaxPooling n'a pas de paramètre et il n'y a pas des gradient(0) pour les valeurs non maximales.
            car si on changer les valeurs, il change rien l'output
                Tous les autres neurones obtiennent un gradient nul.
        De plus, le max est localement linéaire avec la pente 1, par rapport à l'entrée qui atteint réellement le max.
        Ainsi, le gradient de la couche suivante est renvoyé uniquement au neurone qui a atteint le maximum.(maxind)
        """
        batch,length,chan_in = input.shape
        batch,length_out,chan_in = self.maxind.shape
        
        res = np.zeros(input.shape)
        
        for n in range(batch):
            for l in range(length_out):
                for i in range(chan_in):
                    res[n,self.maxind[n,l,i],i] = delta[n,l,i] # dim 1
        
        return res




class Flatten(Module):
    def __init__(self):
        self._parameters = [] # pas de paramètre, juste pour bien former

    
    def forward(self,X):
        """
        in :
            X : (batch,length,chan_in)
        out :
            Z : (batch,length*chan_in)
        """
        return X.reshape((len(X),-1))
    

    def A (self,X) :
        """
        in :
            X : (batch,length,chan_in)
        out :
            Z : (batch,length*chan_in)
        """
        return self.forward(X)


    def update_parameters(self, gradient_step=1e-5):
        """
        Flatten n'a pas de paramètre
        """  
        pass
        

    def backward_update_gradient(self, input, delta):
        """
        Flatten n'a pas de paramètre
        """       
        pass
        
        
    def backward_delta(self, input, delta):
        ## Calcul la derivee de l'erreur
        """
        in : 
            input : (batch,length,chan_in) resultat de Pooling
            delta : (batch,length*chan_out) = (batch,length*chan_in)
        out : 
            delta : (batch,length,chan_in)  delta^(h)
        """
        return delta.reshape(input.shape)





class AvgPool1D(Module):
    def __init__(self,k_size,stride=None):
        self.k_size = k_size
        
        if stride :
            self.stride = stride
        else : 
            self.stride = k_size
        
        self.maxind = None

        self._parameters = [] # pas de paramètre, juste pour bien former
    
    
    def forward(self,X):
        """
        in :
            X : (batch,length,chan_in)
        out :
            Z : (batch, (length-k_size)/stride +1,chan_in)
            maxind : (batch, (length-k_size)/stride +1,chan_in) : np.argmax pour chaque Zi
        """
        batch,length,chan_in = X.shape
        length_out = (length-self.k_size)//self.stride + 1
        
        res = np.zeros((batch, length_out, chan_in))

        for l in range(length_out):
            res[:,l,:] = np.mean(X[:,(l*self.stride):(l*self.stride+self.k_size)], axis=1)
        
        return res


    def A (self,X) :
        """
        in :
            X : (batch,length,chan_in)
        out :
            Z : (batch, (length-k_size)/stride +1,chan_in)
            maxind : (batch, (length-k_size)/stride +1,chan_in) : np.argmax pour chaque Zi
        """
        return self.forward(X)

    
    def update_parameters(self, gradient_step=1e-5):
        """
        MaxPooling n'a pas de paramètre
        """  
        pass
        

    def backward_update_gradient(self, input, delta):
        """
        MaxPooling n'a pas de paramètre
        """       
        pass

    
    def backward_delta(self, input, delta):
        ## Calcul la derivee de l'erreur
        """
        in : 
            input : (batch,length,chan_in) 
            delta : (batch,(length-k_size)/stride +1,chan_in)
            maxind : (batch, (length-k_size)/stride +1,chan_in)
        out : 
            delta : (batch,length,chan_in) delta^(h)
        
        AvgPooling n'a pas de paramètre et tous les valeur ont la meme gradient (1/k_size)
        """
        batch,length,chan_in = input.shape
        length_out = (length-self.k_size)//self.stride + 1
        
        res = np.zeros(input.shape)
        
        for n in range(batch):
            for l in range(length_out):
                for i in range(chan_in):
                    res[n,(l*self.stride):(l*self.stride+self.k_size),i] += 1/self.k_size * delta[n,l,i] # dim 1
        
        return res