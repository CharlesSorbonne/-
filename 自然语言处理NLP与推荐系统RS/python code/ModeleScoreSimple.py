import TextRepresenter as tr
pt=tr.PorterStemmer()
from IndexerSimple import IndexerSimple
import numpy as np


class ModeleScore():

    def __init__(self, collection, query):
        self.collection = collection # dictionaire de Document()
        indexer = IndexerSimple(collection)
        indexer.indexation()
        self.index = indexer.index
        self.indexInverse = indexer.indexInverse
        self.req = pt.getTextRepresentation(query)
        indexerQuery = IndexerSimple(query)
        indexerQuery.indexation()
        self.reqIndex = indexerQuery.index[0]

    def modelBool (self):
        res = []
        for idDoc,doc in self.index.items() :
            check = True
            motsDoc = list(doc.keys())
            for mots in self.req :
                if mots not in motsDoc :
                    check = False
                    break
            if check : 
                res.append((idDoc,1))
        return dict(res)

    def modelBool_indexInverse (self):
        inters=set(self.index)
        for stem in self.reqIndex:
            inters=inters.intersection(self.indexInverse[stem])
            #On récupère l'intersection des documents contenant un mot de la requete
        res = {}
        for d in inters :
            res[d] = 1
        return res
    
    def modelVector (self):
        res = []
        list_doc = []
        for idDoc,doc in self.index.items() :
            somme = 0
            motsDoc = list(doc.keys())
            for mots in self.req :
                if mots in motsDoc :
                    somme += self.index[idDoc][mots]*self.reqIndex[mots]
            if somme != 0 :
                list_doc.append (idDoc)
                res.append(somme)
        res = dict(zip(list_doc,res))
        return res