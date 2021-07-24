from Parser import Parser
from IndexerSimple import IndexerSimple


print ("----------------------- TME 1 -----------------------")

collection1 = Parser.Parser_doc('./data/cacmShort-good.txt')
indexer=IndexerSimple(collection1)
indexer.indexation()

index,indexInverse = indexer.index,indexer.indexInverse
print ("index : \n",index,"\n\n")
print ("indexInverse : \n",indexInverse,"\n\n")

print ("tf-idf de document 1 : \n",indexer.getTfIDFsForDoc(1),"\n\n")
print ("tf-idf de 'terminolog' : \n",indexer.getTfIDFsForStem('terminolog'),"\n\n")


print ("affichage de document 1 :")

indexer.getStrDoc(1)






print ("\n\n\n----------------------- TME 2 -----------------------")


from Parser import Parser
from ModeleScoreSimple import ModeleScore
from IndexerSimple import IndexerSimple
import Weighter
from IRModel import *


collection1 = Parser.Parser_doc('./data/cacmShort-good.txt')
indexer=IndexerSimple(collection1)
indexer.indexation()




req = "computer terminology"

print ("requete : ", req)

modeleScore = ModeleScore(collection1,req)

print ("Modèle Simple : ")

print ("modèle booléen  : ",modeleScore.modelBool())
print ("modèle vectoriel: ",modeleScore.modelVector())

print ("modèle booléen  (utilise indexInverse): ",modeleScore.modelBool_indexInverse())


print ("\n\nWeighter (test Weighter5)")


w=Weighter.Weighter5(indexer)

print ("WeightsForQuery : \n\t",w.getWeightsForQuery(req))
print ("WeightsForDoc : \n\t",w.getWeightsForDoc(1))
print ("WeightsForStem : \n\t",w.getWeightsForStem("interne"))





print ("\n\nModèle vectoriel : \n")

v = Vectoriel(w, True)

print ("score : ",v.getScores(req))
print ("classement : ",v.getRanking(req))



print ("\n\nModèle probabiliste : \n")

w=Weighter.Weighter1(indexer)
o=Okapi(w)

print ("score : ",o.getScores(req))
print ("classement : ",o.getRanking(req))




print ("\n\nModèle de langues : \n")

w=Weighter.Weighter1(indexer)
RSV=ModeleLangue(w)

print ("score : ",RSV.getScores(req))
print ("classement : ",RSV.getRanking(req))







print ("\n\n\n----------------------- TME 3 -----------------------")
from QueryParser import *
from EvalMesure import *
from EvalIRModel import *
from GridSearch import *

req = QueryParser('./data/cacm/cacm.qry','./data/cacm/cacm.rel')
req1 = req.parseQRY()
req2 = req.parseREL()
print ("les documents pertinents de document 1 : \n",req2[1].docsPertinents)
print ("\n\nle document 1 : \n",req2[1].texte)


print ("\n\nEvalIRModel")
evalIRModel = EvalIRModel('./data/cacm/cacm')
evalIRModel.fit(weighters=[Weighter1,Weighter2],k=50)
evalIRModel.evaluation(nameModels=["Vectoriel","Okapi"],nbQuery =10)


print ("\n\nGridSearch")
gridSearch = GridSearch('./data/cacm/cacm',percent=0.75)
gridSearch.fit()
gridSearch.evaluation (nameModels=["Okapi"], nameMesures=["AP"], weighters=[Weighter1], nbQuery = 10, k = 50)







print ("\n\n\n----------------------- TME 4 -----------------------")


from PageRank import *

path = './data/cisi/cisi.txt'   

print ("path : ",path)

n = 20
k = 10
print ("n = ",n,"; k = ",k)

query = "the present time"
print ("requete : ",query,"\n")

pr = PageRank (path,model=None)
print ("PageRank top 10 : ")
print (pr.PageRank (query,n,k )[:10])