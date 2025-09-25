"""
TEST DE TOUS LES MODULES - Validation du fonctionnement
"""

import sys
import os

# Ajout du dossier src au chemin Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import charger_donnees_covid, extraire_donnees_pays
from analysis import calculer_taux_mortalite, comparer_pays
from visualizer import creer_graphique_barres
from reporter import generer_rapport_pays

def tester_tous_modules():
    """Test complet de tous les modules"""
    print(" TEST COMPLET DES MODULES")
    print("=" * 50)
    
    # Test data_loader
    print("1. Test du module data_loader...")
    df = charger_donnees_covid()
    assert df is not None, " Échec du chargement des données"
    print("    data_loader fonctionne")
    
    # Test analysis
    print("2. Test du module analysis...")
    donnees_fr = extraire_donnees_pays(df, "France")
    taux_fr = calculer_taux_mortalite(donnees_fr['deces_totaux'], donnees_fr['population'])
    assert taux_fr > 0, " Échec du calcul du taux"
    print("    analysis fonctionne")
    
    # Test reporter
    print("3. Test du module reporter...")
    rapport = generer_rapport_pays(donnees_fr, taux_fr)
    assert "France" in rapport, " Échec de la génération du rapport"
    print("    reporter fonctionne")
    
    print("\n TOUS LES TESTS SONT PASSÉS!")
    return True

if __name__ == "__main__":
    tester_tous_modules()