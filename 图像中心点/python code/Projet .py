#!/usr/bin/env python
# coding: utf-8

# In[]:


# pour lire les listes de arête 

def lire_ficher (nom_fichier) :
    
    """
    type d'entrée : String -> (int list) dictionnaire 
    source : le nom de fichier (String)
    hypothèse : 
        On lire le contenu dans la fichier et les transforme de String à Int. 
        
    Il renvoie le dictionnaire dont le clé sont des numéro d'arête et les valeurs sont la liste de paires qui repensent un arête 

    """
    
    # apres fiche.readlines() on obtient :  
        # par exemple : ['0 6\n', '0 3\n', '3 4\n', '4 5\n', '0 2\n', '2 1\n', '4 6\n']    
    fiche = open(nom_fichier,"r")
    contenu = fiche.readlines()

    # apres lire_contenu(contenu) on obtient :  
        # par exemple : {0: [0, 6], 1: [0, 3], 2: [3, 4], 3: [4, 5], 4: [0, 2], 5: [2, 1], 6: [4, 6]}    
    contenu = lire_contenu(contenu)
    
    fiche.close()
    return contenu




def lire_contenu(contenu): 
    """
    type d'entrée : (String) liste -> (int list) dictionnaire 
    source : la liste de String vient de fiche.readlines()
    hypothèse : 
        On realise la transformation de liste de String à Int.
        
    Il renvoie le dictionnaire dont les valeurs sont même contenu que source mais de type (Int) dictionnaire  

    """
    res = dict()
    i = 0
    for x in contenu :
        # on utilise fonction split() pour filtre le string : on obtient 
            # par exemple : {0: ['0', '6'], 1: ['0', '3'], 2: ['3', '4'], 3: ['4', '5'], 4: ['0', '2'], 5: ['2', '1'], 6: ['4', '6']}        
        tmpstr = x.split()

        # on transforme type Sting à Int        
        tmpint = [int(tmpstr[0]),int(tmpstr[1])]
  
        res [i] = tmpint
        i = i + 1
    return res 




#lire_ficher ("test")


# In[]:


# pour créer les listes adjacents

def fonction_liste_adjacent (nom_fichier) :
    
    """
    type d'entrée : String -> (int list) dictionnaire 
    source : le nom de fichier (String)
    hypothèse : 
        On lire le contenu dans la fichier et les traite comme les donné de une graphe. On chercher les listes adjacents de chaque sommet.
        
    Il renvoie le dictionnaire dont le clé sont des sommets et les valeurs sont la liste d'adjacence du sommet représenté par la clé  
    
    """
    

    # on lire les arrêts avec la fonction lire_ficher (), et obtient :
        # par exemple : {0: [0, 6], 1: [0, 3], 2: [3, 4], 3: [4, 5], 4: [0, 2], 5: [2, 1], 6: [4, 6]}
    l = lire_ficher (nom_fichier)
    liste_adjacent = dict()
    
    for indice in range(len(l)) :
        x1 = l[indice][0]              # x1 : le premier sommet d'une arête 
        x2 = l[indice][1]              # x2 : le second sommet d'une arête 
              
        # on cherche la dictionaire de clé "x1" si il existe on le ajoute dans la liste de clé "x1", sinon on crée la diste de clé "x1"
        if x1 in liste_adjacent:
            liste_adjacent[x1].append(x2) 
        else : 
            liste_adjacent[x1] = [x2]
                
        # on fait le même pour "x2"
        if x2 in liste_adjacent :
            liste_adjacent[x2].append(x1) 
        else : 
            liste_adjacent[x2] = [x1]
        
    return liste_adjacent


#fonction_liste_adjacent ("test")


# In[]:


def distance (liste_adjacent ,centre):
    distance = {}
    verifie = {}
    for x in liste_adjacent:
        verifie[x] = -1
        if(x == centre):
            verifie[x]=1
   
    distance[0]=[centre]
    distance[1]=liste_adjacent[centre]
    modifier_verifie(distance[1],verifie)
    
    i=1
    while(distance[i]!=[]):
        i = i + 1
        distance[i] = []
        for x in distance[i-1]:
            for y in liste_adjacent[x]:
                ajouter_ele(y,distance[i],verifie)
    del distance[i]
    return distance

