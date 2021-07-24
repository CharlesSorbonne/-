# **TME 1 Indexation**

## **Explication :** 

$\verb|Document.py|$ : définir la classe $\verb|Document|$ (la classe enregistre les données des documents), on va l'utiliser dans la classe $\verb|Parser|$ <br/>

$\verb|Parser.py|$ : définir la classe $\verb|Parser|$ (la classe lit tous les documents enregistré dans un fichier)<br/>

$\verb|IndexerSimple.py|$ : définir la classe $\verb|IndexerSimple|$ (la classe calcule les indexs d'après un collection de type dictionnaire de la classe $\verb|Document|$)

# **--- TEST ---**


```python
from Parser import Parser
from IndexerSimple import IndexerSimple
collection1 = Parser.Parser_doc('./data/cacmShort-good.txt')
indexer=IndexerSimple(collection1)
indexer.indexation()
```

### **index et index inverse**
on remaque que $\verb|nbDocument==len(index)|$


```python
index,indexInverse = indexer.index,indexer.indexInverse
```

### **tf-idf par doc**


```python
indexer.getTfIDFsForDoc(1)
```

résultat :
```
    {'preliminari': 1.791759469228055,
     'report': 1.791759469228055,
     'intern': 1.791759469228055,
     'algebra': 1.791759469228055,
     'languagejgkfldjgfkld': 1.791759469228055}
```


### **tf-idf par stem**

```python
indexer.getTfIDFsForStem('terminolog')
```

résultat :
```
    {4: 1.0986122886681098, 7: 1.0986122886681098, 10: 1.0986122886681098}
```



### **affichage**


```python
indexer.getStrDoc(1)
```

résultat :
```
    -----------------------------
    Identifiant : 1
    Titre : Preliminary Report-International Algebraic Languagejgkfldjgfkld
    Auteurs : 
    	Perlis A. J.
    	Samelson K.
    Nombre de liens : 34
    -----------------------------
```
    

# **TME 2 Appariement**

## **Explication :**

$\verb|ModeleScoreSimple.py|$ : définir la classe $\verb|ModeleScore|$ (la classe calcule modèle booléen et modèle vectoriel simplement et one ne l'utilise jamais) <br/>

$\verb|Weighter.py|$ : définir la classe $\verb|Weighter|$ et $\verb|Weighter1-5|$ (la classe calcule les pondérations pour le modèle vectoriel)<br/>

$\verb|IRModel.py|$ : définir la classe $\verb|IRModel|$ (abstrait) et 
> $\verb|Vectoriel|$<br/>
> $\verb|Okapi|$ <br/>
> $\verb|ModeleLangue|$

(la classe calcule la score d'après un paramètre de type $\verb|Weighter|$ (on peut utilise index dans $\verb|Weighter|$) )

# **--- TEST ---**

### **Modèle Simple**


```python
from ModeleScoreSimple import ModeleScore
req = "computer terminology"
```


```python
modeleScore = ModeleScore(collection1,req)

print ("modèle booléen  : ",modeleScore.modelBool())
print ("modèle vectoriel: ",modeleScore.modelVector())
print ("modèle booléen  (utilise indexInverse): ",modeleScore.modelBool_indexInverse())
```

résultat :
```
    modèle booléen  :  {4: 1, 7: 1, 10: 1}
    modele vectoriel:  {2: 1, 4: 2, 6: 1, 7: 2, 10: 2}
    modèle booléen  (utilise indexInverse):  {10: 1, 4: 1, 7: 1}
```

### **Weight**

Notation : <br/>
- $w_{t,d}$ est le poids d'un terme $t$ dans un document $d$ et $w_{t,q}$ le poids d'un terme $t$ dans une requete $q$.<br/>
- $tf_{t,d}$ (resp. $tf_{t,q}$) correspond au *term frequency* du terme $t$  dans le document $d$ (resp. la requete $q$).<br/>
- $idf_t$ correspond à l'*inverse document frequency* du terme $t$ dans l'ensemble de la collection/du corpus considéré<br/>

$\verb|weight1|$ : $w_{t,d} = tf_{t,d}$ et $w_{t,q} = 1$ si $t \in q$ <br/>
$\verb|weight2|$ : $w_{t,d} = tf_{t,d}$ et $w_{t,q} = tf_{t,q}$ si $t \in q$<br/>
$\verb|weight3|$ : $w_{t,d} = tf_{t,d}$ et $w_{t,q} = idf_t$ si $t \in q$<br/>
$\verb|weight4|$ : $w_{t,d} = 1 + ln(tf_{t,d})$ et $w_{t,q} = idf_t$ si $t \in q$<br/>
$\verb|weight4|$ : $w_{t,d} = (1 + ln(tf_{t,d})) \times idf_t$ et $w_{t,q} = (1 + ln(tf_{t,q})) \times idf_t$ si $t \in q$<br/>


```python
import Weighter

w=Weighter.Weighter5(indexer)

print ("WeightsForQuery : \n\t",w.getWeightsForQuery(req))
print ("WeightsForDoc : \n\t",w.getWeightsForDoc(1))
print ("WeightsForStem : \n\t",w.getWeightsForStem("interne"))
```

résultat :
```
    WeightsForQuery : 
    	 {'comput': 0.6931471805599453, 'terminolog': 1.0986122886681098}
    WeightsForDoc : 
    	 {'preliminari': 1.791759469228055, 'report': 1.791759469228055, 'intern': 1.791759469228055, 'algebra': 1.791759469228055, 'languagejgkfldjgfkld': 1.791759469228055}
    WeightsForStem : 
    	 {1: 1.791759469228055}
```


### **Modèle vectoriel**

#### **Remarque : (modele vectoriel)**

Le poids d'un terme n'appartenant pas à la requete sera toujours nul. <br/>

Donc, le produit scalaire entre le vecteur de la requete et un vecteur de document ne prendra pas en compte les termes ne se trouvant pas dans la requete (multiplication par 0).<br/>

Ainsi, on ne retournera pas les documents ayant un score nul (rapidité d'execution). La norme de chaque vecteur sera calculée la première fois que cela est nécessaire et sera gardée en mémoire pour la suite.<br/>


```python
from IRModel import *

v=Vectoriel(w, True)

print ("score : ",v.getScores(req))
print ("classement : ",v.getRanking(req))
```

résultat :
```
    score :  {2: 0.09473140616367136, 4: 0.588769560363494, 6: 0.14079185956679588, 7: 0.588769560363494, 10: 0.588769560363494}
    classement :  [4, 7, 10, 6, 2]
```

### **Modèle probabiliste**


```python
w=Weighter.Weighter1(indexer)
o=Okapi(w)

print ("score : ",o.getScores(req))
print ("classement : ",o.getRanking(req))
```

résultat :
```
    score :  {2: 0.6187041659413354, 4: 1.7360571023090483, 6: 0.8101157672794361, 7: 1.7360571023090483, 10: 1.7360571023090483}
    classement :  [4, 7, 10, 6, 2]
```

### **Modèle de langues**


```python
w=Weighter.Weighter1(indexer)
RSV=ModeleLangue(w)

print ("score : ",RSV.getScores(req))
print ("classement : ",RSV.getRanking(req))
```

résultat :
```
    score :  {2: 0.0017993079584775079, 4: 0.030850288350634376, 6: 0.0033679354094578997, 7: 0.030850288350634376, 10: 0.030850288350634376}
    classement :  [4, 7, 10, 6, 2]
```


# **TME 3**

## **Explication :**

$\verb|Query.py|$ : définir la classe $\verb|Query|$ (la classe enregistre les données des requetes), on va l'utiliser dans la classe $\verb|QueryParser|$ (très proche que $\verb|Document|$)<br/>

$\verb|QueryParser.py|$ : définir la classe $\verb|QueryParser|$ (la classe lit tous les requetes enregistré dans un fichier) (très proche que $\verb|Parser|$)<br/>

$\verb|EvalMesure.py|$ : définir la classe $\verb|EvalMesure|$ (abstrait) et 
> $\verb|Precision|$ <br/>
$\verb|Rappel|$ <br/>
$\verb|F-mesure|$ <br/>
$\verb|NDCG|$ <br/>
$\verb|AP|$ <br/>
$\verb|RR|$ 

(la classe calcule tous les mesure d'évaluation) <br/>

$\verb|EvalIRModel.py|$ : définir la classe $\verb|EvalIRModel|$ (la classe permet l'évaluation de différents modèles de recherche sur un ensemble de requetes selon différentes mesures d'évaluation)

$\verb|GridSearch.py|$ : définir la classe $\verb|GridSearch|$ (la classe permet l'évaluation de différents paramètres de un modèle de recherche sur un ensemble de requetes selon un mesure d'évaluation)

# **--- TEST ---**

### **Charger des requêtes et de leur docs pertinents**


```python
from QueryParser import *
```


```python
req = QueryParser('./data/cacm/cacm.qry','./data/cacm/cacm.rel')
req1 = req.parseQRY()
req2 = req.parseREL()
print (req2[1].docsPertinents) # req2[1] ou bien req.reqs[1]
print (req2[1].texte)
```

résultat :
```
    [1410, 1572, 1605, 2020, 2358]
     What articles exist which deal with TSS (Time Sharing System), an
    operating system for IBM computers?
```

    

### **Métriques et Plateforme d'évaluation**


```python
from EvalMesure import *
from EvalIRModel import *
```


```python
evalIRModel = EvalIRModel('./data/cacm/cacm')
evalIRModel.fit(weighters=[Weighter1,Weighter2],k=50)
evalIRModel.evaluation(nameModels=["Vectoriel","Okapi"],nbQuery =10)
```

résultat :
```
    Vectoriel  :
    	Weight  1 ; mesure  Precision 
    		mean:  0.052000000000000005 std:  0.03709447398198282
    	Weight  1 ; mesure  Rappel 
    		mean:  0.3076190476190476 std:  0.2547770355987382
    	Weight  1 ; mesure  F_mesure 
    		mean:  0.0794089565629021 std:  0.0445619246991046
    	Weight  1 ; mesure  AP 
    		mean (MAP):  0.08550502169087199 std:  0.055100354020198423
    	Weight  1 ; mesure  NDCG 
    		mean:  0.21320321263610564 std:  0.28766103146071925
    	Weight  1 ; mesure  RR 
    		mean (MRR):  0.2887770562770563 std:  0.29182370159167503
    	Weight  2 ; mesure  Precision 
    		mean:  0.05600000000000001 std:  0.04543126676640219
    	Weight  2 ; mesure  Rappel 
    		mean:  0.3520238095238095 std:  0.2790116840586964
    	Weight  2 ; mesure  F_mesure 
    		mean:  0.08620849455536747 std:  0.053516756782500334
    	Weight  2 ; mesure  AP 
    		mean (MAP):  0.11672996065437447 std:  0.10917264677569836
    	Weight  2 ; mesure  NDCG 
    		mean:  0.12982462285909657 std:  0.16376680469897711
    	Weight  2 ; mesure  RR 
    		mean (MRR):  0.3384387351778656 std:  0.3584530563656995
    Okapi  :
    	Weight  1 ; mesure  Precision 
    		mean:  0.084 std:  0.08475848040166836
    	Weight  1 ; mesure  Rappel 
    		mean:  0.43742063492063493 std:  0.29230257047445085
    	Weight  1 ; mesure  F_mesure 
    		mean:  0.12359805082827371 std:  0.09593265025080626
    	Weight  1 ; mesure  AP 
    		mean (MAP):  0.15350891982746412 std:  0.15492977534612348
    	Weight  1 ; mesure  NDCG 
    		mean:  0.27285245835429883 std:  0.33675697555894846
    	Weight  1 ; mesure  RR 
    		mean (MRR):  0.44000000000000006 std:  0.39074003861618506


    {'Vectoriel-Precision-W1': (0.052000000000000005, 0.03709447398198282),
     'Vectoriel-Rappel-W1': (0.3076190476190476, 0.2547770355987382),
     'Vectoriel-F_mesure-W1': (0.0794089565629021, 0.0445619246991046),
     'Vectoriel-AP-W1': (0.08550502169087199, 0.055100354020198423),
     'Vectoriel-NDCG-W1': (0.21320321263610564, 0.28766103146071925),
     'Vectoriel-RR-W1': (0.2887770562770563, 0.29182370159167503),
     'Vectoriel-Precision-W2': (0.05600000000000001, 0.04543126676640219),
     'Vectoriel-Rappel-W2': (0.3520238095238095, 0.2790116840586964),
     'Vectoriel-F_mesure-W2': (0.08620849455536747, 0.053516756782500334),
     'Vectoriel-AP-W2': (0.11672996065437447, 0.10917264677569836),
     'Vectoriel-NDCG-W2': (0.12982462285909657, 0.16376680469897711),
     'Vectoriel-RR-W2': (0.3384387351778656, 0.3584530563656995),
     'Okapi-Precision-W1': (0.084, 0.08475848040166836),
     'Okapi-Rappel-W1': (0.43742063492063493, 0.29230257047445085),
     'Okapi-F_mesure-W1': (0.12359805082827371, 0.09593265025080626),
     'Okapi-AP-W1': (0.15350891982746412, 0.15492977534612348),
     'Okapi-NDCG-W1': (0.27285245835429883, 0.33675697555894846),
     'Okapi-RR-W1': (0.44000000000000006, 0.39074003861618506)}
```



### **GridSearch**


```python
from GridSearch import *
```


```python
gridSearch = GridSearch('./data/cacm/cacm',percent=0.75)
gridSearch.fit()
gridSearch.evaluation (nameModels=["Okapi"], nameMesures=["AP"], weighters=[Weighter1], nbQuery = 10, k = 50)
```

résultat :
```
    Okapi  : parametre optimal =  (1.3, 0.85)  
    	mean(Train) =  0.15290570175277668
    --- Test ---
    Okapi  :
    	Weight  1 ; mesure  F_mesure 
    		mean:  0.00392156862745098 std:  0.011764705882352941

    {'Okapi-F_mesure-W1': (0.00392156862745098, 0.011764705882352941)}
```


# **TME 4**

## **Explication :**

$\verb|PageRank.py|$ : définir la classe $\verb|PageRank|$ (la classe calcule PageRank) <br/>

# **--- TEST ---**


```python
from PageRank import *
```


```python
path = './data/cisi/cisi.txt'   
n = 20
k = 10
query = "the present time"
pr = PageRank (path,model=None)
pr.PageRank (query,n,k )[:10]
```

résultat :
```
    converge en  8  iteration
    [925, 175, 1302, 603, 245, 484, 382, 625, 1390, 413]