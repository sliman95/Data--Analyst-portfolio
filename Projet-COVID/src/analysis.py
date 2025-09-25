"""
Module d'analyse statistique des données COVID
"""

import pandas as pd
import numpy as np

def calculer_taux_mortalite(deces, population, multiplicateur=1000000):
    """
    Calcule le taux de mortalité standardisé
    
    Args:
        deces (int): Nombre total de décès
        population (int): Population totale
        multiplicateur (int): Base de calcul (par défaut 1 million)
    
    Returns:
        float: Taux de mortalité
    """
    if population is None or population <= 0:
        return 0
    
    if deces is None or deces < 0:
        return 0
    
    return (deces / population) * multiplicateur

def calculer_taux_vaccination(vaccines, population):
    """
    Calcule le taux de vaccination
    
    Args:
        vaccines (int): Nombre de personnes vaccinées
        population (int): Population totale
    
    Returns:
        float: Taux de vaccination (0-100)
    """
    if population is None or population <= 0:
        return 0
    
    if vaccines is None or vaccines < 0:
        return 0
    
    return (vaccines / population) * 100

def comparer_pays(donnees_pays1, donnees_pays2):
    """
    Compare deux pays et retourne les différences
    
    Args:
        donnees_pays1 (dict): Données du premier pays
        donnees_pays2 (dict): Données du deuxième pays
    
    Returns:
        dict: Résultats de la comparaison
    """
    if not donnees_pays1 or not donnees_pays2:
        return None
    
    # Calcul des taux pour les deux pays
    taux_mortalite1 = calculer_taux_mortalite(
        donnees_pays1['deces_totaux'], 
        donnees_pays1['population']
    )
    
    taux_mortalite2 = calculer_taux_mortalite(
        donnees_pays2['deces_totaux'], 
        donnees_pays2['population']
    )
    
    # Calcul de la différence
    difference_absolue = taux_mortalite1 - taux_mortalite2
    difference_pourcentage = 0
    
    if taux_mortalite2 > 0:
        difference_pourcentage = (difference_absolue / taux_mortalite2) * 100
    
    # Détermination du pays avec le taux le plus bas
    if taux_mortalite1 < taux_mortalite2:
        pays_meilleur = donnees_pays1['pays']
        avantage = taux_mortalite2 - taux_mortalite1
    else:
        pays_meilleur = donnees_pays2['pays']
        avantage = taux_mortalite1 - taux_mortalite2
    
    return {
        'pays1': donnees_pays1['pays'],
        'pays2': donnees_pays2['pays'],
        'taux_mortalite1': taux_mortalite1,
        'taux_mortalite2': taux_mortalite2,
        'difference_absolue': difference_absolue,
        'difference_pourcentage': difference_pourcentage,
        'pays_meilleur': pays_meilleur,
        'avantage': avantage
    }

def analyser_groupe_pays(df, liste_pays):
    """
    Analyse un groupe de pays et retourne des statistiques globales
    
    Args:
        df (pandas.DataFrame): Données complètes
        liste_pays (list): Liste des pays à analyser
    
    Returns:
        dict: Statistiques du groupe
    """
    from src.data_loader import extraire_donnees_pays
    
    taux_mortalite = []
    populations = []
    resultats_detailles = {}
    
    for pays in liste_pays:
        donnees = extraire_donnees_pays(df, pays)
        if donnees:
            taux = calculer_taux_mortalite(
                donnees['deces_totaux'], 
                donnees['population']
            )
            taux_mortalite.append(taux)
            populations.append(donnees['population'])
            resultats_detailles[pays] = {
                'taux_mortalite': taux,
                'population': donnees['population'],
                'deces_totaux': donnees['deces_totaux']
            }
    
    if not taux_mortalite:
        return None
    
    # Calcul des statistiques du groupe
    stats = {
        'nombre_pays': len(taux_mortalite),
        'taux_moyen': np.mean(taux_mortalite),
        'taux_median': np.median(taux_mortalite),
        'taux_min': min(taux_mortalite),
        'taux_max': max(taux_mortalite),
        'ecart_type': np.std(taux_mortalite),
        'population_totale': sum(populations),
        'pays_analyse': list(resultats_detailles.keys()),
        'details': resultats_detailles
    }
    
    return stats

def formater_nombre(nombre):
    """
    Formate un nombre avec des espaces pour les milliers
    
    Args:
        nombre (int/float): Nombre à formater
    
    Returns:
        str: Nombre formaté
    """
    try:
        return f"{nombre:,.0f}".replace(",", " ").replace(".", " ")
    except (ValueError, TypeError):
        return str(nombre)

# Test du module
if __name__ == "__main__":
    # Test des fonctions de calcul
    taux = calculer_taux_mortalite(1000, 500000)
    print(f"Taux de mortalité test : {taux:.1f}")
    
    # Test de formatage
    nombre_test = 1234567
    print(f"Formatage test : {formater_nombre(nombre_test)}")