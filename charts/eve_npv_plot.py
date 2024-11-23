import matplotlib.pyplot as plt
import json
import io
import base64
import numpy as np

def generate():
    # Charger les données
    with open('data/eve_npv_data.json', 'r') as file:
        data = json.load(file)
    
    metrics = data['metrics']
    years = [m['year'] for m in metrics]
    
    # Créer une figure avec plusieurs sous-graphiques
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Graphique EVE
    baseline = [m['EVE']['baseline'] / 1e9 for m in metrics]  # Conversion en milliards
    minus_200bps = [m['EVE']['stress_scenario_minus_200bps'] / 1e9 for m in metrics]
    plus_200bps = [m['EVE']['stress_scenario_plus_200bps'] / 1e9 for m in metrics]
    
    ax1.plot(years, baseline, 'b-', label='Baseline', marker='o')
    ax1.plot(years, minus_200bps, 'r--', label='-200bps', marker='s')
    ax1.plot(years, plus_200bps, 'g--', label='+200bps', marker='^')
    ax1.set_title('Economic Value of Equity (EVE) Evolution')
    ax1.set_ylabel('Milliards €')
    ax1.grid(True)
    ax1.legend()
    
    # Graphique NPV
    assets = [m['NPV']['assets'] / 1e9 for m in metrics]
    liabilities = [m['NPV']['liabilities'] / 1e9 for m in metrics]
    npv = [m['NPV']['net_present_value'] / 1e9 for m in metrics]
    
    ax2.bar(years, assets, label='Assets', alpha=0.6, color='blue')
    ax2.bar(years, liabilities, label='Liabilities', alpha=0.6, color='red')
    ax2.plot(years, npv, 'g-', label='Net Present Value', linewidth=2, marker='o')
    
    # Ajouter les valeurs sur les barres
    for i, (a, l) in enumerate(zip(assets, liabilities)):
        ax2.text(years[i], a/2, f'{a:.1f}', ha='center', va='center')
        ax2.text(years[i], l/2, f'{l:.1f}', ha='center', va='center')
    
    ax2.set_title('Net Present Value Components')
    ax2.set_ylabel('Milliards €')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    
    # Sauvegarder le graphique dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8') 