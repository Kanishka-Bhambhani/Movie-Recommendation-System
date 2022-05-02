import time
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import scipy.sparse as sp
import pickle
from collections import defaultdict
import os

class CFModel:
    def __init__(self, file = None):
        self.base = ['the+wrong+trousers+1993', 'a+close+shave+1995', 'viy+1967', 'alaskaland+2013', 'one+flew+over+the+cuckoos+nest+1975', 
                    'casablanca+1942', 'lawrence+of+arabia+1962', 'cool+hand+luke+1967', 'crouching+tiger_+hidden+dragon+2000', 
                    'shrek+2001', 'lethal+weapon+2+1989', 'the+untouchables+1987', 'one+flew+over+the+cuckoos+nest+1975', 
                    'the+dark+knight+2008', 'the+bridge+on+the+river+kwai+1957', 'vertigo+1958', 'american+beauty+1999', 'fargo+1996', 
                    'rear+window+1954', 'citizen+kane+1941']
        if file == None:
            return

        print(f'Reading data from file {file}')
        with (open(file, "rb")) as openfile:
            try:
                self.ratings = pickle.load(openfile)
            except Exception as e:
                print(f'Train file failed to load \n {e}')
                # break

        # print(f'self.ratings: {self.ratings}')
        print("Processing data")
        self.processData()

        print("Training model")
        self.trainModel()

    def processData(self):
        users = set()
        movies = set()
        for user_id, movie_ids in self.ratings.keys():
            users.add(user_id)
            movies.add(movie_ids)
            if self.ratings[(user_id, movie_ids)] >=3:
                self.ratings[(user_id, movie_ids)] = 1
            else:
                self.ratings[(user_id, movie_ids)] = 0
        
        count = 1
        self.UtoEEncoding = {}
        self.EtoUEncoding = {}
        for user in users:
            self.UtoEEncoding[user] = count
            self.EtoUEncoding[count] = user
            count += 1

        count = 1
        self.MtoEEncoding = {}
        self.EtoMEncoding = {}
        for movie in movies:
            self.MtoEEncoding[movie] = count
            self.EtoMEncoding[count] = movie
            count += 1

        self.encodedData = {}
        for user_id, movie_ids in self.ratings.keys():
            self.encodedData[(self.UtoEEncoding[user_id], self.MtoEEncoding[movie_ids])] = self.ratings[(user_id, movie_ids)]

        del self.ratings
        del movies
        del users

        self.temp = defaultdict(list)
        for user_id, movie_ids in self.encodedData.keys():
            if self.encodedData[(user_id, movie_ids)] == 1:
                self.temp[user_id].append(movie_ids)
        
        row_ind = [k for k, v in self.temp.items() for _ in range(len(v))]
        col_ind = [i for ids in self.temp.values() for i in ids]

        self.sparseMatrix = sp.csr_matrix(([1]*len(row_ind), (col_ind, row_ind)))

        del row_ind
        del col_ind

    def trainModel(self):
        self.knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=3, n_jobs=-1)
        self.knn.fit(self.sparseMatrix)

    def predictForUser(self, user):
        if isinstance(user, str):
            try:
                user = int(user)
            except:
                pass

        if user in self.UtoEEncoding:
            userpref = self.temp[self.UtoEEncoding[user]][:2]
        else:
            return self.base
            
        if (len(userpref) == 0):
            return self.base

        factor = int(20/len(userpref))
        recommendation = []
        for i in userpref:
            _, indices = self.knn.kneighbors(self.sparseMatrix[i],n_neighbors=factor+1)
            indices = indices.flatten()[1:]
            for index in indices[:factor]:
                recommendation.append(self.EtoMEncoding[index])
        recommendation.extend(self.base[:20-len(recommendation)])
        return recommendation

    def savefile(self, data, name):
        f = open(name,"wb")
        pickle.dump(data,f)
        f.close()

    def saveModel(self, name, prefix = "model/"):
        self.savefile(self.UtoEEncoding, prefix + name + "UtoEEncoding.pkl")
        self.savefile(self.knn, prefix + name + "knn.pkl")
        self.savefile(self.temp, prefix + name + "tempEncoding.pkl")
        self.savefile(self.sparseMatrix, prefix + name + "sparseMatrix.pkl")
        self.savefile(self.EtoMEncoding, prefix + name + "EtoMEncoding.pkl")

    def loadfile(self, file):
        objects = []
        with (open(file, "rb")) as openfile:
            while True:
                try:
                    objects.append(pickle.load(openfile))
                    return objects[0]
                except EOFError:
                    return -1
            

    def loadModel(self, name, prefix = "model/"):
        self.UtoEEncoding = self.loadfile(prefix + name + "UtoEEncoding.pkl")
        self.knn = self.loadfile(prefix + name + "knn.pkl")
        self.temp = self.loadfile(prefix + name + "tempEncoding.pkl")
        self.sparseMatrix = self.loadfile(prefix + name + "sparseMatrix.pkl")
        self.EtoMEncoding = self.loadfile(prefix + name + "EtoMEncoding.pkl")

if __name__ == '__main__':
    m = CFModel("data_exploration/sample_pickles/ratings.pkl")
    print(type(m.objects))
    for data in m.objects:
        print(data)


    # print(m.predictForUser('17578'))
    # with open('model.pkl', 'wb') as file:
    #     pickle.dump(m, file, pickle.HIGHEST_PROTOCOL)
    
    # with open('model.pkl', 'rb') as file:
    #     dd = pickle.load(file)
    # print(dd.predictForUser('359906'))