def modifier_verifie(tableau,verifie):
    for x in tableau:
        verifie[x] = 1
        
def ajouter_ele(x,distance,verifie):
    if(verifie[x]==-1):
        distance.append(x)
        verifie[x] = 1
    return distance
        

#distance(liste_adjacent , 1)


# In[]:


# pour calculer just des classes des sommets
import copy

def PGCC_Class (nom_fichier):
    """
    type d'entrée : String -> (int liste) dictionnaire
    source : le nom de fichier (String) 
    hypothèse : 
        on parcour tous les sommet et obtient leurs composantes connexes
                                
    Il renvoie de dictionnaire dont le clé sont les numéros de classe et les valeur :
            int liste represent l'ensemble de sommet de la même classe 
        
    """
    niveau = -1
    composante_connexe = dict()
    used = dict()        # pour stocke les elements qui est utilisées
    all_false = dict()   # pour initialiser usedtmp

    liste_adjacent = fonction_liste_adjacent (nom_fichier) 

    # on initialise used pour chaque clé qui est la sommet qui existe dans ce graphe."-1" qui represent "false"
    for x in liste_adjacent :
        used[x] = -1
        all_false[x] = -1
     
    # on parcour tous les sommet
    for centre in used : 
        D = dict()
        sommet = []
        somme = 0
        i = 1
        ll = []
        
        # on choisis bien le niveau de cette sommet         
        if (used[centre] == -1 ):
            niveau = niveau + 1
            niveautmp = niveau
            composante_connexe [niveautmp] = []
        else :
            continue
        
        # initialiser usedtmp pour chercher distance
        usedtmp = copy.deepcopy(all_false)
        
        # on initialisation D[0] et D[1] et changer la valeur de used dont le clé existe dans D et les note par "0" qui represent "true"
        D[0]=[centre] 
        used[centre] = niveautmp
        usedtmp[centre] = niveautmp
        sommet.append(centre)
        D[1]= liste_adjacent[centre] 
        for x in D[1] :
            somme = somme + 1
            used [x] = niveautmp
            usedtmp [x] = niveautmp
            sommet.append(x)
        
        # [même que la calculation de distance dans la fonction précédente]
        # on recurrence avec D : D(i+1) = tous les sucesseur de elements dans D(i) except les element qui a deja utilisé just'à D[i+1] = []
        while (D[i]!=[]):
            i = i + 1
            # la liste d'ensemble des listes adjacents des éléments de liste de distance précédent
            # c'est-à-dire : par exemple si D[i] = [0,1] ,alors ll = liste_adjacent[0] + liste_adjacent[1]
            for x in D[i-1] :
                ll = ll + liste_adjacent[x]             
            # On filtre les elements qui n'est pas utilisées dans "ll" et les stocke comme D[i+1]
            if (ll != []) :
                tmp = [] 
                for x in ll :  
                    #  si les elements dans "ll" n'existe pas dans used (il est dans distance plus petit), 
                    #        on les ajoute dans used et renvoie tous par un liste 
                    #  sinon on ne fait rien 
                    if (usedtmp[x] == -1) :
                        used [x] = niveautmp
                        usedtmp[x] = niveautmp
                        sommet.append(x)
                        tmp.append (x)
                D[i] = tmp
        
        # on stocke les classes
        composante_connexe [niveautmp] = sommet
        
    
    return composante_connexe
      
        
#PGCC_Class ("test" )


# In[]:


# pour calculer la centralité de proximité des sommets de centralité de proximité maximum pour chaque composante connexe.

