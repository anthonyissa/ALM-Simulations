import matplotlib.pyplot as plt
import io
import json
import base64
import numpy as np

def generate():
    # Load JSON data
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    years = data['years']
    
    # Créer un dictionnaire avec les composantes du PNB (sans le PNB total)
    components = {
        'MNI': data['data']['MNI'],
        'Commissions': data['data']['Commissions'],
        'Revenus_Activites_Marches': data['data']['Revenus_Activites_Marches'],
        'Autres_Revenus': data['data']['Autres_Revenus']
    }
    
    plt.figure(figsize=(12, 6))
    
    bottom = np.zeros(len(years))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # Couleurs personnalisées
    
    # Créer les barres empilées
    for i, (label, values) in enumerate(components.items()):
        plt.bar(years, values, bottom=bottom, label=label, color=colors[i])
        bottom += np.array(values)
    
    plt.title('Décomposition du PNB')
    plt.xlabel('Années')
    plt.ylabel('Milliards €')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Ajouter les valeurs totales (PNB) au-dessus de chaque barre
    pnb_values = data['data']['PNB']
    for i, v in enumerate(pnb_values):
        plt.text(years[i], v, f'{v}', ha='center', va='bottom')
    
    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8') 