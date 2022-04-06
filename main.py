"""
Created on Tue Dec 8 09:52:30 2020
@author: Clothilde Royan
"""

from Code import Extraction
from Code import Nettoyage
from Code import Ajout_BDD

print("Extraction des données 2017")
Extraction.extraction_conso()
Extraction.extraction_temp()

print("\nNettoyage des données")
Nettoyage.nettoyage_conso()
Nettoyage.nettoyage_temp()
Nettoyage.creation_relation()

print("\nAjout des données à la BDD")
Ajout_BDD.ajouter_donnees()
print("Ajout des données dans la base terminé")