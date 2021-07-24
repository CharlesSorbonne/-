import os
import numpy as np
import librosa
import librosa.display

def get_dic_file (path) :
    """
    in : chemin du data dossier
    out : dictionaire {classe : liste de chemins des fichiers audios de cette classe}
    
    """
    files= os.listdir(path) 
    dic_files = {}
    for file in files:
        scene = file.split('-')[0]
        if scene not in dic_files:
            dic_files[scene] = []
        dic_files[scene].append(file)
    return dic_files


def get_logmel_data (filepath,esp=1e-8,duration = 10,num_freq_bin = 128,num_fft = 2048,num_channel = 1):
    """
    in : un chemin de fichier audio
    out :matrice de dimension (1, 128, 431)
    
    """
    y,sr = librosa.load(filepath, sr=None)
    
    hop_length = int(num_fft / 2)
    num_time_bin = int(np.ceil(duration * sr / hop_length))
    
    logmel_data = np.zeros((num_channel,num_freq_bin, num_time_bin), 'float32')
    logmel_data[:,:,:] = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=num_fft, hop_length=hop_length, 
                                                        n_mels=num_freq_bin, fmin=0.0, fmax=sr/2, htk=True, norm=None)
    logmel_data = np.log(logmel_data+esp)
    return logmel_data



def get_dic_data (path,f_to_data) :
    """
    in : 
        path : chemin du data dossier
        f_to_data : fonction pour traiter les fichiers audios
    out : 
        dictionaire {classe : les donnees traite pour chaque fichier audio}
    
    """
    dic_files = get_dic_file (path)
    dic_data = {}
    for scene in dic_files : 
        dic_data[scene] = []
        for file in dic_files[scene] :
            filepath = path + file
            dic_data[scene].append(f_to_data (filepath))
    return dic_data


def get_data (path,f_to_data) :
    """
    in : 
        path : chemin du data dossier
        f_to_data : fonction pour traiter les fichiers audios
    out : 
        list_data : matrice taille (nombre de echantillion , nombre de channel , dimension x de donnee , dimension y de donnee)
        list_label : (nombre de echantillion , 1)
        classe : liste des classes
        
    """
    dic_files = get_dic_file (path)
    list_data = []
    list_label = []
    classe = []
    c = 0
    for scene in dic_files : 
        for file in dic_files[scene] :
            filepath = path + file
            list_data.append(f_to_data (filepath))
            list_label.append (c)
        c+=1
        classe.append (scene)
    
    # random shuffle
    idx = np.random.permutation(len(list_data))
    list_data,list_label = np.array(list_data)[idx], np.array(list_label)[idx]
    
    return list_data,list_label,classe