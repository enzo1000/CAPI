import json
import os

#Cette fonction a pour but d'analyser le contenu d'un dictionnaire et de vérifier si les taches présente
# dedans on été faite ou non
def processDic(dic):
    tacheNonTraite = 0
    tacheTraite = 0
    for e in dic:
        if dic[e] == -1:
            tacheNonTraite += 1
        else:
            tacheTraite += 1
    
    return [tacheNonTraite, tacheTraite, tacheNonTraite + tacheTraite]

#Cette fonction a pour but d'ouvrir un dossier contenant des json et 
# de retourner un dictionnaire ayant comme structure {nomFichier : {Tache : valeurAssociée}}
def findAllJson(Folderpath="./data_json/"):  #Default folder to save json files
    dicRet = {}
    try:
        listJson = os.listdir(Folderpath)
    except:
        print("Exception : Bad json folder path")
    else:
        for i in range(len(listJson)):                          #For each elem in the path
            with open(Folderpath + listJson[i], 'r') as f:      #Open it as a json
                try:
                    data = json.load(f)
                except:
                    print("Exception : There is a non-json file in the json folder")
                else:
                    #print("\n".join(data))     #Debug purpose (very pround of it)
                    dicRet[listJson[i].split('.')[0]] = [data, processDic(data)]

    return dicRet


def writeJson(name, dic, Folderpath="./data_json/"):
    with open(f"{Folderpath}{name}.json", 'w') as f:
        json.dump(dic, f)

# Fct de test de la classe, peut être supprimé
# a = findAllJson()
# print(a)
# writeJson(a)
