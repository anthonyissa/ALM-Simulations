import matplotlib.pyplot as plt
import json
import io
import base64
import numpy as np

def get_amount(item):
    """Helper function to get amount from either 'montant' or 'total' field"""
    if 'montant' in item:
        return item['montant']
    elif 'total' in item:
        return item['total']
    return 0

def generate():
    # Load data
    with open('data/gap_taux_data.json', 'r') as file:
        data = json.load(file)
    
    actifs = data['gap_taux']['details']['actifs']
    passifs = data['gap_taux']['details']['passifs']
    
    # Calculer le total des actifs et passifs
    total_actifs = sum(get_amount(v) for v in actifs.values())
    total_passifs = sum(get_amount(v) for v in passifs.values())
    
    # Calculer le gap de liquidité
    gap = total_actifs - total_passifs
    
    # Créer le graphique
    plt.figure(figsize=(10, 6))
    
    # Créer les barres
    bars = plt.bar(['Actifs', 'Passifs'], [total_actifs, total_passifs], 
                  color=['blue', 'red'], alpha=0.6)
    
    # Personnaliser le graphique
    plt.title('Gap de Liquidité Global', pad=20)
    plt.ylabel('Montant (Milliards €)')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom')
    
    # Ajouter le gap
    plt.text(0.02, 0.95, f'Gap de Liquidité: {gap:.1f} Mrd €',
             transform=plt.gca().transAxes,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8') 