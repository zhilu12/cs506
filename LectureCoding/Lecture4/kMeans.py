import numpy as np
from PIL import Image as im
import matplotlib.pyplot as plt
import sklearn.datasets as datasets

centers = [[0, 0], [2, 2], [-3, 2], [2, -4]]
X, _ = datasets.make_blobs(n_samples=300, centers=centers, cluster_std=1, random_state=0)

class KMeans():

    def __init__(self, data, k):
        self.data = data
        self.k = k
        self.assignment = [-1 for _ in range(len(data))]
        self.snaps = []
    
    def snap(self, centers):
        TEMPFILE = "temp.png"

        fig, ax = plt.subplots()
        ax.scatter(X[:, 0], X[:, 1], c=self.assignment)
        ax.scatter(centers[:,0], centers[:, 1], c='r')
        fig.savefig(TEMPFILE)
        plt.close()
        self.snaps.append(im.fromarray(np.asarray(im.open(TEMPFILE))))
        
    def initiliaze(self):
        return np.random_choice(range(len(self.data), size=self.k, replace=False))
    
    def dist(self, x, y):
        return sum((x-y)**2)**1/2
    
    def assign(self, centers):
        for i in range(len(self.data)):
            min_dist = self.dist(self.data[i], centers[0])
            self.assignment[i] = 0
            for j in range(1, self.k):
                if (self.dist(self.data[i], centers[j]) < min_dist):
                    min_dist = self.dist(self.data[i], centers[j])
                

    def lloyds(self):
        centers = self.initialize()
        self.snap(centers)
        self.assign(centers)
        new_centers = self.update_centers()
        while self.centers_differ(centers, new_centers):
            self.unassign()
            centers = new_centers
            self.assign(centers)
            new_centers = self.update_centers()
        return
    
        

kmeans = KMeans(X, 4)
kmeans.lloyds()
images = kmeans.snaps

images[0].save(
    'kmeans.gif',
    optimize=False,
    save_all=True,
    append_images=images[1:],
    loop=0,
    duration=500
)