def centraliser_proxi_valeur (nom_fichier):
    """
    type d'entrée : String -> (double) dictionnaire
    source : le nom de fichier (String) 
    hypothèse : 
        on parcour tous les sommet et obtient leurs valeurs des centralités de proximité 
                                et on compare tous les valeurs des centralités de proximité  pour choisr le plus grand
                                
    Il renvoie de dictionnaire dont le clé est la plus grand centralisé de proximité
                                    la valeur est la valeur de la plus grand centralisé de proximité
        
    """
    classe = PGCC_Class (nom_fichier)
    centraliser_proxi_valeur = dict()
    d = dict()
    
    liste_adjacent = fonction_liste_adjacent (nom_fichier) 
    
    for niveau in classe:
        sommet_pgcc = -1
        somme_min = -1
        
        # on parcours tous les sommet dans même classe et cherche le plus grand connexe 
        for sommet in classe[niveau] :
            somme = 0
            d = distance (liste_adjacent ,sommet)
            
            for x in d :
                somme = somme + x*len(d[x])
                
            if (somme < somme_min or somme_min == -1) :
                somme_min = somme 
                sommet_pgcc = sommet
                
        centraliser_proxi_valeur[sommet_pgcc] = 1.0/somme_min

    return centraliser_proxi_valeur

    

#centraliser_proxi_valeur ("test" )


# In[]:


# on crée une graphe
import random

def un_graphe ( nombre_arete , nombre_sommet , minrandom , maxrandom , nom_fichier ) :
    """
    type d'entrée : int * int * int * String -> (int liste) dictionnaire
    source :    le nombre d'arête créé par cette fonction, 
                le maximum de numéro de sommet, 
                le minimum de numéro de sommet,
                le nom de fichier (String) 
    hypothèse : 
        Il crée une graphe d'après Erdős–Rényi est stocke dans un fichier nommé par nom_fichier (dans la source)
        
    Il renvoie les listes adjacentes par un dictionnaire dont le clé est le numéro de arête et la valeur est le arête.
        
    """
    liste_arete = dict ()
    
    fiche = open(nom_fichier,"w")
    
    i = 0
    
    # n = nombre_sommet alors nombre_arete minimal(n-1+1)*(n-1) / 2 
    if ((nombre_sommet*(nombre_sommet-1))/2 <= nombre_arete ):
        print ("erreur pour nombre de arete, on cree une graphie qui contient 'nombre_sommet' sommet")
        while (i < nombre_arete) :
            liste_arete[i] = [-1,-1]
            
            # on prend sommet aléatoire 
            x1 = random.randint(minrandom,maxrandom)
            x2 = random.randint(minrandom,maxrandom)

            # vérifier qu'il n'y a pas de "arête" comme : "i-i" et il n'existe que une arête entre i et j (pas de multiple de "i-j")
            if (x1 != x2 and existance(liste_arete,x1,x2) == 1 ) :
                liste_arete[i][0] = x1
                liste_arete[i][1] = x2
                string = str(x1) + " " +  str(x2) + "\n"
                fiche.write( string )
                i = i + 1        
    
    else :
        liste_sommet = [0] * nombre_sommet
        liste_sommet[0] = random.randint(minrandom,maxrandom)
        i = i + 1
        while (i < nombre_sommet) :
            rand = random.randint(minrandom,maxrandom)
            if rand not in liste_sommet :
                liste_sommet[i] = rand
                i = i + 1
        i = 0
        while (i < nombre_arete) :
            liste_arete[i] = [-1,-1]
            
            # on cherche les sommets dans liste_sommet
            x1 = liste_sommet[random.randint(0,nombre_sommet-1)]
            x2 = liste_sommet[random.randint(0,nombre_sommet-1)]

            # vérifier qu'il n'y a pas de "arête" comme : "i-i" et il n'existe que une arête entre i et j (pas de multiple de "i-j")
            if (x1 != x2 and existance(liste_arete,x1,x2) == 1 ) :
                liste_arete[i][0] = x1
                liste_arete[i][1] = x2
                string = str(x1) + " " +  str(x2) + "\n"
                fiche.write( string )
                i = i + 1   
    

            
    fiche.close()
    return liste_arete
        
    
def existance (liste_arete,x1,x2) :
    """
    type d'entrée : int liste * int * int -> int 
    source :    le dictionnaire dont le clé est le numéro de arête et la valeur est le arête 
                le numéro de sommet x1
                le numéro de sommet x2
    hypothèse : 
        Il vérifie s'il n'existe que une arête entre i et j (pas de multiple de "i-j")
        
    Il renvoie  1 si il n'existe dans "liste_sommet"
                0 sinon
        
    """
    for x in liste_arete :
        if ((liste_arete [x][0] == x1 and liste_arete [x][1] == x2) or (liste_arete [x][0] == x2 and liste_arete [x][1] == x1)):
            return 0 
    return 1
        
    
