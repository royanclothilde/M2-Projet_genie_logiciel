"""
Created on Thu Nov 26 16:53:30 2020
@author: Clothilde Royan
"""

import psycopg2
import json


def ajouter_donnees():
    # Importation des accès à POSTGRE
    with open("./Configuration/postgre.json") as file:
        postgre = json.load(file)

    # Ouverture des fichiers nettoyés et organisés conformément à la BDD
    region = open("./Datas_finales/region.csv")
    temp = open("./Datas_finales/temp_2017.csv")
    conso = open("./Datas_finales/conso_2017.csv")
    relation = open("./Datas_finales/relation.csv")


    # Connection à la base de données
    conn = psycopg2.connect(
        host=postgre["host"],
        database=postgre["database"],
        user=postgre["user"],
        password=postgre["password"])
    # Création d'un curseur pour les requêtes
    cur = conn.cursor()

    # Importation des données
    cur.copy_from(region, 'region', sep=',')
    cur.copy_from(temp, 'temperature', sep=',')
    cur.copy_from(conso, 'consommation', sep=',')
    cur.copy_from(relation, "relation", sep=',')

    # On se déconnecte correctement
    cur.close()
    conn.commit()
    conn.close()
