import matplotlib.pyplot as plt
import json
import io
import base64
import numpy as np

def generate():
    with open('data/rwa_market_data.json', 'r') as file:
        data = json.load(file)
    
    dates = data['dates']
    risque_change = data['risques']['change']['valeurs']
    risque_taux = data['risques']['taux']['valeurs']
    
    plt.figure(figsize=(12, 6))
    
    bottom = np.zeros(len(dates))
    
    # Risque de change
    plt.bar(dates, risque_change, bottom=bottom, label='Risque de Change',
            color='gold', alpha=0.7)
    bottom += np.array(risque_change)
    
    # Risque de taux
    plt.bar(dates, risque_taux, bottom=bottom, label='Risque de Taux',
            color='hotpink', alpha=0.7)
    
    plt.title('Contribution aux RWA Marché par Type de Risque', pad=20)
    plt.xlabel('Dates')
    plt.ylabel('Contribution aux RWA (%)')
    plt.grid(True, alpha=0.3, axis='y')
    plt.legend()
    
    plt.xticks(rotation=45, ha='right')
    
    # Ajouter les valeurs totales
    for i in range(len(dates)):
        total = risque_change[i] + risque_taux[i]
        plt.text(i, total, f'{total:.0f}%', ha='center', va='bottom')
    
    # Ajouter une annotation détaillée
    plt.text(0.02, 0.95, 
             'Impact sur les RWA marché:\n'
             '• Risque de change: exposition aux variations\n  des taux de change (8-22%)\n'
             '• Risque de taux: sensibilité aux variations\n  des taux d\'intérêt (45-60%)\n'
             '• Total: contribution aux exigences\n  en fonds propres',
             transform=plt.gca().transAxes,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'),
             va='top')
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8') 