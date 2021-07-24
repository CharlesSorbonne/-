import numpy as np
import TextRepresenter as tr
pt=tr.PorterStemmer()

class IndexerSimple():
    
    def __init__(self, collection):
        self.collection = collection # dictionaire de Document()

        # index: dict{int : dict{string: int}}  (doc: mots)
        self.index = None

        # indexInverse: dict{string : dict{int: int}}  (mots: doc)
        self.indexInverse = None

        # indexInverseNormalized: dict{string : dict{int: float}}  (mots: doc)
        self.indexInverseNormalized = None

        # df: dict{string : int}  (mots: doc frequence)
        self.df = None
        
        self.tf_idf = None
        
    def indexation(self):
        #index (index va produit tous les autres, Donc on désigne comme ca pour traiter le cas où on spécifique l'index)
        if self.index is None :
            self.index = {}
            if type(self.collection) == str :
                # pour utiliser dans le cas simple et générale
                self.index[0] = pt.getTextRepresentation(self.collection)
            else :
                for doc in self.collection.values():
                    docTexte = doc.titre+" "+doc.texte
                    self.index[doc.identifiant] = pt.getTextRepresentation(docTexte)

        #index inversé pas normalisé
        self.indexInverse = {}
        for numDoc, dico in self.index.items():
            for word, tf in dico.items():
                if(word not in self.indexInverse):
                    self.indexInverse[word]= {}
                self.indexInverse[word][numDoc] = tf

        #Df
        self.df={}
        for word in self.indexInverse:
            self.df[word]=len(self.indexInverse[word])
        
        #Index inversé normalisé
        self.indexInverseNormalized = {}
        for key in self.indexInverse:
            factor = 1.0/sum(self.indexInverse[key].values())
            self.indexInverseNormalized[key] = {}
            for k in self.indexInverse[key]:
                self.indexInverseNormalized[key][k] = factor*self.indexInverse[key][k]

        #Tf-Idf
        self.tf_idf = {}
        for numDoc in self.index:
            self.tf_idf[numDoc] = {}
            for word in self.index[numDoc]:
                self.tf_idf[numDoc][word] = self.index[numDoc][word] * np.log( (1+len(self.index)) / (1+self.df[word]) )

    def getTfsForDoc(self, docId):
        return self.index[docId]

    def getTfIDFsForDoc(self, docId): 
        return self.tf_idf[docId]
    
    def getTfsForStem(self, word):
        return self.indexInverse[word]

    def getTfIDFsForStem(self, word):
        res = {}
        for numDoc in self.indexInverse[word]:
            res[numDoc] = self.tf_idf[numDoc][word]
        return res

    def getStrDoc(self, docId):
        if type(self.collection) == str :
            print (self.collection)
        else :
            print (self.collection[docId].__str__())