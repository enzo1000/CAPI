import unittest
import os
import json
from import_json import processDic
from import_json import findAllJson
from import_json import writeJson

from factoryEvent import FactoryEvent

class TestStringMethods(unittest.TestCase):
    #Test ayant pour but de vérifier le nombre de tache réalisés dans un dictionnaire
    # Retour attendu :
    # Liste = [int tacheNontraite, int tacheTraitée, int nbDeTacheTotales]
    def test_processDic(self):
        #Dictionnaire avec 2 tache réalisés et 2 tache non réalisés
        fakeDico = {"Tache1" : -1, "Tache2" : 6, "Tache3" : 7, "Tache19" : -1}
        ret = processDic(fakeDico)
        self.assertEqual(ret, [2, 2, 4])
        self.assertNotEqual(ret, [2, 5, 4])


    #Test ayant pour but de vérifier la présence de json dans l'arborescence de notre ordinateur
    # Retour attendu :
    # (Dico1) {NomFichierOuvert : (Liste)[(Dico2){Tache1 : valeur, ... , Tachex : valeur}, [processDic()]]}
    def test_findAllJson(self):
        #Créer un faux dico dans un faux dossier
        Folderpath = "testUnitaire"
        fakeDicoName = "dico1"
        os.mkdir(Folderpath)
        with open(f"./{Folderpath}/{fakeDicoName}.json", 'w') as f:
            fakeDico = {"Tache1":-1, "Tache2":6, "Tache3":7, "Tache4":-1}
            json_object = json.dumps(fakeDico, indent=len(fakeDico))
            f.write(json_object)

        #Comparaison
        ret = findAllJson(f"./{Folderpath}/")
        fakeReturn = {}
        fakeReturn[fakeDicoName] = [fakeDico, processDic(fakeDico)]
        self.assertEqual(ret, fakeReturn)

        #Supprimer le dico
        os.remove(f"./{Folderpath}/{fakeDicoName}.json")
        os.rmdir(Folderpath)
    
    def test_findAllJson_missingFolder(self):
        self.assertEqual(findAllJson("./FauxDossier/"), "Exception : Wrong json folder path")

    def test_writeJson(self):
        Folderpath = "testUnitaire"
        fakeDicoName = "dico1"
        fakeDico = {"Tache1":-1, "Tache2":6, "Tache3":7, "Tache4":-1}
        os.mkdir(Folderpath)
        writeJson(fakeDicoName, fakeDico, f"./{Folderpath}/")

        fakeRet = {}
        fakeRet[fakeDicoName] = [fakeDico, processDic(fakeDico)]
        self.assertEqual(findAllJson(f"./{Folderpath}/"), fakeRet)

        os.remove(f"./{Folderpath}/{fakeDicoName}.json")
        os.rmdir(Folderpath)

    def test_singleton_factory(self):
        factory = FactoryEvent()
        menu = factory.eventConstructor('Menu')
        preMain = factory.eventConstructor('preMain')

        self.assertEqual(menu.imp, preMain.imp)
        self.assertIs(menu.imp, preMain.imp)

if __name__ == '__main__':
    unittest.main()