import pickle
import sys
import os
import os.path as osp
sys.path.append(os.path.dirname(os.getcwd()))
from deployment.CFModel import CFModel



class Model:
    def __init__(self):
        self.dict = {}
        self.model = CFModel()
        self.model.loadModel('oldModel')
        # self.updateModel()

    # if the dict has recommendation for the user, return the recommendation
    # else return CFModel's recommendation
    def getRecommendation(self, user_id):
        # if (user_id in self.dict):
        #     return self.dict[user_id]
        # else:
        return self.model.predictForUser(user_id)

    # Update the model by reading the model.pkl file and update the dict
    def updateModel(self):
        # with open('model.pkl', 'rb') as file:
        #     self.model = pickle.load(file)

        self.dict = {}
        
        # get all user_ids
        users = set()
        for user_id in self.model.UtoEEncoding:
            users.add(user_id)
        
        # get recommendation for each user and store the key value pair in the dict
        for user_id in users:
            self.dict[user_id] = self.model.predictForUser(user_id)

if __name__ == '__main__':
    model = Model()

    print(model.getRecommendation('359906'))
    print(model.getRecommendation('158599'))