#un_graphe ( 24 ,45 , 0 , 45 ,"test")


# In[]:


#fonction_liste_adjacent ("test")


# In[]:


# pour calculer les sommet de degré maximal 
def degre_max (nom_fichier) :
    """
    type d'entrée : String -> (int liste) dictionnaire
    source : le nom de fichier (String) 
    hypothèse : 
        Il calcule les sommet de degré maximal 
        
    Il renvoie les listes des sommet de degré maximal.
        
    """
    used = dict()        # pour stocke les elements qui est utilisées
    all_false = dict()   # pour initialiser usedtmp
    sommet_max = []
    degre_max = -1
    
    liste_adjacent = fonction_liste_adjacent (nom_fichier) 
    
    for sommet in liste_adjacent :
        used[sommet] = -1
        all_false[sommet] = -1
        
    for sommet in liste_adjacent :
        used= copy.deepcopy(all_false)
        degre = 0
        
        for fils in liste_adjacent[sommet] :
            # "used" pour verifier si degre deja compte ce sommet 
            # ( on suppose il exist plusieurs mêmes arrête et len(liste_adjacent) pas correct pour degré )
            if ( used[fils]== -1 ):
                used[fils] = 1
                degre=degre + 1
                
        if (sommet_max == []):
            # initaliation
            sommet_max = [sommet]
        else :
            if (degre > degre_max) :
                # alors on cherche le plus grand degré 
                sommet_max = [sommet]
                degre_max = degre
                continue 
            if  (degre == degre_max) :
                # alors on cherche les sommet de degré maximal  
                sommet_max.append (sommet)
    
    return sommet_max

#degre_max ("chicago_net.txt")


# In[]:


import time
def timetest1 () :
    start = time.process_time()
    l = centraliser_proxi_valeur  ("chicago_net.txt") 
    end = time.process_time()
    print (end-start)
    return l
    
#timetest1 ()


# In[]:


import time
def timetest1 () :
    start = time.process_time()
    l = degre_max ("chicago_net.txt")
    end = time.process_time()
    print (end-start)
    return l
    
#timetest1 ()


# In[]:


# pour calculer degré de tous les sommets

from collections import OrderedDict

def centraliser_degree (fichier) :
    """
    type d'entrée : String -> (int liste) dictionnaire
    source : le nom de fichier (String) 
    hypothèse : 
        Il calcule degré de tous les sommets
        
    Il renvoie sommet de degre maximun 
            et une dictionaire dont la valeur est le degré et les sommet sont representés par les clé.
        
    """
    dic = fonction_liste_adjacent(fichier)
    composant = PGCC_Class (fichier)
    degree = {}
    cc=-1
    maxi=0
    
    for niveau in composant:
        for x in composant[niveau]:
            n = len(dic[x])
            degree[x]=n
            if(n>maxi):
                maxi = n
                cc = x
    return (cc,degree)

#centraliser_degree ("chicago_net.txt")


# In[]:


# pour calculer la centralité de proximité de tous les sommets

from collections import OrderedDict

def centraliser_proxi (nom_fichier):
    """
    type d'entrée : String -> (double) dictionnaire
    source : le nom de fichier (String) 
    hypothèse : 
        on parcour tous les sommet et obtient leurs valeurs des centralités de proximité 
                                
    Il renvoie de dictionnaire dont le clé est les sommet et les valeur representé les valeur des centralités de proximité
        
    """
    liste_adjacent = fonction_liste_adjacent (nom_fichier) 
    centraliser_proxi = dict()
    d = dict()
    
    for sommet in liste_adjacent :
        somme = 0
        d = distance (liste_adjacent ,sommet)

        for x in d :
            somme = somme + x*len(d[x])

        centraliser_proxi[sommet] = 1.0/somme
    
    centraliser_proxi_tmp = centraliser_proxi
    centraliser_proxi = sort_value(centraliser_proxi,True)
    noeud = list(centraliser_proxi)[0]
    return (noeud,centraliser_proxi_tmp)

