import numpy as np
import random

from Parser import *
from IndexerSimple import *
from IRModel import *
from Weighter import *

class PageRank (object):
    """
    permettant de calculer PageRank 
    
    """
    def __init__(self, path, model=None):
        self.path = path
        self.collection = Parser.Parser_doc(path)

        self.sort = self.getHyperlinksFrom ()
        self.entre = self.getHyperlinksTo ()

        # indexer
        self.indexer = IndexerSimple(self.collection)
        self.indexer.indexation()

        # model 
        if model is None :
            self.model = Vectoriel(Weighter2(self.indexer),True)
        else :
            self.model = model


    def getHyperlinksFrom (self):
        """
        sortie :
            dictionaire : {document D: les documents pointant par D}
        """
        sort = {}
        for doc in self.collection :
            sort[doc] = np.int0(np.unique(self.collection[doc].liens))
        return sort
    

    def getHyperlinksTo (self) :
        """
        sortie :
            dictionaire : {document D: les documents pointant vers D}
        """
        entre = {}
        for doc in self.collection :
            entre[doc] = []
        for doc in self.collection :
            for direction in np.int0(np.unique(self.collection[doc].liens)) :
                entre[direction].append(doc)
        return dict(sorted(entre.items(), key=lambda item: item[0]))


    def generateVQ (self,query,n,k) :
        """
        génerateur de VQ

        entrée :
            query : string
            n : déterminant le nombre de documents seeds à considérer
            k : déterminant le nombre de liens entrants à considérer pour chaque document seed
        
        sortie :
            liste[int] : liste de documents de ce composant (VQ)
        """
        self.ranking = self.model.getRanking(query)
        self.ranking = self.ranking [:min(n,len(self.ranking))]
        VQ = self.ranking.copy()
        for seed in self.ranking :
            # on choisi tous les documents pointant par D
            VQ += list(self.sort[seed])

            if len(self.entre[seed]) > k:
                # on choisi k documents pointant vers D aléatoire
                VQ += random.sample(self.entre[seed], k)
            else :
                # on choisi tous les documents pointant vers D
                VQ += self.entre[seed]
        return np.unique(VQ)


    def generateGQ (self,query,n,k) :
        """
        génerateur de sous graphe GQ

        entrée :
            query : string
            n : déterminant le nombre de documents seeds à considérer
            k : déterminant le nombre de liens entrants à considérer pour chaque document seed
        
        sortie :
            liste[int] : liste de documents de ce composant (VQ)
        """
        VQ = self.generateVQ (query,n,k)
        
        resSort = {}
        resEntre = {}
        for doc in VQ :
            resSort[doc] = [i for i in self.sort[doc] if i in VQ]
            resEntre[doc] = [i for i in self.entre[doc] if i in VQ]
        return resSort,resEntre,VQ
    

    def PageRank (self,query,n,k,d=0.8,maxite=500,eps=1e-5) :
        """
        calculer PageRank : on défini aj = 1/len(VQ) uniforme

        entrée :
            query : string
            n : déterminant le nombre de documents seeds à considérer
            k : déterminant le nombre de liens entrants à considérer pour chaque document seed
            d : le facteur d’amortissement 

        sortie :
            liste[int] : liste de documents tirée par PageRank
        """
        sort,entre,VQ = self.generateGQ (query,n,k)

        # initialiser par uniforme
        PR = dict.fromkeys( VQ, 1/len(VQ))

        for i in range (maxite):
            old = list(PR.values())
            tmp = []
            # itération : tmp = PR^t
            for doc in VQ :
                # Remarque len(index) = len(docs)
                tmp.append ((d* sum ([PR[doc_entre]/len(sort[doc_entre]) for doc_entre in entre[doc]] ) + (1-d)/len(VQ)))
            # renouveller PR
            for do in range(len(tmp)) :
                PR[VQ[do]] = tmp[do]/np.sum(tmp)
            # ici old = PR^(t-1) ; PR = PR^t
            if np.max(np.abs((list(PR.values()) - np.array(old)))) < eps :
                break
        print ("converge en " , i ," iteration")
        PR = list(dict(sorted(PR.items(), key=lambda item: item[1],reverse=True)).keys())
        return PR