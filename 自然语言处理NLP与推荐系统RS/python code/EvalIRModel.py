import numpy as np
from Weighter import *
from IRModel import *
from Parser import *
from IndexerSimple import *
from QueryParser import *
from EvalMesure import *


class EvalIRModel():
    """
    permettant l'évaluation de différents modèles de recherche sur un ensemble de requetes selon différentes mesures d'évaluation
    
    Les résultats devront etre résumés pour l'ensemble des requetes considérées en présentant la moyenne et l'écart-type pour chaque modèle.
    
    """
    def __init__(self, path):
        # type string : cacm ou cisi
        self.path = path
        
        # type IndexerSimple
        self.indexer = None
        
        # type dictionnaire de Query (identifiant,texte,docsPertinents)
        self.querys = None
        
        # type liste de Weight
        self.weighters = []
        
        # type dictionaire de (liste de IRModel)
        self.models = {}
        
        # type dictionaire de EvalMesure
        self.mesures = {}
        
    
    def fit (self, weighters=[Weighter1,Weighter2,Weighter3,Weighter4,Weighter5], k = 1000): 
        """
        permettant de charger tous les paramètres
        """
        ###############
        ### indexer ###
        ###############
        if self.indexer is None:
            collection = Parser.Parser_doc(self.path+'.txt')
            indexer = IndexerSimple(collection)
            indexer.indexation()
            self.indexer = indexer
            self.index, self.indexInverse = indexer.index, indexer.indexInverse
        
        
        ##############
        ### querys ###
        ##############
        if self.querys is None:
            reqPath = self.path+'.qry'
            relPath = self.path+'.rel'
            req = QueryParser(reqPath,relPath)
            req.parseREL()
            self.querys = req.reqs
        
        
        #################
        ### weighters ###
        #################
        for weighter in weighters:
            w = weighter(self.indexer)
            self.weighters.append(w)
        
        
        ##############
        ### models ###
        ##############
        #vectoriel
        self.models["Vectoriel"] = []
        for weighter in self.weighters:
            self.models["Vectoriel"].append(Vectoriel(weighter,True))
            
        #ModeleLangue
        self.models["ModeleLangue"] = [ModeleLangue(Weighter1(self.indexer), lambd=0.8)]

        #Okapi
        self.models["Okapi"] = [Okapi(Weighter1(self.indexer), k1=1.2, b=0.75)]
        
        
        ###############
        ### mesures ###
        ###############
        # on initialiser tous les mesure a un query None, on va le définir après
        self.mesures["Precision"] = Precision(k)
        self.mesures["Rappel"] = Rappel(k)
        self.mesures["F_mesure"] = F_mesure(k)
        self.mesures["AP"] = AP()
        self.mesures["NDCG"] = NDCG()
        self.mesures["RR"] = RR()
        
        
    def evaluationModelMesure(self, model, mesure, nbQuery = 10):
        """
        permettant de evaluer par rapport un modèle et un mesure
        
        entrée :
            model : type IRModel
            mesure : type EvalMesure
        
        sortie :
            res : liste de float (evaluation pour chaque query à partir de un modèle et un mesure) 
        """
        res = []
        for query in list(self.querys.values())[:nbQuery] :
            ranking = model.getRanking(query.texte)
            mesure.query = query
            res.append(mesure.evalQuery(ranking))
        return res
    
    def evaluation (self, nameModels=["Vectoriel","ModeleLangue","Okapi"], 
                    nameMesures=["Precision","Rappel","F_mesure","AP","NDCG","RR"], nbQuery = 10, visual=True):
        
        res = {}

        for nameModel in nameModels :
            listeModel = self.models[nameModel]
            if visual :
                print(nameModel, " :")
            for numModel,model in enumerate(listeModel) :
                for nameMesure in nameMesures :
                    mesure = self.mesures[nameMesure]
                    evals = self.evaluationModelMesure(model,mesure,nbQuery=nbQuery)
                    if visual :
                        if (nameMesure == "AP"):
                            print ("\tWeight ",(numModel+1),"; mesure ",nameMesure,"\n\t\tmean (MAP): ", np.mean(evals), "std: ", np.std(evals))
                        elif (nameMesure == "RR"):
                            print ("\tWeight ",(numModel+1),"; mesure ",nameMesure,"\n\t\tmean (MRR): ", np.mean(evals), "std: ", np.std(evals))
                        else :
                            print ("\tWeight ",(numModel+1),"; mesure ",nameMesure,"\n\t\tmean: ", np.mean(evals), "std: ", np.std(evals))
                    res[nameModel+'-'+nameMesure+"-W"+str(numModel+1)] = (np.mean(evals),np.std(evals))
        
        return res