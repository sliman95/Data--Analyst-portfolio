"""
Module de génération de rapports textuels et export de données
"""

import pandas as pd
from datetime import datetime
from src.analysis import formater_nombre

def generer_rapport_pays(donnees_pays, taux_mortalite):
    """
    Génère un rapport détaillé pour un pays
    
    Args:
        donnees_pays (dict): Données du pays
        taux_mortalite (float): Taux calculé
    
    Returns:
        str: Rapport formaté
    """
    if not donnees_pays:
        return " Données manquantes pour générer le rapport"
    
    rapport = f"""
{'='*60}
  RAPPORT DÉTAILLÉ - {donnees_pays['pays'].upper()}
{'='*60}

  DONNÉES DÉMOGRAPHIQUES
   • Population totale : {formater_nombre(donnees_pays['population'])} habitants
   • Décès COVID totaux : {formater_nombre(donnees_pays['deces_totaux'])}
   • Cas COVID totaux : {formater_nombre(donnees_pays.get('cas_totaux', 'N/A'))}

  ANALYSE STATISTIQUE
   • Taux de mortalité : {taux_mortalite:,.1f} décès par million d'habitants
   • Ratio : 1 décès pour {formater_nombre(int(donnees_pays['population'] / donnees_pays['deces_totaux']))} habitants

  PERSPECTIVE
   Ce taux signifie qu'en {donnees_pays['pays']}, environ {int(taux_mortalite/1000)} personnes 
   sur 1000 sont décédées du COVID-19 depuis le début de la pandémie.

{'='*60}
  Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
{'='*60}
"""
    return rapport

def generer_rapport_comparaison(donnees_comparaison):
    """
    Génère un rapport de comparaison entre deux pays
    
    Args:
        donnees_comparaison (dict): Résultats de la comparaison
    
    Returns:
        str: Rapport formaté
    """
    if not donnees_comparaison:
        return " Données de comparaison manquantes"
    
    rapport = f"""
{'='*70}
  RAPPORT COMPARATIF
   {donnees_comparaison['pays1']} vs {donnees_comparaison['pays2']}
{'='*70}

  TAUX DE MORTALITÉ
   • {donnees_comparaison['pays1']} : {donnees_comparaison['taux_mortalite1']:,.1f} décès/million
   • {donnees_comparaison['pays2']} : {donnees_comparaison['taux_mortalite2']:,.1f} décès/million

  DIFFÉRENCES
   • Différence absolue : {donnees_comparaison['difference_absolue']:+,.1f} décès/million
   • Différence relative : {donnees_comparaison['difference_pourcentage']:+.1f}%

  ANALYSE
   • Meilleur résultat : {donnees_comparaison['pays_meilleur']}
   • Avantage : {donnees_comparaison['avantage']:.1f} décès/million en moins

  INTERPRÉTATION
   Le taux de mortalité de {donnees_comparaison['pays1']} est 
   {abs(donnees_comparaison['difference_pourcentage']):.1f}% 
   {'plus élevé' if donnees_comparaison['difference_pourcentage'] > 0 else 'plus bas'} 
   que celui de {donnees_comparaison['pays2']}.

{'='*70}
"""
    return rapport

def generer_rapport_groupe(donnees_groupe):
    """
    Génère un rapport pour un groupe de pays
    
    Args:
        donnees_groupe (dict): Statistiques du groupe
    
    Returns:
        str: Rapport formaté
    """
    if not donnees_groupe:
        return " Données de groupe manquantes"
    
    rapport = f"""
{'='*70}
  ANALYSE DE GROUPE ({donnees_groupe['nombre_pays']} pays)
{'='*70}

  STATISTIQUES GLOBALES
   • Nombre de pays analysés : {donnees_groupe['nombre_pays']}
   • Population totale : {formater_nombre(donnees_groupe['population_totale'])} habitants
   • Taux de mortalité moyen : {donnees_groupe['taux_moyen']:,.1f} décès/million
   • Taux médian : {donnees_groupe['taux_median']:,.1f} décès/million

  DISTRIBUTION
   • Taux minimum : {donnees_groupe['taux_min']:,.1f} décès/million
   • Taux maximum : {donnees_groupe['taux_max']:,.1f} décès/million
   • Écart-type : {donnees_groupe['ecart_type']:,.1f} décès/million

  PAYS ANALYSÉS
   • {", ".join(donnees_groupe['pays_analyse'])}
  CONTEXTE
   L'écart-type de {donnees_groupe['ecart_type']:.1f} indique une variation 
   {'faible' if donnees_groupe['ecart_type'] < 500 else 'modérée' if donnees_groupe['ecart_type'] < 1000 else 'importante'} 
   entre les pays du groupe.

{'='*70}
"""
    return rapport

def exporter_rapport_texte(contenu, nom_fichier):
    """
    Exporte un rapport vers un fichier texte
    
    Args:
        contenu (str): Contenu du rapport
        nom_fichier (str): Nom du fichier de sortie
    """
    try:
        chemin = f"outputs/{nom_fichier}"
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(contenu)
        print(f" Rapport exporté : {chemin}")
        return True
    except Exception as e:
        print(f" Erreur d'export : {e}")
        return False

def exporter_donnees_csv(donnees, nom_fichier):
    """
    Exporte des données vers un fichier CSV
    
    Args:
        donnees (dict/list): Données à exporter
        nom_fichier (str): Nom du fichier de sortie
    """
    try:
        chemin = f"outputs/{nom_fichier}"
        
        if isinstance(donnees, dict):
            # Convertir le dictionnaire en DataFrame
            df = pd.DataFrame([donnees])
        elif isinstance(donnees, list):
            df = pd.DataFrame(donnees)
        else:
            print(" Format de données non supporté")
            return False
        
        df.to_csv(chemin, index=False, encoding='utf-8')
        print(f" Données exportées : {chemin}")
        return True
    except Exception as e:
        print(f" Erreur d'export CSV : {e}")
        return False

# Test du module
if __name__ == "__main__":
    # Test avec des données fictives
    donnees_test = {
        'pays': 'France',
        'population': 67391582,
        'deces_totaux': 167985
    }
    
    rapport = generer_rapport_pays(donnees_test, 2492.6)
    print(rapport)