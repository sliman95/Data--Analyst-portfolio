"""
Module de création de visualisations pour les données COVID
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.analysis import formater_nombre

def configurer_style():
    """
    Configure le style des graphiques pour une apparence professionnelle
    """
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Configuration pour l'affichage en français
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

def creer_graphique_barres(donnees, titre, fichier_sortie=None):
    """
    Crée un graphique en barres pour comparer les pays
    
    Args:
        donnees (dict): Dictionnaire {pays: valeur}
        titre (str): Titre du graphique
        fichier_sortie (str): Chemin pour sauvegarder l'image
    """
    configurer_style()
    
    pays = list(donnees.keys())
    valeurs = list(donnees.values())
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(pays, valeurs, color=plt.cm.Set3(range(len(pays))))
    
    # Personnalisation
    plt.title(titre, fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Décès par million d\'habitants', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    # Ajout des valeurs sur les barres
    for i, valeur in enumerate(valeurs):
        plt.text(i, valeur + max(valeurs)*0.01, f'{valeur:.0f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Ajustement de l'espacement
    plt.tight_layout()
    
    # Sauvegarde si demandé
    if fichier_sortie:
        plt.savefig(f"outputs/{fichier_sortie}", dpi=300, bbox_inches='tight')
        print(f" Graphique sauvegardé : outputs/{fichier_sortie}")
    
    return plt

def creer_graphique_comparaison(donnees_comparaison, titre):
    """
    Crée un graphique de comparaison entre deux pays
    
    Args:
        donnees_comparaison (dict): Résultats de comparaison
        titre (str): Titre du graphique
    """
    configurer_style()
    
    pays = [donnees_comparaison['pays1'], donnees_comparaison['pays2']]
    taux = [donnees_comparaison['taux_mortalite1'], 
            donnees_comparaison['taux_mortalite2']]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Graphique à barres
    bars = ax1.bar(pays, taux, color=['#1f77b4', '#ff7f0e'])
    ax1.set_title('Comparaison des taux de mortalité', fontweight='bold')
    ax1.set_ylabel('Décès par million')
    ax1.grid(axis='y', alpha=0.3)
    
    # Ajout des valeurs
    for i, v in enumerate(taux):
        ax1.text(i, v + max(taux)*0.02, f'{v:.0f}', 
                ha='center', va='bottom', fontweight='bold')
    
    # Graphique de différence
    differences = [0, donnees_comparaison['difference_absolue']]
    ax2.bar(['', 'Différence'], differences, 
            color=['white', '#2ca02c'], edgecolor='black')
    ax2.set_title(f"Différence : {donnees_comparaison['difference_absolue']:.0f} décès/million", 
                 fontweight='bold')
    ax2.set_ylabel('Différence (décès/million)')
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle(titre, fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    return plt

def creer_camembert_taux_mortalite(donnees_groupe, titre):
    """
    Crée un camembert pour visualiser la répartition des taux
    
    Args:
        donnees_groupe (dict): Statistiques du groupe de pays
        titre (str): Titre du graphique
    """
    configurer_style()
    
    details = donnees_groupe['details']
    pays = list(details.keys())
    taux = [details[p]['taux_mortalite'] for p in pays]
    
    plt.figure(figsize=(10, 8))
    
    # Création du camembert
    wedges, texts, autotexts = plt.pie(taux, labels=pays, autopct='%1.1f%%',
                                      startangle=90, colors=plt.cm.Pastel1(range(len(pays))))
    
    # Personnalisation
    plt.title(titre, fontsize=16, fontweight='bold')
    
    # Amélioration des pourcentages
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # Légende avec les valeurs exactes
    legend_labels = [f'{p} : {t:.0f} décès/million' for p, t in zip(pays, taux)]
    plt.legend(wedges, legend_labels, title="Pays", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()
    return plt

# Test du module
if __name__ == "__main__":
    # Test avec des données fictives
    donnees_test = {
        'France': 2492,
        'Allemagne': 2102,
        'Italie': 3180,
        'Espagne': 2750
    }
    
    graphique = creer_graphique_barres(donnees_test, "Test Visualisation")
    plt.show()