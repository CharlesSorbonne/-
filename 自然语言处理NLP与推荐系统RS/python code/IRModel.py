import numpy as np
import TextRepresenter as tr
pt=tr.PorterStemmer()

class IRModel():
    """
    Modèle de score
    """
    def __init__(self, weighter):
        """
        weighter: Weighter (Instance d'une classe Weighter)
        """
        self.weighter = weighter
    
    def getScores(self, query):
        """
        Le score de chaque document
        
        entrée :
            query: string (La requete)
        
        sortie :
            dict{int : int ou float} (doc : score)
        """
        pass
    
    def getRanking(self, query):
        """
        Classement de document par score pertinence
        
        entrées :
            query: string (La requete)
        
        sortie :
            list[int] (liste des identifiants des documents triés par ordre décroissant de pertinence)
        """
        scores = self.getScores(query)
        scores = sorted(scores.items(), reverse=True, key=lambda x: x[1])
        return list(dict(scores).keys())


class Vectoriel(IRModel):
    """
    Le modèle vectoriel
    """
    def __init__(self, weighter, normalized = True):
        """
        normalized: Booleen indique si on calcule le modèle vectoriel normalisé
        """
        super().__init__(weighter)
        self.normalized = normalized
        
    def getScores(self, query):
        if(self.normalized == True):
            # le modèle vectoriel normalisé
            return self.getScoresNormalized(query)
        else:
            # le modèle vectoriel non normalisé
            return self.getScoresNotNormalized(query)

    def getScoresNotNormalized(self, query):
        """
        Le produit scalaire entre les représentations vectorielles des documents et la requete
        
        entrées :
            query: string (La requete)

        sortie :
            dict{int : int ou float} (doc : score)
        """
        reqWeights = self.weighter.getWeightsForQuery(query) 
        res={}
        # on considère que le poids d'un terme n'appartenant pas à la requete sera toujours nul
        # chaque terme de la requete
        for stem,weightStem in reqWeights.items():
            # on cherche les poids de ce terme dans chaque document
            docWeights = self.weighter.getWeightsForStem(stem)
            # chaque document contenant le terme
            for docId,weightDoc in docWeights.items():
                if(docId not in res):
                    # si la clé n'existe pas
                    res[docId] = weightStem*weightDoc
                else:
                    res[docId] += weightStem*weightDoc
        return res
    
    def getScoresNormalized(self, query):
        """
        Le score cosinus (modèle vectoriel non normalisé)
        
        entrées :
            query: string (La requete)

        sortie :
            dict{int : int ou float} (doc : score)
        """
        prodScalaires = self.getScoresNotNormalized(query)
        res={}
        for docId,produire in prodScalaires.items():
            res[docId] = produire/(self.weighter.getNormDoc(docId)*self.weighter.getNormQuery(query))
        return res


class Okapi(IRModel):
    """
    Modèle Okapi

    souvent on utilisera Weighter1
    """
    def __init__(self, weighter, k1=1.2, b=0.75):
        super().__init__(weighter)
        #paramètre du modèle
        self.k1 = k1
        self.b = b

    def getScores(self, query):
        res={}

        # extraiter stem pour la requete
        stems = list(pt.getTextRepresentation(query).keys())

        #longueur moyenne des documents : avgdl
        self.avgdl=np.mean([sum(list(indexDict.values())) for idDoc,indexDict in self.weighter.index.items()])
        
        #Pour chaque terme de la requete
        for stem in stems:
            idf = self.weighter.getIdf(stem)
            
            #Les poids du terme dans chaque document
            docWeights = self.weighter.getWeightsForStem(stem) 
            for idDoc, weight in docWeights.items():
                # weight := tf(qi,D)
                # lenDoc := |D|
                lenDoc = sum(self.weighter.index[idDoc].values()) 

                score = idf * weight * (self.k1+1) / (weight + self.k1 * (1 - self.b + self.b*lenDoc/self.avgdl) ) 
                if(idDoc not in res):
                    res[idDoc] = score
                else:
                    res[idDoc] += score
        return res


class ModeleLangue(IRModel):
    """
    Modèle Jelinek-Mercer

    souvent on utilisera Weighter1
    """
    def __init__(self, weighter, lambd=0.8):
        super().__init__(weighter)
        self.lambd = lambd

    def getScores(self, query):
        stems = list(pt.getTextRepresentation(query).keys())
        
        scores = {}
        for idDoc in self.weighter.index.keys():
            # supprimer les documents qui ne contiennent aucun des termes de la requêtes
            if set(stems).intersection(self.weighter.index[idDoc].keys()):
                scores[idDoc] = self.getQueryScore(idDoc, stems)
        return scores
        
    
    def getQueryScore(self, idDoc, stems):
        """ 
        Le score par un document et pour les termes de requete

        entrée :
            idDoc: int (L'id du document)
            stems: liste[str] (liste des stems de query)

        sortie :
            queryScore: float 
        """
        # probaC : P(t|Mc) probabilité de t apparaît dans la collection des document
        # probaStemCollection: dict{string : float}  (mots : proba)
        probaStemCollection = {}
        lenDocs = sum([sum(indexDict.values()) for indexDict in self.weighter.indexInverse.values()])
        for stem in stems:
            if stem not in self.weighter.indexInverse:
                # le terme n'existe pas dans les document (il ne peut pas trouver dans indexInverse)
                probaStemCollection[stem] = 0
                continue
            probaStemCollection[stem] = sum(self.weighter.indexInverse[stem].values())/lenDocs

        # calcule score
        queryScore = 1
        for stem, probaC in probaStemCollection.items():
            # probaD : P(t|Md) probabilité de t apparaît dans le document indiqué
            if stem not in self.weighter.index[idDoc]:
                probaD = 0
            else: 
                probaD = self.weighter.index[idDoc][stem]/sum(self.weighter.index[idDoc].values()) 
            
            queryScore *= self.lambd*probaD + (1-self.lambd)*probaC
        return queryScore