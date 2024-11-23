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
    
    # Get amounts for all assets and liabilities
    actifs_amounts = {k: get_amount(v) for k, v in actifs.items()}
    passifs_amounts = {k: get_amount(v) for k, v in passifs.items()}
    
    categories = sorted(set(actifs_amounts.keys()) | set(passifs_amounts.keys()))
    
    # Calculate differences
    differences = []
    for cat in categories:
        actif = actifs_amounts.get(cat, 0)
        passif = passifs_amounts.get(cat, 0)
        differences.append(actif - passif)
    
    plt.figure(figsize=(12, 6))
    
    colors = ['green' if x >= 0 else 'red' for x in differences]
    x = np.arange(len(categories))
    plt.bar(x, differences, color=colors, alpha=0.6)
    
    plt.title('Comparaison Actifs-Passifs par Catégorie', pad=20)
    plt.xlabel('Catégories')
    plt.ylabel('Différence (Milliards €)')
    
    plt.xticks(x, [name.replace('_', ' ').title() for name in categories], 
               rotation=45, ha='right')
    
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.grid(True, alpha=0.3, axis='y')
    
    for i, diff in enumerate(differences):
        if diff != 0:
            va = 'bottom' if diff >= 0 else 'top'
            plt.text(i, diff, f'{diff:.1f}', ha='center', va=va)
    
    total_diff = sum(differences)
    plt.text(0.02, 0.95, f'Différence Totale: {total_diff:.1f} Mrd €',
             transform=plt.gca().transAxes,
             bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8') 