def sort_value(old_dict, reverse):
    items = sorted(old_dict.items(), key=lambda obj: obj[1], reverse=reverse)
    new_dict = OrderedDict()
    for item in items:
        new_dict[item[0]] = old_dict[item[0]]
    return new_dict
    
    
#centraliser_proxi ("chicago_net.txt" )


# In[]:


# pour calculer la centralité harmonique de tous les sommets

from collections import OrderedDict

def centraliser_harmonique (nom_fichier):
    """
    type d'entrée : String -> (double) dictionnaire
    source : le nom de fichier (String) 
    hypothèse : 
        on parcour tous les sommet et obtient leurs valeurs des centralités harmonique
                                
    Il renvoie de dictionnaire dont le clé est les sommet et les valeur representé les valeur des centralités harmonique
        
    """
    liste_adjacent = fonction_liste_adjacent (nom_fichier) 
    centraliser_proxi = dict()
    d = dict()
    
    for sommet in liste_adjacent :
        somme = 0
        d = distance (liste_adjacent ,sommet)

        for x in d :
            if ( x*len(d[x])!= 0 ):
                somme = somme + 1.0 / x*len(d[x])

        centraliser_proxi[sommet] = somme
    
    centraliser_proxi_tmp = centraliser_proxi
    centraliser_proxi = sort_value(centraliser_proxi,True)
    noeud = list(centraliser_proxi)[0]
    return (noeud,centraliser_proxi_tmp)

def sort_value(old_dict, reverse):
    items = sorted(old_dict.items(), key=lambda obj: obj[1], reverse=reverse)
    new_dict = OrderedDict()
    for item in items:
        new_dict[item[0]] = old_dict[item[0]]
    return new_dict
    
    
#centraliser_harmonique ("chicago_net.txt" )


# In[]:


# pour calculer la valuer Pearson et comparer les deux 

from scipy.stats import pearsonr

def coef_pearson(ficher):
    """
    ficher -> 5plet(Pearson de centralité de proximité ,
                    Pearson de centralité harmonique,
                    classment de degrée des noeuds,
                    classement de centralité de proximité,
                    classement de centralité harmonique )

    """
    (cd,degree) = centraliser_degree(ficher)
    (cp,proxi) = centraliser_proxi(ficher)
    (ch,harmonique) = centraliser_harmonique(ficher)
    dic = tirer_noeuds(ficher)

    x = [];y = [];z=[]
    
    for i in dic:
        x.append(degree[i])
        y.append(proxi[i])
        z.append(harmonique[i])
    pearson_proxi_deg = pearsonr(x,y)
    pearson_harmo_deg = pearsonr(x,z)
    pearson_harmo_proxi = pearsonr(y,z)
    return (pearson_proxi_deg,pearson_harmo_deg,pearson_harmo_proxi,x,y,z)

def tirer_noeuds(ficher):
    dic = []
    liste = PGCC_Class (ficher)
    for niveau in liste:
        for sommet in liste[niveau]:
            dic.append (sommet)
    dic = sorted(dic)
    return dic
    
    
#coef_pearson ("chicago_net.txt")


# In[]:


def cherche_classement(liste,val):
    """
    cette fonction est pour chercher le classement dans une liste triée
    """
    for i in range(len(liste)):
        (x,y)=liste[i]
        if(x==val):
            return i
    return -1


# In[]:


from scipy.stats import spearmanr

