import numpy as np


class EvalMesure():
    
    def __init__(self,k=10,query = None):
        self.query = query 
        self.k = k
        
    def evalQuery(self,scores):
        """
        Le score de chaque document
        
        entrée :
            scores[int]: une liste de idDOC retourné par le modele
        
        sortie :
            float
        """
        pass



class Precision(EvalMesure):
    """
    Le mesure Precision
    
    Precision = tp / (tp + fp) = nb(doc pertinent) / k
    """
    def __init__(self,k=10,query = None):
        super().__init__(k,query)
        
    def evalQuery(self, scores):
        return np.mean([(numDoc in self.query.docsPertinents) for numDoc in scores[:self.k]])



class Rappel(EvalMesure):
    """
    Le mesure Rappel
    
    Rappel = tp / (tp + fn) = nb(doc pertinent) / nb(doc pertinent total)
    """
    
    def __init__(self,k=10,query = None):
        super().__init__(k,query)
        
    def evalQuery(self, scores):
        if len(self.query.docsPertinents) == 0 :
            return 0
        return np.sum([(numDoc in self.query.docsPertinents) for numDoc in scores[:self.k]])/len(self.query.docsPertinents)



class F_mesure(EvalMesure):
    """
    Le F-mesure
    
    F-mesure = (1 + beta^2) * Precision * Rappel / (beta^2 * Precision + Rappel)
    """
    def __init__(self, k=10,query = None,beta = 1):
        super().__init__(k,query)
        self.beta = beta

    def evalQuery(self, scores):
        R = Rappel(self.k,self.query).evalQuery(scores)
        P = Precision(self.k,self.query).evalQuery(scores)
        
        if (self.beta**2 * P + R) ==0:
            return 0
        return (1+self.beta**2)*P*R/(self.beta**2*P+R)



class NDCG(EvalMesure):
    """
    Le mesure NDCG
    
    NDCG = DCG / iDCG
    
    k ne change rien
    """
    def __init__(self,k=10,query = None):
        super().__init__(k,query)
        
    def evalQuery(self, scores):
        # la pertinence graduée des documents dans scores
        rel = [1 if d in self.query.docsPertinents else 0 for d in scores]
        
        nbRel = len(self.query.docsPertinents)
        self.k = min(nbRel,self.k)
        
        sorted_rel = sorted(rel,reverse=True)
        # denominateur de chaque terme
        metrique = np.concatenate(([1],np.log([2+i for i in range(self.k-1)])))
        
        dcg = np.sum(rel[:self.k]/metrique)
        idcg = np.sum(sorted_rel[:self.k]/metrique)
        
        if idcg == 0:
            return 0
        else:
            return dcg/idcg



class AP(EvalMesure):
    """
    Le mesure Avg precision
    
    AP = moyenne de précision pour chaque rang i <= k
    
    k ne change rien
    """
    def __init__(self,k=10,query = None):
        super().__init__(k,query)
        
    def evalQuery(self, scores):
        nbPertinent = 0
        res = 0
        for rang,numDoc in enumerate(scores) :
            if numDoc in self.query.docsPertinents :
                nbPertinent += 1
                res += nbPertinent/(rang+1)
        if nbPertinent == 0 :
            return 0
        return res/nbPertinent



class RR(EvalMesure):
    """
    Le mesure reciprocal rank
    
    reciprocal rank = 1/rang(h) avec h appartient docsPertinents
    
    k ne change rien
    """
    
    def __init__(self,k=10,query = None):
        super().__init__(k,query)
        
    def evalQuery(self, scores):
        for rang,numDoc in enumerate(scores) :
            if numDoc in self.query.docsPertinents :
                return 1/(rang+1)
        return 0
