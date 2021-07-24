from Parser import *
from IndexerSimple import *
from QueryParser import *
from EvalIRModel import *


class GridSearch ():
    """
    permettant l'évaluation de différents paramètres de un modèle de recherche sur un ensemble de requetes selon un mesure d'évaluation
    
    """

    def __init__(self, path, percent=0.85, GridSize=3, GridStep=0.1):
        # type string : cacm ou cisi
        self.path = path 

        # pourcentage pour fait une cross validation
        self.percent = percent

        self.GridSearch = GridSearch

        self.GridSize = GridSize

        self.GridStep = GridStep


    def fit (self):
        """
        sortie :
            indexerTrain : type IndexerSimple
            querysTrain : type dictionnaire de Query (identifiant,texte,docsPertinents)
            indexerTest : type IndexerSimple
            querysTest : type dictionnaire de Query (identifiant,texte,docsPertinents)
        """
        ###############
        ### indexer ###
        ###############
        collection = Parser.Parser_doc(self.path+'.txt')
        indexer = IndexerSimple(collection)
        indexer.indexation()
        # index: dict{int : dict{string: int}}  (doc: mots)
        indexAll = indexer.index

        # initialiser indexerTrain et indexerTest
        self.indexerTrain = IndexerSimple(collection)
        self.indexerTrain.index = {}
        self.indexerTest = IndexerSimple(collection)
        self.indexerTest.index = {}

        self.TrainNumDoc = list(indexAll.keys())[:int(self.percent*len(indexAll))]
        self.TestNumDoc = list(indexAll.keys())[int(self.percent*len(indexAll)):]
        for numDoc, dico in indexAll.items():
            if numDoc in self.TestNumDoc :
                self.indexerTest.index[numDoc] = dico
            else :
                self.indexerTrain.index[numDoc] = dico

        self.indexerTest.indexation()
        self.indexerTrain.indexation()


        ##############
        ### querys ###
        ##############
        reqPath = self.path+'.qry'
        relPath = self.path+'.rel'
        req = QueryParser(reqPath,relPath)
        req.parseREL()
        # type dictionnaire de Query (identifiant,texte,docsPertinents)
        querysAll = req.reqs
        
        self.querysTrain = {}
        self.querysTest = {}

        for numQuery,query in querysAll.items():
            queryTest = Query(numQuery)
            queryTest.texte = query.texte

            queryTrain = Query(numQuery)
            queryTrain.texte = query.texte

            for docPertinent in query.docsPertinents :
                if docPertinent in self.TestNumDoc:
                    queryTest.addDocspertinents(docPertinent)
                else :
                    queryTrain.addDocspertinents(docPertinent)

            self.querysTrain[numQuery] = queryTrain
            self.querysTest[numQuery] = queryTest


    def evaluation (self, nameModels=["ModeleLangue","Okapi"], nameMesures=["F_mesure"], weighters=[Weighter1], nbQuery=10, k=1000):
        # pour GridSearch, on just utilise un seul mesure pour evaluer
        evalIRModelTrain = EvalIRModel(self.path)
        evalIRModelTrain.indexer = self.indexerTrain
        evalIRModelTrain.querys = self.querysTrain
        evalIRModelTrain.fit(weighters=weighters, k=k)

        evalIRModelTest = EvalIRModel(self.path)
        evalIRModelTest.indexer = self.indexerTest
        evalIRModelTest.querys = self.querysTest
        evalIRModelTest.fit(weighters=weighters, k=k)

        
        testRange = np.arange(0,self.GridSize,1)*self.GridStep-self.GridStep*(self.GridSize//2)
        for nameModel in nameModels :
            if nameModel == "ModeleLangue" :
                res = []
                lambdList = 0.8 + testRange

                for lambd in lambdList :
                    evalIRModelTrain.models[nameModel][0].lambd = lambd
                    tmp = evalIRModelTrain.evaluation(nameModels=[nameModel],nameMesures=[nameMesures[0]],nbQuery=nbQuery,visual=False)
                    # le premier resultat (on compare la moyenne d'abord et écart-type après)
                    res.append (list(tmp.values())[0][0])

                lambdOptimal = lambdList[np.argmax(res)]
                print (nameModel," : lambda optimal = ",lambdOptimal," \n\tmean(Train) = ",max(res))
                print ("--- Test ---")
                evalIRModelTest.models[nameModel][0].lambd = lambdOptimal
                return evalIRModelTest.evaluation(nameModels=[nameModel],nameMesures=[nameMesures[0]],nbQuery=nbQuery,visual=True)

            if nameModel == "Okapi" :
                res = []

                k1List = 1.2 + testRange
                bList = 0.75 + testRange

                parameterList = [(k1,b) for k1 in k1List for b in bList]
                
                for k1,b in parameterList :
                    evalIRModelTrain.models[nameModel][0].k1 = k1
                    evalIRModelTrain.models[nameModel][0].b = b
                    tmp = evalIRModelTrain.evaluation(nameModels=[nameModel],nameMesures=[nameMesures[0]],nbQuery=nbQuery,visual=False)
                    res.append (list(tmp.values())[0][0])
                
                parameterOptimal =  parameterList[np.argmax(res)]
                print (nameModel," : parametre optimal = ",parameterOptimal," \n\tmean(Train) = ",max(res))
                print ("--- Test ---")
                evalIRModelTest.models[nameModel][0].k1 = parameterOptimal[0]
                evalIRModelTest.models[nameModel][0].b = parameterOptimal[1]
                return evalIRModelTest.evaluation(nameModels=[nameModel],nameMesures=[nameMesures[0]],nbQuery=nbQuery,visual=True)