def coef_spearman(ficher): 
    
    """
    ficher -> 5plet(spearman de proximité et degreé,
                    spearman de proximité et harmonique,
                    classment de degrée des noeuds,
                    classement de centralité de proximité,
                    classement de centralité harmonique )

    """
    (ch,dic_harmonique) = centraliser_harmonique(ficher)
    (cd,dic_degree) = centraliser_degree(ficher)
    (cp,dic_proxi) = centraliser_proxi(ficher) #rappelle des fonctions
   
    dic = sorted(dic_proxi.keys())#obtenir les noeuds de la pgcc trié
    
    harmonique = sorted(dic_harmonique.items(),key = lambda x:x[1],reverse = True) 
    degree = sorted(dic_degree.items(),key = lambda x:x[1],reverse = True) 
    proxi = sorted(dic_proxi.items(),key = lambda x:x[1],reverse = True) #trier les deux tableaux 
    
    x=[];y=[];z=[]

    for i in dic:#construire les tableaux de sclassements de degree et de proximite
        x.append(cherche_classement(degree,i))
        y.append(cherche_classement(proxi,i))
        z.append(cherche_classement(harmonique,i))
    spear_proxi_deg = spearmanr(x,y)
    spear_harmoni_deg = spearmanr(x,z)
    spear_harmoni_proxi = spearmanr(y,z)
    return (spear_proxi_deg , spear_harmoni_deg , spear_harmoni_proxi , x , y , z)

#coef_spearman("chicago_net.txt")


# In[]:


#shéma de distribution de degrée
from matplotlib import pyplot as plt

def deg_noeuds () :
    (noeud,diction)=centraliser_degree("chicago_net.txt")
    tmp = [diction[num] for num in diction]
    x = list(set(tmp))
    y = [tmp.count(n) for n in x]

    plt.plot(x, y, color='blue', marker='+',linestyle='solid')
    plt.title('Distribution de degrée')
    plt.xlabel('Degrée')
    plt.ylabel('Nbr de noeuds')
    plt.show()
    # plt.savefig('plot')


# In[]:


#déssiner le graphe du Spearman et Pearson
from matplotlib import pyplot as plt 

(spear_proxi_deg,spear_harmoni_deg,spear_harmoni_proxi,x,y,z) = coef_spearman("chicago_net.txt")
(pearson_proxi_deg,pearson_harmo_deg,pearson_harmo_proxi,useless1,useless2,useless3) = coef_pearson("chicago_net.txt")

def degre_proxi ():
    s = 'Spearman = '+ str(spear_proxi_deg[0])+'\nPearson = '+str(pearson_proxi_deg[0])
    plt.scatter(x, y, c='b', s=20 , alpha=0.5)
    plt.title(s)
    plt.xlabel('Degrée')
    plt.ylabel('Proximité')
    plt.show()


# In[]:

def degre_harmo ():
    s = 'Spearman = '+ str(spear_harmoni_deg[0])+'\nPearson = '+str(pearson_harmo_deg[0])
    plt.scatter(x, z, c='b', s=20 , alpha=0.5)
    plt.title(s)
    plt.xlabel('Degrée')
    plt.ylabel('harmonique')
    plt.show()


# In[]:

def proxi_harmo () :
    s = 'Spearman = '+ str(spear_harmoni_proxi[0])+'\nPearson = '+str(pearson_harmo_proxi[0])
    plt.scatter(y, z, c='b', s=20 , alpha=0.5)
    plt.title(s)
    plt.xlabel('Proximité')
    plt.ylabel('harmonique')
    plt.show()


# In[]:


def fixe_un_noeud (nom_fichier , centre): 
    """
    (nom de fichier , la source "centre")
        --> res est un tableau de liste de liste, chaque liste de liste res[i] contient les chemin entre la source et le nœud i, 
            décrit comme une liste des nœuds intermédiaires 
    
    """
    liste_adjacent = fonction_liste_adjacent (nom_fichier) 
    res = dict ()
    for elem in liste_adjacent[centre] :
        res[elem] = [[]]
    
    check = True
    while (check == True) :
        check = False 
        
        tmpparcour = []
        for elem in res :
            tmpparcour.append (elem)
        for elems in tmpparcour :
            for fils in liste_adjacent[elems] :
                if (fils != centre) :
                    tmp = creer_un_chemin (res ,fils , elems) 
                    if (tmp != []) :
                        res[fils] = tmp
                        check = True      
    return res 
    
    
                    
