"""
Created on Thu Nov 26 15:07:25 2020
@author: Clothilde Royan
"""

import pandas as pd


def extraction_conso():
    # Importation des données
    data = pd.read_csv("./Datas/conso_quotidienne.csv", sep=";")
    data['Date'] = pd.to_datetime(data['Date'])

    # Sélection des données de 2017
    start_date = "01/01/2017"
    end_date = "31/12/2017"
    mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
    data_2017 = data.loc[mask]

    # Sélection des données pertinentes
    data_2017 = data_2017.loc[:, ["Date", "Heure", "Code INSEE région", "Consommation brute gaz totale (MW PCS 0°C)",
                                  "Consommation brute totale (MW)"]]

    data_2017.columns = ["date", "heure", "code_insee_region", "consommation gaz", "consommation electricite"]
    data_2017.reset_index(drop=True, inplace=True)

    # Exportation au format csv pour une execution plus rapide
    data_2017.to_csv("./Datas/conso_2017.csv", index=False, header=False)
    print("Extraction des données de conso 2017 terminée")


def extraction_temp():
    # Importation des données
    data = pd.read_csv("./Datas/temp_quotidienne.csv", sep=";")
    data['date'] = pd.to_datetime(data['date'])

    # Sélection des données de 2017
    start_date = "01/01/2017"
    end_date = "31/12/2017"
    mask = (data['date'] >= start_date) & (data['date'] <= end_date)
    data_2017 = data.loc[mask]

    # Sélection des données pertinentes
    region = data_2017.loc[:, ["code_insee_region", "region"]]
    region.columns = ["code_insee_region", "region"]
    region.reset_index(drop=True, inplace=True)

    data_2017 = data_2017.loc[:, ["date", "code_insee_region", "tmoy", "tmin", "tmax"]]
    data_2017.columns = ["date", "code_insee_region", "temperaturemoy", "temperaturemin", "temperaturemax"]

    # Récupération des noms de régions associé au code
    code_region = {}
    for i in range(len(region)):
        if region["code_insee_region"][i] not in code_region and region["code_insee_region"][i] != 94:
            code_region[region["code_insee_region"][i]] = region["region"][i]

    # Création d'un dataframe avec les données des régions
    data_region = pd.DataFrame(list(code_region.items()), columns=['coderegion', 'nomregion'])

    # Exportation au format csv
    data_2017.to_csv("./Datas/temp_2017.csv", index=False)

    # Sauvegarde du dataframe au format csv pour la mettre dans la BDD
    data_region.to_csv("./Datas_finales/region.csv", index=False, header=False)
    print("Extraction des données de température 2017 et régions terminée")
