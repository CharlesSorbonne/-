class Document():
    
    def __init__(self, identifiant):
        self.identifiant=int(identifiant)
        self.titre=""
        self.auteurs=[]
        self.texte=""
        self.liens=[]
    
    def __repr__(self):
        
        #formater l'identifiant
        identifiant = "\nIdentifiant : "+str(self.identifiant)
        
        #Formater le titre
        titre = ""
        if(self.titre != ""):
            titre = "\nTitre : "+str(self.titre)
        
        #Formater les auteurs
        auteurs = ""
        if(self.auteurs!= []):
            auteurs = "\nAuteurs : \n"
            for auteur in self.auteurs:
                auteurs+="\t" + " ".join(auteur) +"\n"
        
        #Formater le texte
        texte=""
        if(self.texte != ''):
            texte = "Longeur de texte : "+ str(len(self.texte)) +"\n "
        
        #Formater les liens
        liens=""
        if(self.liens != []):
            liens = "Nombre de liens : "+str(len(self.liens))
            
        return "\n-----------------------------" + identifiant+titre+auteurs+texte+liens+"\n-----------------------------\n"
    
        
    