import matplotlib.pyplot as plt
import torch.optim as optim
import torch
import torch.nn as nn
import numpy as np
from sklearn.metrics import confusion_matrix


def separer_validation (pourcentage,list_data,list_label):
    validation_size = int(len(list_data)*pourcentage)
    list_data_train = list_data[:validation_size]
    list_label_train = list_label[:validation_size]
    list_data_validation= list_data[validation_size:]
    list_label_validataion = list_label[validation_size:]
    return list_data_train,list_label_train,list_data_validation,list_label_validataion


def train_visual (net,list_data,list_label,pourcentage_validation=1,lossfonction=nn.CrossEntropyLoss(),
                  nbite=1,batch_size=1,visual=True,SGD=False,eps=1e-9,lr=0.001):
    """
    in : 
        net : Réseau
        lossfonction : fonction du cout
        list_data : matrice taille (nombre de echantillion , nombre de channel , dimension x de donnee , dimension y de donnee)
        list_label : liste taille (nombre de echantillion , 1)
        nbite : nombre d'iteration de backward
        batch_size : taille de batch
        visual : decide si on affiche le graphe du cout
        SGD : decide si on utilise SGD ou Adam
    out : 
        visualisation et net
    
    """
    if pourcentage_validation != 1:
        list_data_train,list_label_train,list_data_validation,list_label_validataion=separer_validation(pourcentage_validation,
                                                                                                        list_data,list_label)
    else :
        list_data_train,list_label_train = list_data,list_label
    
    # eviter le cas ou batch_size est plus grand que la taille de donnee
    batch_size = min (len(list_data_train),batch_size)
    
    # choisir le model pour descente de gradiant
    if SGD :
        optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9)
    else :
        optimizer = optim.Adam(net.parameters(), lr=lr,eps = eps)
    
    # on confirme que les echantillions de train sont de ordre arbitraire
    dataset = torch.utils.data.TensorDataset(torch.tensor(list_data_train), torch.tensor(list_label_train))
    dataset = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    # dataset := [[tensor(datax),tensor([label])],...]
    
    # backward
    running_loss = []
    precision = []
    matrices_confusion = []
    for epoch in range(nbite):
        for i,data in enumerate(dataset):
            # extrait datax et label
            inputs, labels = data
            labels = torch.tensor(labels, dtype=torch.long)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = lossfonction(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss.append(loss.item()) # singleton float 
            
            if pourcentage_validation != 1:
                outputs = net(torch.tensor(list_data_validation))
                _, predicted = torch.max(outputs.data,1)
                correct = (np.array(predicted) == list_label_validataion).sum().item()
                precision.append (100 * correct / len(list_data_validation))
                matrices_confusion.append(confusion_matrix(list_label_validataion, predicted))
                
    # affichier les graphe     
    if visual :
        # cout
        plt.plot(running_loss)
        plt.xlabel("nombre d'iteration")
        plt.ylabel("cout")
        if batch_size == 1 :
            plt.title("stochastique")
            plt.savefig ("stochastique.png")
        else :
            plt.title("batch "+str(batch_size))
            plt.savefig ("batch_"+str(batch_size)+".png")
        plt.show()
        
        # precision
        if pourcentage_validation != 1:
            plt.plot(precision)
            plt.xlabel("nombre d'iteration")
            plt.ylabel("precision")
            plt.title("precision validation")
            plt.savefig ("precision_validation.png")
            plt.show()
            print ("validation ",pourcentage_validation*100," % : \n\tloss = ",running_loss[-1]," \n\tprecision : ",precision[-1]," %")
    
    return matrices_confusion,net



def train (list_data,net,list_label,pourcentage_validation=0.9,lossfonction=nn.CrossEntropyLoss(),nbite=1,batch_size=10,
           visual=False,SGD=False,eps=1e-9,lr=0.001):
    
    print ("validation : ")
    matrices_confusion_validation,net_validation = train_visual (net=net,lossfonction=lossfonction,list_data = list_data,
                                                                 list_label=list_label,pourcentage_validation=pourcentage_validation,
                                                                 nbite=nbite,batch_size=batch_size,visual=visual,SGD=SGD,eps=eps,lr=lr)
    
    print ("\n\ntrain : ")
    _,net_trained = train_visual (net=net,lossfonction=lossfonction,list_data = list_data,list_label=list_label,
                  pourcentage_validation=1,nbite=nbite,batch_size=batch_size,visual = visual,SGD=SGD,eps=eps,lr=lr)
    
    return matrices_confusion_validation,net_validation,net_trained