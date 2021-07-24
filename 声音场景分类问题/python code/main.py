import DocumentReader as DR
import Net1 as n1
import Net2 as n2
# import NetComplex as nc
import Train as train
import Test as t

import torch.nn as nn
import torch



""" lire les fichiers """
path_train = "../TAU-urban-acoustic-scenes-2020-mobile-development/audio/" 

list_data,list_label,classe = DR.get_data (path_train,DR.get_logmel_data) 

nb_calsse = len(classe)



""" net """
net1 = n1.Net(nb_calsse)

net2 = n2.Net(nb_calsse)

print ("net 1")
matrices_confusion1,net1_validation,net1_trained = train.train (net=net1,lossfonction=nn.CrossEntropyLoss(),list_data = list_data,
                                                         list_label=list_label,pourcentage_validation = 0.9,nbite=2,batch_size=50,
                                                         eps=1e-15,visual =True)

#print ("net 2")
#matrices_confusion2,net2_validation,net2_trained = train.train (net=net2,lossfonction=nn.CrossEntropyLoss(),list_data = list_data,
#                                                         list_label=list_label,pourcentage_validation = 0.9,nbite=2,batch_size=50,
#                                                         eps=1e-15,visual =True)

""" test """
path_test = "../test/" 

t.test(net1,path_test)

#t.test(net2,path_test)



""" enregistrer le réseau """

torch.save(net1.state_dict(), './cifar_net1.pth')

#torch.save(net2.state_dict(), './cifar_net2.pth')