def creer_un_chemin (res ,fils , elems):
    """
    pour obtenir un chemin. c'est un élément de res[i]
    
    """
    tmplist = []
    for chemin in res[elems]:
        copylist = chemin[:] + [elems]
        if fils in res :
            if (len(res[fils][0])==len(copylist)) : 
                if (pas_meme (copylist,res[fils])):
                    tmplist= res[fils][:]
                    tmplist.append (copylist)
        else :
            tmplist.append (copylist)
            
    return tmplist 



def pas_meme (copylist , listeres) :
    """
     pour verifier si il y a un chemin plus court que ce qu'on creer
     
    """
    for chemin in listeres :
        for indice in range(len (copylist)):
            if (copylist[indice]!=chemin[indice]):
                continue
            return False
    return True 



fixe_un_noeud ("test" , 3)


# In[]:


def valeur_centralite_intermediaire (nom_fichier): 
    """
    nom de fichier
        --> res est une dictionnaire dont les clés sont des nœud et les valeurs sont des valeurs de centralite intermediaire
    
    """
    res = dict()
    graphe = PGCC_Class (nom_fichier)
    for niveau in graphe :
        for x in graphe[niveau] :
            somme = 0.0
            for y in graphe[niveau] :
                ensemble_de_chemin = fixe_un_noeud (nom_fichier , y)
                for z in ensemble_de_chemin :
                    if (y!=x or z!=x or y!=z) :
                        nombre_de_plus_court_chemin_de_y_a_z = len(ensemble_de_chemin[z])
                        nombre_de_plus_court_chemin_pass_x = nb_pass_x ( x , ensemble_de_chemin[z])
                        somme = somme + nombre_de_plus_court_chemin_pass_x * 1.0 / nombre_de_plus_court_chemin_de_y_a_z
            res[x] = somme 
    return res 
            

def nb_pass_x ( x , chemin_liste):
    nb = 0
    for chemin in chemin_liste :
        if x in chemin :
            nb = nb + 1
    return nb 

#valeur_centralite_intermediaire ("test")


# In[]:


def centralite_intermediaire (nom_fichier): 
    """
    nom de fichier
        --> le plus grand valeur de centralite intermediaire
    
    """
    valeur = valeur_centralite_intermediaire ("test")
    centraliser_inter = sort_value(valeur,True)
    noeud = list(centraliser_inter)[0]
    return noeud 

#centralite_intermediaire("test")








# In[]:

import os

def stock_fichier (densite ,n) :
    m = int (0.5 * n * (n-1) * densite);
    nom_fichier = "test" + str(densite*100) + str(n) + ".txt"
    un_graphe(m, n, 0, n, nom_fichier)

def creer_tous_test () :
    all_tab = [100, 130, 160, 200, 230, 260, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560,
               580, 600]
    for densite in [0.1,0.2,0.3,0.5,0.8]:
        for n in all_tab :
            nom_fichier = "test" + str(densite*100) + str(n) + ".txt"
            if not os.path.exists(nom_fichier) :
                stock_fichier(densite, n)


# In[]:

import time

def creer_temps_data(s, n, data_fichier):
    nom_fichier = "test" + str(s*100) + str(n) + ".txt"
    if not os.path.exists(nom_fichier):
        stock_fichier(s, n)

    start = time.process_time()
    centraliser_proxi_valeur(nom_fichier)
    end = time.process_time()
    temps = end - start

    fich = open(data_fichier, "a+")
    string = str(s) + " " + str(n) + " " + str(temps) + "\n"
    fich.write(string)

def temp_test_fichier_version(s, data_fichier):
    test_tab = [100, 130, 160, 200, 230, 260, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500]
    grand_tab = [520, 540, 560, 580, 600]
    all_tab = [100, 130, 160, 200, 230, 260, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560,
               580, 600]
    for n in all_tab:
        if (s == 0.8) and ( n >= 500) :
            break
        creer_temps_data(s, n, data_fichier)


# In[]:

def creer_temps_data_degre(s, n, data_fichier):
    nom_fichier = "test" + str(s*100) + str(n) + ".txt"
    if not os.path.exists(nom_fichier):
        stock_fichier(s, n)

    start = time.process_time()
    degre_max (nom_fichier)
    end = time.process_time()
    temps = end - start

    fich = open(data_fichier, "a+")
    string = str(s) + " " + str(n) + " " + str(temps) + "\n"
    fich.write(string)

