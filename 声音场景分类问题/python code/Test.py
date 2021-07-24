import torch
import DocumentReader as DR

def test (net,path_test) :
    list_test_data,list_test_label,classe = DR.get_data (path_test,DR.get_logmel_data)
    
    correct = 0
    total = 0
    class_correct = list(0. for i in range(len(classe)))
    class_total = list(0. for i in range(len(classe)))
    with torch.no_grad():
        for datas, labels in zip(list_test_data,list_test_label):

            datas = torch.tensor([datas], requires_grad=True)
            labels = torch.tensor([labels], dtype=torch.long)

            outputs = net(datas)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            c = (predicted == labels).squeeze()
            label = labels[0]
            class_correct[label] += c.item()
            class_total[label] += 1

    print('Precision de Reseau : %d %%' % (100 * correct / total),"\n")

    for i in range(len(classe)):
        print('Precision de %5s : %2d %%' % (
            classe[i], 100 * class_correct[i] / class_total[i]))