import re
from Document import Document

class Parser():
    
    def Parser_doc(chemin):
        file = open(chemin, 'r') 

        res = {}
        currentBalise = None # type : str
        currentDoc = None    # type : Document()

        """
        on ne peut pas utilise Expression régulière pour tous les documents
            parce que il exists les documents sans quelques Balises
        on doit lire ligne par ligne pour éviter le cas

        """
        line = file.readline()
        while line:
            #récupère la ligne sous forme de mots
            words=line.split()

            #Si la ligne n'est pas vide ('\n')
            if(len(words)>0):

                if(words[0][0]=='.'): 
                # On est sur une balise
                    if(words[0]==".I"):
                        if(currentDoc != None): # on a fini la balise précedente
                            #enregistre le document courant avant d'en créer un autre
                            res[currentDoc.identifiant] = currentDoc 
                        # on commence une nouvelle balise et crée du document avec son identifiant
                        currentDoc = Document(words[1])
                        currentBalise = 'I' 
                    elif(words[0]==".T"): # une balise T : titre
                        currentBalise='T' 
                    elif(words[0]==".A"): # une balise A : auteurs
                        currentBalise='A' 
                    elif(words[0]==".W"): # une balise W : texte
                        currentBalise='W' 
                    elif(words[0]==".X"): # une balise X : liens
                        currentBalise='X' 
                    else : # une balsie inutile
                        currentBalise='uselessBalsie'

                else: 
                # On est dans le contenu d'une balise
                    if(currentBalise=='T'):
                        currentDoc.titre += line[:-1]
                    elif(currentBalise=='A'):
                        #extraire l'auteur de la ligne
                        auteur = re.compile(r'(\w+)\s*,\s*(.+)\s*\n').search(line)
                        if(auteur != None):
                            nom = auteur.group(1)
                            prenom = auteur.group(2)
                            currentDoc.auteurs.append([nom,prenom])
                        else: #Si le format n'est pas nom, prenoms, on prend toute la ligne
                            currentDoc.auteurs.append([line[:-1]])
                    elif(currentBalise=='W'):
                        currentDoc.texte+=line
                    elif(currentBalise=='X'):
                        currentDoc.liens.append(int(words[0]))
            
            #lire une seule ligne suivant
            line = file.readline()
        res[currentDoc.identifiant] = currentDoc 

        file.close()
        return res
