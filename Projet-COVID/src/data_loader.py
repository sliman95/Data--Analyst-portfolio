"""
Module de chargement et de préparation des données COVID-19
"""

import pandas as pd
import requests
from datetime import datetime

# Constantes
COVID_DATA_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"

def charger_donnees_covid(url=COVID_DATA_URL):
    """
    Charge les données COVID depuis GitHub
    
    Returns:
        pandas.DataFrame: Données COVID ou None en cas d'erreur
    """
    try:
        print(f" Chargement des données depuis {url}")
        df = pd.read_csv(url)
        print(f" Données chargées : {len(df)} pays")
        return df
    except Exception as e:
        print(f" Erreur de chargement : {e}")
        return None

def filtrer_par_pays(df, liste_pays):
    """
    Filtre le DataFrame pour une liste de pays spécifique
    
    Args:
        df (pandas.DataFrame): Données complètes
        liste_pays (list): Liste des noms de pays
    
    Returns:
        pandas.DataFrame: Données filtrées
    """
    if df is None:
        print(" Aucune donnée à filtrer")
        return None
    
    pays_trouves = []
    pays_non_trouves = []
    
    for pays in liste_pays:
        if pays in df['location'].values:
            pays_trouves.append(pays)
        else:
            pays_non_trouves.append(pays)
    
    if pays_non_trouves:
        print(f"  Pays non trouvés : {', '.join(pays_non_trouves)}")
    
    df_filtre = df[df['location'].isin(pays_trouves)]
    print(f" {len(df_filtre)} pays filtrés avec succès")
    
    return df_filtre

def extraire_donnees_pays(df, nom_pays):
    """
    Extrait les données d'un pays spécifique
    
    Args:
        df (pandas.DataFrame): Données complètes ou filtrées
        nom_pays (str): Nom du pays
    
    Returns:
        dict: Dictionnaire avec les données du pays ou None si non trouvé
    """
    if df is None:
        return None
    
    pays_data = df[df['location'] == nom_pays]
    
    if len(pays_data) == 0:
        print(f" Aucune donnée pour le pays : {nom_pays}")
        return None
    
    # Extraction des valeurs principales
    ligne = pays_data.iloc[0]
    donnees = {
        'pays': nom_pays,
        'deces_totaux': ligne.get('total_deaths', 0),
        'population': ligne.get('population', 0),
        'cas_totaux': ligne.get('total_cases', 0),
        'vaccines': ligne.get('people_vaccinated', 0)
    }
    
    # Vérification de la disponibilité des données
    if pd.isna(donnees['deces_totaux']) or pd.isna(donnees['population']):
        print(f"  Données manquantes pour {nom_pays}")
        return None
    
    print(f" Données extraites pour {nom_pays}")
    return donnees

def sauvegarder_donnees_locales(df, nom_fichier="donnees_covid.csv"):
    """
    Sauvegarde les données dans un fichier CSV local
    
    Args:
        df (pandas.DataFrame): Données à sauvegarder
        nom_fichier (str): Nom du fichier de sauvegarde
    """
    try:
        chemin = f"data/{nom_fichier}"
        df.to_csv(chemin, index=False)
        print(f" Données sauvegardées : {chemin}")
    except Exception as e:
        print(f" Erreur de sauvegarde : {e}")

# Test du module
if __name__ == "__main__":
    # Test de chargement
    df_test = charger_donnees_covid()
    if df_test is not None:
        print(f"Colonnes disponibles : {list(df_test.columns)[:5]}...")
        
        # Test de filtrage
        pays_test = ["France", "Germany", "TestPaysInexistant"]
        df_filtre = filtrer_par_pays(df_test, pays_test)
        
        # Test d'extraction
        donnees_france = extraire_donnees_pays(df_test, "France")
        if donnees_france:
            print(f"Données France : {donnees_france}")