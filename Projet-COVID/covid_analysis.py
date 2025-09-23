import pandas as pd

print(" Démarrage de l'analyse COVID...")

# Données simples pour tester
data = {
    'Pays': ['France', 'Allemagne'],
    'Décès': [167985, 174979],
    'Population': [67391582, 83237124]
}

df = pd.DataFrame(data)
df['Décès_par_million'] = (df['Décès'] / df['Population']) * 1000000

print(df)
print("✅ Analyse réussie !")