def temp_test_fichier_version_degre(s, data_fichier):
    test_tab = [100, 130, 160, 200, 230, 260, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500]
    grand_tab = [520, 540, 560, 580, 600]
    all_tab = [100, 130, 160, 200, 230, 260, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560,
               580, 600]
    for n in all_tab:
        if (s == 0.8) and ( n >= 500) :
            break
        creer_temps_data_degre(s, n, data_fichier)


# In[]:

def charger_graphe_temps ():
    for densite in [0.1, 0.2, 0.3, 0.5, 0.8] :
        temp_test_fichier_version(densite, "data")
        temp_test_fichier_version_degre(densite, "datadeg")
def graphe ():
    deg = 3
    dessiner_le_graphe(deg, "data")
    deg = 2
    dessiner_le_graphe(deg, "datadeg")






# In[]:

from random import choice
import numpy as np
from scipy.optimize import leastsq


def error(params , x , y,deg) :
    """
    = f(x) - y
    f est le fonction on suppose
    y est la valeur donné

    """
    res = 0.0
    for i in range(deg + 1) :
        res = params[i] + res * x
    res = res - y
    return res


def creer_fonction(params , x , y,deg) :
    """
    = f(x)
    methode Horner

    """
    for i in x :
        res = 0.0
        for l in range(deg + 1) :
            res = params[l] + res * i
        y.append(res)


color_sequence = ['#1f77b4' , '#aec7e8' , '#ff7f0e' , '#ffbb78' , '#2ca02c' , '#98df8a' , '#d62728' , '#ff9896' ,
                  '#9467bd' , '#c5b0d5' ,
                  '#8c564b' , '#c49c94' , '#e377c2' , '#f7b6d2' , '#7f7f7f' , '#c7c7c7' , '#bcbd22' , '#dbdb8d' ,
                  '#17becf' , '#9edae5']


def dessiner_le_graphe(deg,data_fichier) :
    """
    (deg on suppose le compexite ,ficher qui stocké tous les data de temps on a testé avant )-> graphe

    """
    fiche = open(data_fichier , "r")
    contenu = fiche.readlines()

    res = {}
    tmpstr = []

    for x in contenu :
        tmpstr = x.split()

        delta = float(tmpstr[0])
        noeud = int(tmpstr[1])
        temps = float(tmpstr[2])

        if delta in res :
            check = True
            for data in res[delta] :
                if (data[0] == noeud) :
                    # s'il y a deux data on choix la moyenne
                    data[1] = (temps + data[1]) / 2
                    check = False
                    break;
            if (check) :
                res[delta].append([noeud , temps])
        else :
            res[float(tmpstr[0])] = [[noeud , temps]]

    for delta in res :

        tmpx = []
        tmpy = []
        yfinal = []

        for data in res[delta] :
            tmpx.append(data[0])
            tmpy.append(data[1])

        x = np.array(tmpx)
        y = np.array(tmpy)

        # leastsq : Méthode des moindres carrés
        coef = [1] * (deg + 1)
        parasdetermine = leastsq(error , coef , args=(x , y, deg))

        src = str(delta) + ' : f(x) = '
        for i in range(deg + 1) :
            if (i != deg) :
                src = src + str(parasdetermine[0][i]) + ' x^' + str(deg - i) + ' + '
            else :
                src = src + str(parasdetermine[0][i])
        print(src)

        erreur = 0.0
        for i in range(len(tmpx)) :
            erreur += error(parasdetermine[0] , tmpx[i] , tmpy[i], deg) ** 2
        print('  erreur : ' + str(erreur))

        creer_fonction(parasdetermine[0] , x , yfinal,deg)
        color = choice(color_sequence)
        plt.scatter(tmpx , tmpy , c=color , marker='+' , alpha=0.5 , label=str(delta))
        plt.plot(x , yfinal , color , marker='' , linestyle='-' , label='courbe de ' + str(delta))

    plt.legend()
    plt.title("temps - nombre de noeud")
    plt.xlabel('nombre de noeud')
    plt.ylabel('temps')
    plt.show()

