"""
ANALYSE COVID SIMPLIFIÉE - Point d'entrée pour tests rapides
Version simplifiée utilisant nos nouveaux modules
"""

from src.data_loader import charger_donnees_covid, extraire_donnees_pays
from src.analysis import calculer_taux_mortalite, formater_nombre

def analyse_rapide():
    """Version rapide et simple de l'analyse"""
    print(" ANALYSE COVID RAPIDE")
    print("=" * 40)
    
    # Chargement des données
    df = charger_donnees_covid()
    if df is None:
        return
    
    # Analyse France vs Allemagne (notre exemple original)
    pays_a_analyser = ["France", "Germany"]
    
    for pays in pays_a_analyser:
        donnees = extraire_donnees_pays(df, pays)
        if donnees:
            taux = calculer_taux_mortalite(donnees['deces_totaux'], donnees['population'])
            print(f"\n {pays}:")
            print(f"   Population: {formater_nombre(donnees['population'])}")
            print(f"   Décès: {formater_nombre(donnees['deces_totaux'])}")
            print(f"   Taux: {taux:.1f} décès/million")
    
    print("\n Analyse rapide terminée!")

if __name__ == "__main__":
    analyse_rapide()