import matplotlib.pyplot as plt
import io
import json
import base64
import numpy as np

def generate():
    # Load JSON data
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    plt.figure(figsize=(10, 6))
    
    years = data['years']
    mni_values = data['data']['MNI']
    pnb_values = data['data']['PNB']
    
    # Calculer le pourcentage du MNI par rapport au PNB
    mni_percentage = [mni/pnb*100 for mni, pnb in zip(mni_values, pnb_values)]
    
    # Créer un graphique avec deux axes Y
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Premier axe pour les valeurs absolues
    ax1.bar(years, pnb_values, alpha=0.3, color='gray', label='PNB Total')
    ax1.bar(years, mni_values, color='blue', label='MNI')
    ax1.set_xlabel('Années')
    ax1.set_ylabel('Milliards €')
    
    # Deuxième axe pour le pourcentage
    ax2 = ax1.twinx()
    ax2.plot(years, mni_percentage, 'r--', label='% MNI/PNB', linewidth=2)
    ax2.set_ylabel('% MNI/PNB')
    
    # Ajouter les pourcentages au-dessus des points
    for i, pct in enumerate(mni_percentage):
        ax2.text(years[i], pct, f'{pct:.1f}%', ha='center', va='bottom')
    
    # Combiner les légendes des deux axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.title('Influence du MNI sur le PNB')
    plt.grid(True, alpha=0.3)
    
    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8') 