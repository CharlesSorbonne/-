import numpy as np
import TextRepresenter as tr
pt=tr.PorterStemmer()

class Weighter():
    """
    Classe abstraite représentant une pondération
    """
    def __init__(self, indexerSimple):
        # index: dict{int : dict{string: int}}  (doc: mots)
        self.index = indexerSimple.index
        # indexInverse: dict{string : dict{int: int}}  (mots: doc)
        self.indexInverse = indexerSimple.indexInverse
        self.idf = {}
        self.normDoc = {}
        
    def getIdf(self, stem):
        """
        L'idf (index inverse frequency) d'une terme
        
        entrée :
            stem: string (Le terme dont l'idf doit être calculé)

        sortie :
            float
            (idf: {string : float} (mots : idf))
        """
        if(stem not in self.idf):
            if(stem not in self.indexInverse):
                df = 0
            else:
                df = len(self.indexInverse[stem])
            self.idf[stem] = np.log((1+len(self.index)) / (1+df))
        return self.idf[stem]
    
    def getWeightsForDoc(self, idDoc):
        """
        Les poids des termes du document indiqué
        
        entrée : 
            idDoc: int (L'id du document)

        sortie :
            dict{string: int ou float}  (mots : weight)
        """
        pass
    
    def getWeightsForStem(self, stem):
        """
        Les poids du terme indiqué dans chaque document
        
        entrée : 
            stem: string (Le terme)
        
        sortie : 
            dict{int: int ou float}  (doc : weight)
        """
        pass
    
    def getWeightsForQuery(self, query):
        """
        Les poids des termes de la requete indiqué
        
        entrée :
            query: string (La requete)

        sortie :
            dict{string: int ou float}  (mots : weight)
        """
        pass
    
    def getNormDoc(self, docId):
        """
        >> Pour utilisée dans le modèle vectoriel
        La norme d'un document vectorisé (car il y a plusieur requete, on enregiste les resultats dans self.normDoc)
        
        entrée : 
            idDoc: int (L'id du document)
        
        sortie :
            float (La norme du document vectorisé)
            il y a plusieur doc donc on enregistrer tous les norme dans une dictionaire
        """
        if(docId not in self.normDoc):
            #le poids de chaque terme du document indiqué
            docWeights = self.getWeightsForDoc(docId)
            #calculer norme
            self.normDoc[docId] = np.linalg.norm(list(docWeights.values()))
        return self.normDoc[docId]
    
    def getNormQuery(self, query):
        """
        >> Pour utilisée dans le modèle vectoriel
        La norme d'une requete vectorisée
        
        entrée : 
            query: string (La requete)
        
        sortie :
            float (La norme de la requete vectorisé)
            il y a une seule norme pour un requete
        """
        reqWeights = self.getWeightsForQuery(query)
        return np.linalg.norm(list(reqWeights.values()))

class Weighter1(Weighter):
    def getWeightsForDoc(self, idDoc):
        return self.index[idDoc] 
    
    def getWeightsForStem(self, stem):
        tmp = list(pt.getTextRepresentation(stem).keys())
        if len(tmp) < 1 :
            return {}
        else :
            stem = list(pt.getTextRepresentation(stem).keys())[0]
        return self.indexInverse[stem] if stem in self.indexInverse else {}
    
    def getWeightsForQuery(self, query):
        tmp = pt.getTextRepresentation (query)
        return dict(zip(tmp.keys(),(np.array(list(tmp.values()))>0)*1))

class Weighter2(Weighter):
    def getWeightsForDoc(self, idDoc):
        return self.index[idDoc] 
    
    def getWeightsForStem(self, stem):
        tmp = list(pt.getTextRepresentation(stem).keys())
        if len(tmp) < 1 :
            return {}
        else :
            stem = list(pt.getTextRepresentation(stem).keys())[0]
        return self.indexInverse[stem] if stem in self.indexInverse else {}
    
    def getWeightsForQuery(self, query):
        return pt.getTextRepresentation (query)

class Weighter3(Weighter):
    def getWeightsForDoc(self, idDoc):
        return self.index[idDoc]
    
    def getWeightsForStem(self, stem):
        tmp = list(pt.getTextRepresentation(stem).keys())
        if len(tmp) < 1 :
            return {}
        else :
            stem = list(pt.getTextRepresentation(stem).keys())[0]
        return self.indexInverse[stem] if stem in self.indexInverse else {}
    
    def getWeightsForQuery(self, query):
        req=list(pt.getTextRepresentation(query).keys())
        res={}
        for stem in req:
            res[stem] = self.getIdf(stem)
        return res

class Weighter4(Weighter):
    def getWeightsForDoc(self, idDoc):
        res={}
        for stem in self.index[idDoc]:
            res[stem] = 1+np.log(self.index[idDoc][stem])
            # index[idDoc][stem] forcement > 0
        return res
    
    def getWeightsForStem(self, stem):
        tmp = list(pt.getTextRepresentation(stem).keys())
        if len(tmp) < 1 :
            return {}
        else :
            stem = list(pt.getTextRepresentation(stem).keys())[0]

        res={}
        if stem in self.indexInverse:
            for doc in self.indexInverse[stem]:
                res[doc] = 1+np.log(self.indexInverse[stem][doc])
        return res
    
    def getWeightsForQuery(self, query):
        req=list(pt.getTextRepresentation(query).keys())
        res={}
        for stem in req:
            res[stem] = self.getIdf(stem)
        return res

class Weighter5(Weighter):
    def getWeightsForDoc(self, idDoc):
        res = {}
        for stem in self.index[idDoc]:
            idf = self.getIdf(stem)
            res[stem] = (1+np.log(self.index[idDoc][stem])) * idf
            # index[idDoc][stem] forcement > 0
        return res
    
    def getWeightsForStem(self, stem):
        tmp = list(pt.getTextRepresentation(stem).keys())
        if len(tmp) < 1 :
            return {}
        else :
            stem = list(pt.getTextRepresentation(stem).keys())[0]
        
        res={}
        if stem in self.indexInverse:
            idf = self.getIdf(stem)
            for doc in self.indexInverse[stem]:
                res[doc] = (1+np.log(self.indexInverse[stem][doc])) * idf
                # index[idDoc][stem] forcement > 0
        return res
    
    def getWeightsForQuery(self, query):
        tfs=pt.getTextRepresentation(query)
        res={}
        for stem in tfs:
            idf = self.getIdf(stem)
            res[stem] = (1+np.log(tfs[stem]))*idf
            # tfs[stem] forcement > 0
        return res