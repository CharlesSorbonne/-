import numpy as np
import random


class KMeans():

    def __init__(self, data, k, precision=5, maxite=1e3):
        self.data = data
        self.k = k
        self.precision = precision
        self.centroids = []
        self.clusters = []
        self.cluster_sizes = []
        self.maxite = int(maxite)
        self.cost = []

    @staticmethod
    def dist(p1, p2):
        """Methode retourne distance euclidenne entre deux points"""
        return np.linalg.norm(np.array(p1) - np.array(p2))

    @staticmethod
    def cal_centroids(clusters, precision):
        """Methode retourne centroids (nouveux centres) pour un input de liste de clusters"""
        centroids = []
        for item in clusters: 
            # Pour chaque cluster
            ele = len(item[0])
            c_item = []
            for i in range(ele):
                # mu^(t+1) = barycentre de chaque cluster
                c_item.append(round(np.mean([li[i] for li in item]), precision))
            centroids.append(c_item)
        return centroids

    @staticmethod
    def compare_lists(list_1, list_2):
        """
        Les deux listes ne sont pas en ordre 
        Methode retourne True quand les deux listes sont meme sinon returns False
        """
        flag = True
        for item in list_1:
            if list(item) not in list_2:
                flag = False
            break
        if flag:
            return True
        else:
            return False
            
    @staticmethod
    def cost_fonction(self):
        res = 0
        for center,points in zip(self.centroids,self.clusters):
            res += np.sum ([self.dist(center, point) for point in points])
        return res

    def fit(self):
        """Method that does the clustering"""
        # initialiser les cout
        self.cost = []
        # On choisi l'indice de centroids initial aleatoirement
        indices = random.sample(range(len(self.data)), self.k)
        # Initialiser centroids aleatoire (mu^0)
        for index in indices:
            self.centroids.append(self.data[index])
        
        for _ in range (self.maxite) :
            # Initialization de clusters
            self.clusters = []
            for i in range(self.k):
                self.clusters.append([])
            for point in self.data:
                distances = []
                for centroid in self.centroids:
                    distances.append(self.dist(point, centroid))
                self.clusters[np.argmin(distances)].append(point)
            # Calcul de nouveux centroids
            new_centroids = self.cal_centroids(self.clusters, self.precision)
            # Loop breaks quand centroids ne change pas
            if self.compare_lists(self.centroids, new_centroids):
                break
            self.cost.append(self.cost_fonction(self))
            # Renouveller centroids
            self.centroids = new_centroids
        # Cluster sizes
        for cluster in self.clusters:
            self.cluster_sizes.append(len(cluster))
