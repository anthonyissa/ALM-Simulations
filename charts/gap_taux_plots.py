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
    # Premier graphique (code existant)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    
    # --- Premier graphique (Gap de taux) ---
    with open('data/gap_taux_data.json', 'r') as file:
        data = json.load(file)
    
    actifs = data['gap_taux']['details']['actifs']
    passifs = data['gap_taux']['details']['passifs']
    
    actifs_sensibles = {k: get_amount(v) for k, v in actifs.items() if v.get('sensible_aux_taux', False)}
    passifs_sensibles = {k: get_amount(v) for k, v in passifs.items() if v.get('sensible_aux_taux', False)}
    
    all_categories = sorted(set(actifs_sensibles.keys()) | set(passifs_sensibles.keys()))
    actifs_values = [actifs_sensibles.get(cat, 0) for cat in all_categories]
    passifs_values = [passifs_sensibles.get(cat, 0) for cat in all_categories]
    
    x = np.arange(len(all_categories))
    width = 0.35
    
    ax1.bar(x - width/2, actifs_values, width, label='Actifs sensibles', color='blue', alpha=0.6)
    ax1.bar(x + width/2, passifs_values, width, label='Passifs sensibles', color='red', alpha=0.6)
    
    ax1.set_title('Gap de Taux - Actifs et Passifs Sensibles')
    ax1.set_xlabel('Catégories')
    ax1.set_ylabel('Montant (Milliards €)')
    ax1.set_xticks(x)
    ax1.set_xticklabels([name.replace('_', ' ').title() for name in all_categories], rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Ajout des valeurs sur les barres
    for i, v in enumerate(actifs_values):
        if v > 0:
            ax1.text(i - width/2, v, f'{v:.1f}', ha='center', va='bottom')
    for i, v in enumerate(passifs_values):
        if v > 0:
            ax1.text(i + width/2, v, f'{v:.1f}', ha='center', va='bottom')
    
    # --- Deuxième graphique (Impact des taux) ---
    with open('data/eve_npv_data.json', 'r') as file:
        eve_data = json.load(file)
    
    years = []
    baseline_values = []
    stress_minus = []
    stress_plus = []
    
    for metric in eve_data['metrics']:
        years.append(metric['year'])
        baseline_values.append(metric['EVE']['baseline'] / 1e9)  # Conversion en milliards
        stress_minus.append(metric['EVE']['stress_scenario_minus_200bps'] / 1e9)
        stress_plus.append(metric['EVE']['stress_scenario_plus_200bps'] / 1e9)
    
    ax2.plot(years, baseline_values, 'g-', label='Baseline', marker='o')
    ax2.plot(years, stress_minus, 'r--', label='-200 bps', marker='s')
    ax2.plot(years, stress_plus, 'b--', label='+200 bps', marker='^')
    
    ax2.set_title('Impact des Variations de Taux sur l\'EVE')
    ax2.set_xlabel('Années')
    ax2.set_ylabel('EVE (Milliards €)')
    ax2.legend()
    ax2.grid(True)
    
    # Ajout des valeurs sur les points
    for i, (base, minus, plus) in enumerate(zip(baseline_values, stress_minus, stress_plus)):
        ax2.text(years[i], base, f'{base:.1f}', ha='center', va='bottom')
        ax2.text(years[i], minus, f'{minus:.1f}', ha='center', va='bottom')
        ax2.text(years[i], plus, f'{plus:.1f}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8')