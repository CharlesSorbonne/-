from Query import *


class QueryParser():
    def __init__(self,cheminQRY,cheminREL):
        self.cheminQRY = cheminQRY
        self.cheminREL = cheminREL
        self.reqs = {}
    
    def parseQRY(self):
        """ 
        Fonction permettant de parser les fichers QRY (avec leurs identifiants et leur texte)
        
        proche de fonction Parser_doc dans Parser.py
        """
        file = open(self.cheminQRY, 'r') 

        currentBalise = None  # type : str
        currentQuery = None   # type : Query()

        line = file.readline()
        while line:
            #récupère la ligne sous forme de mots
            words=line.split()

            #Si la ligne n'est pas vide
            if(len(words)>0):
                if(words[0][0]=='.'): 
                # On est sur une balise
                    if(words[0]==".I"):
                        if(currentQuery != None):
                            #enregistre le Query courant avant d'en créer un autre
                            self.reqs[currentQuery.identifiant] = currentQuery 

                        # on commence une nouvelle balise et crée du Query avec son identifiant
                        currentQuery = Query(words[1])
                        currentBalise = 'I' 

                    elif(words[0]==".W"):
                        currentBalise='W' 
                    else : 
                        currentBalise='uselessBalsie'
                        
                else: 
                    if(currentBalise=='W'):
                        currentQuery.addTexte(line)
            
            #lire une seule ligne suivant
            line = file.readline()
        self.reqs[currentQuery.identifiant] = currentQuery 

        file.close()
        return self.reqs
    
    
    def parseREL(self):
        """ 
        Fonction permettant de parser les fichers REL (ajouter les documents pertinents)
        """
        file = open(self.cheminREL, 'r') 
        self.reqs = self.parseQRY()
        
        line = file.readline()
        while line:
            #récupère la ligne sous forme de mots
            words=line.split()
            
            docPertinent = int(words[1])
            self.reqs[int(words[0])].addDocspertinents(docPertinent)
            
            line = file.readline()
                     
        file.close()
        return self.reqs