class Query():
    def __init__(self, idQuery):
        self.identifiant = int(idQuery)
        self.texte = ""
        self.docsPertinents = []
     
    def addTexte(self, texte):
        self.texte += texte
        
    def addDocspertinents(self,doc):
        self.docsPertinents.append(doc)