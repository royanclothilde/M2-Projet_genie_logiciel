"""
Created on Wed Nov 25 20:25:13 2020
@author: Clothilde Royan
"""

import pandas as pd
import numpy as np
from datetime import datetime


def nettoyage_conso():
    # Importation des données
    data = pd.read_csv("./Datas/conso_2017.csv")
    data.columns = ["date", "heure", "code_insee_region", "consommation gaz", "consommation electricite"]

    print("\t\t ## Nettoyage Conso ##")
    print("Avant nettoyage, il existe des valeurs nulles : ", data.isnull().values.any())
    if data.isnull().values.any():
        data = data.fillna(0)  # Remplace les "NaN" par des 0

        region = [28, 11, 32, 53, 52, 24, 44, 84, 27, 93, 75, 76]
        consommation = dict()
        conso_net = pd.DataFrame(columns=["id_conso", "date", "code_insee_region", "consommation gaz",
                                          "consommation electricite"])
        j = 0

        # Pour chaque région
        for r in region:
            for i in range(len(data)):
                if data["code_insee_region"][i] == r:
                    # On récupère la consommation suivant la date
                    if data["date"][i] not in consommation:
                        consommation[data["date"][i]] = [[data["consommation gaz"][i],
                                                          data["consommation electricite"][i]]]
                    else:
                        consommation[data["date"][i]].append([data["consommation gaz"][i],
                                                              data["consommation electricite"][i]])

            # Pour chaque date on calcule la consommation totale de gaz et d'électricité
            for d in consommation:
                conso_gaz = 0
                conso_elec = 0
                for i in consommation[d]:
                    conso_gaz += i[0]
                    conso_elec += i[1]
                conso_net.loc[j] = [j+1, d, r, conso_gaz, conso_elec]
                j += 1
        print("Après nettoyage, il existe des valeurs nulles : ", data.isnull().values.any())

        # Sauvegarde du dataframe au format csv pour la mettre dans la BDD
        conso_net.to_csv("./Datas_net/conso_2017.csv", index=False)
        print("Nettoyage des données de consommations terminé")


def nettoyage_temp():
    # Importation des données
    data = pd.read_csv("./Datas/temp_2017.csv")

    print("\t\t ## Nettoyage Température ##")
    print("Avant nettoyage, il existe des valeurs nulles : ", data.isnull().values.any())

    # Après examen, il apparait qu'il n'y a pas de données de conso pour la corse, il faut donc les enlever
    temp = data.loc[(data["code_insee_region"] != 94)]
    temp["id_temp"] = np.arange(1, len(temp)+1)

    # Sauvegarde du dataframe au format csv pour la mettre dans la BDD
    temp.to_csv("./Datas_net/temp_2017.csv", index=False)
    print("Nettoyage des données de température terminé")


def creation_relation():
    print("\t\t ## Création des relations ##")
    start_time = datetime.now()
    conso = pd.read_csv("./Datas_net/conso_2017.csv")
    temp = pd.read_csv("./Datas_net/temp_2017.csv")

    relation = pd.DataFrame(columns=["coderegion", "idconsommation", "idtemperature", "date"])
    id_temp = []
    code = []
    id_conso = []
    date = []

    for i in range(len(conso)):
        for j in range(len(temp)):
            if temp["date"][j] == conso["date"][i] and temp["code_insee_region"][j] == conso["code_insee_region"][i]:
                id_temp.append(temp["id_temp"][j])
                code.append(temp["code_insee_region"][j])
                id_conso.append(conso["id_conso"][i])
                date.append(temp["date"][j])

    relation["idtemperature"] = id_temp
    relation["coderegion"] = code
    relation["idconsommation"] = id_conso
    relation["date"] = date

    conso = conso.loc[:, ["id_conso", "consommation gaz", "consommation electricite"]]
    temp = temp.loc[:, ["id_temp", "temperaturemoy", "temperaturemin", "temperaturemax"]]

    temp.to_csv("./Datas_finales/temp_2017.csv", index=False, header=False)
    conso.to_csv("./Datas_finales/conso_2017.csv", index=False, header=False)
    relation.to_csv("./Datas_finales/relation.csv", index=False, header=False)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))