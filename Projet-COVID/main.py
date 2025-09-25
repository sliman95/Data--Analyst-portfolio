"""
Script principal du projet COVID-19 Analysis
Auteur: [Votre Nom]
Date: [Date]
"""

import pandas as pd
from src.data_loader import charger_donnees_covid, filtrer_par_pays, extraire_donnees_pays
from src.analysis import calculer_taux_mortalite, comparer_pays, analyser_groupe_pays
from src.visualizer import creer_graphique_barres, creer_graphique_comparaison, creer_camembert_taux_mortalite
from src.reporter import generer_rapport_pays, generer_rapport_comparaison, generer_rapport_groupe, exporter_rapport_texte

def main():
    """
    Fonction principale du programme
    """
    print(" LANCEMENT DE L'ANALYSE COVID-19")
    print("="*60)
    
    # 1. CHARGEMENT DES DONNÉES
    print(" Étape 1: Chargement des données...")
    df = charger_donnees_covid()
    
    if df is None:
        print(" Impossible de charger les données. Arrêt du programme.")
        return
    
    # 2. DÉFINITION DES PAYS À ANALYSER
    pays_europe_principaux = ["France", "Germany", "Italy", "Spain", "United Kingdom", "Belgium", "Netherlands"]
    
    # 3. ANALYSE INDIVIDUELLE DES PAYS
    print("\n Étape 2: Analyse individuelle des pays...")
    resultats_pays = {}
    
    for pays in pays_europe_principaux[:3]:  # On analyse les 3 premiers pour l'exemple
        print(f"   • Analyse de {pays}...")
        donnees = extraire_donnees_pays(df, pays)
        
        if donnees:
            taux = calculer_taux_mortalite(donnees['deces_totaux'], donnees['population'])
            resultats_pays[pays] = taux
            
            # Génération du rapport individuel
            rapport = generer_rapport_pays(donnees, taux)
            print(rapport)
            
            # Export du rapport
            exporter_rapport_texte(rapport, f"rapport_{pays}.txt")
    
    # 4. COMPARAISON FRANCE-ALLEMAGNE
    print("\n Étape 3: Comparaison France-Allemagne...")
    donnees_france = extraire_donnees_pays(df, "France")
    donnees_allemagne = extraire_donnees_pays(df, "Germany")
    
    if donnees_france and donnees_allemagne:
        comparaison = comparer_pays(donnees_france, donnees_allemagne)
        
        if comparaison:
            rapport_comparaison = generer_rapport_comparaison(comparaison)
            print(rapport_comparaison)
            exporter_rapport_texte(rapport_comparaison, "comparaison_france_allemagne.txt")
            
            # Graphique de comparaison
            graphique = creer_graphique_comparaison(comparaison, "France vs Allemagne - Analyse COVID")
            graphique.savefig("outputs/comparaison_france_allemagne.png")
            graphique.show()
    
    # 5. ANALYSE DU GROUPE DE PAYS
    print("\n Étape 4: Analyse du groupe de pays...")
    stats_groupe = analyser_groupe_pays(df, pays_europe_principaux)
    
    if stats_groupe:
        rapport_groupe = generer_rapport_groupe(stats_groupe)
        print(rapport_groupe)
        exporter_rapport_texte(rapport_groupe, "rapport_groupe_europe.txt")
        
        # Graphique du groupe
        taux_par_pays = {pays: stats_groupe['details'][pays]['taux_mortalite'] 
                        for pays in stats_groupe['pays_analyse']}
        
        graphique_groupe = creer_graphique_barres(
            taux_par_pays, 
            "Taux de mortalité COVID en Europe",
            "europe_taux_mortalite.png"
        )
        graphique_groupe.show()
        
        # Camembert
        camembert = creer_camembert_taux_mortalite(stats_groupe, "Répartition des taux de mortalité")
        camembert.savefig("outputs/camembert_europe.png")
        camembert.show()
    
    # 6. RAPPORT FINAL
    print("\n  Étape 5: Génération du rapport final...")
    rapport_final = f"""
{'='*70}
  RAPPORT FINAL - ANALYSE COVID-19 EUROPE
{'='*70}

  SYNTHÈSE
   • Pays analysés : {len(pays_europe_principaux)}
   • Données source : Our World in Data
   • Période : Données les plus récentes disponibles

  CONCLUSION
   Cette analyse démontre les variations significatives des taux de mortalité
   COVID-19 entre les pays européens, mettant en lumière l'importance des
   comparaisons standardisées pour une analyse épidémiologique rigoureuse.

  MÉTHODOLOGIE
   • Taux calculés par million d'habitants
   • Données standardisées pour une comparaison équitable
   • Analyse statistique descriptive complète

{'='*70}
  Analyse réalisée le {pd.Timestamp.now().strftime('%d/%m/%Y à %H:%M')}
{'='*70}
"""
    print(rapport_final)
    exporter_rapport_texte(rapport_final, "rapport_final.txt")
    
    print(" ANALYSE TERMINÉE AVEC SUCCÈS!")
    print(" Consultez le dossier 'outputs/' pour les résultats détaillés")

if __name__ == "__main__":
    main()