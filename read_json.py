import json
import os

with open('./data_json/task_to_plan.json', 'r') as f:
    data = json.load(f)

#{'Tache 1 concernant le tableau de bord': -1, 'Tache 2 concernant le remplissage des cases': -1, 
#'Tache 3 concernant le finalisation du tableau': -1, 'Tache 4 conclusion': -1}
print(data)
print("-----------")
print(os.listdir('./data_json/')[0])

#Faire une fct qui prend aucun argument 

def findAllTasks(path="./data_json/"):  #Default folder to save json files
    listJson = os.listdir(path)
    for i in range(len(listJson)):      #For each elem in the path
        with open(listJson[i], 'r') as f:      #Open it as a json
            data = json.load(f)         #print it