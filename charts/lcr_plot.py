import matplotlib.pyplot as plt
import json
import io
import base64
import numpy as np

def calculate_lcr():
    with open('data/gap_taux_data.json', 'r') as file:
        data = json.load(file)
    
    # HQLA Niveau 1
    hqla_1 = (
        data['gap_taux']['details']['actifs']['tresorerie_et_comptes_banques_centrales']['montant'] +
        data['gap_taux']['details']['actifs']['titres_de_dette_detenus']['par_categorie']['administrations_centrales']
    )
    
    # HQLA Niveau 2 (avec décote de 15% sur les titres éligibles)
    hqla_2 = (
        data['gap_taux']['details']['actifs']['titres_de_dette_detenus']['par_categorie']['etablissements_credit'] * 0.85
    )
    
    total_hqla = hqla_1 + hqla_2
    
    # Sorties de trésorerie
    sorties = {
        'Dépôts Retail': data['gap_taux']['details']['passifs']['depots']['par_categorie']['menages'] * 0.05,
        'Dépôts Entreprises': data['gap_taux']['details']['passifs']['depots']['par_categorie']['snf'] * 0.25,
        'Dépôts Financiers': data['gap_taux']['details']['passifs']['depots']['par_categorie']['autres_entites_financieres'] * 0.40
    }
    
    total_sorties = sum(sorties.values())
    
    # Entrées de trésorerie
    entrees = {
        'Prêts Entreprises': data['gap_taux']['details']['actifs']['prets_et_avances']['par_categorie']['snf'] * 0.05,
        'Prêts Financiers': data['gap_taux']['details']['actifs']['prets_et_avances']['par_categorie']['autres_entites_financieres'] * 0.15
    }
    
    total_entrees = min(sum(entrees.values()), total_sorties * 0.75)
    sorties_nettes = total_sorties - total_entrees
    
    lcr = (total_hqla / sorties_nettes) * 100
    
    return {
        'hqla': {
            'Niveau 1': hqla_1,
            'Niveau 2': hqla_2
        },
        'flux': {
            'Sorties': sorties,
            'Entrées': entrees
        },
        'total_hqla': total_hqla,
        'sorties_nettes': sorties_nettes,
        'lcr': lcr
    }

def generate():
    lcr_data = calculate_lcr()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    
    # Premier graphique : Composition du HQLA
    hqla_data = lcr_data['hqla']
    bars = ax1.bar(['HQLA Niveau 1\n(Actifs les plus liquides)', 'HQLA Niveau 2\n(Actifs moins liquides)'], 
            [hqla_data['Niveau 1'], hqla_data['Niveau 2']], 
            color=['darkgreen', 'lightgreen'])
    
    ax1.set_title('Composition des HQLA (High Quality Liquid Assets)', pad=20)
    ax1.set_ylabel('Milliards €')
    ax1.grid(True, alpha=0.3)
    
    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f} Mrd €', ha='center', va='bottom')
    
    # Ajouter des annotations explicatives pour les HQLA
    ax1.text(-0.25, ax1.get_ylim()[1], 
             'HQLA Niveau 1:\n'
             '• Trésorerie et réserves banque centrale\n'
             '• Titres souverains\n'
             '• Pas de décote appliquée',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='darkgreen'),
             va='top')
    
    ax1.text(0.75, ax1.get_ylim()[1], 
             'HQLA Niveau 2:\n'
             '• Titres d\'établissements de crédit\n'
             '• Décote de 15% appliquée\n'
             '• Limité à 40% du total HQLA',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='lightgreen'),
             va='top')
    
    # Deuxième graphique : Entrées et Sorties
    flux_data = lcr_data['flux']
    categories = list(flux_data['Sorties'].keys()) + list(flux_data['Entrées'].keys())
    values = [-v for v in flux_data['Sorties'].values()] + list(flux_data['Entrées'].values())
    colors = ['red'] * len(flux_data['Sorties']) + ['green'] * len(flux_data['Entrées'])
    
    bars = ax2.bar(range(len(categories)), values, color=colors)
    ax2.set_xticks(range(len(categories)))
    ax2.set_xticklabels(categories, rotation=45, ha='right')
    ax2.set_title('Flux de Trésorerie Estimés sur 30 jours', pad=20)
    ax2.set_ylabel('Milliards €')
    ax2.grid(True, alpha=0.3)
    
    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., 
                height if height > 0 else height,
                f'{abs(height):.1f} Mrd €',
                ha='center', va='bottom' if height > 0 else 'top')
    
    # Ajouter des annotations pour les hypothèses de calcul
    ax2.text(0.02, ax2.get_ylim()[0], 
             'Hypothèses de sorties:\n'
             '• Dépôts retail: 5% de retrait\n'
             '• Dépôts entreprises: 25% de retrait\n'
             '• Dépôts financiers: 40% de retrait',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='red'),
             va='bottom')
    
    ax2.text(0.02, ax2.get_ylim()[1], 
             'Hypothèses d\'entrées:\n'
             '• Prêts entreprises: 5% de remboursement\n'
             '• Prêts financiers: 15% de remboursement\n'
             '• Plafonnées à 75% des sorties',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='green'),
             va='top')
    
    # Ajouter le LCR final avec explication
    plt.figtext(0.02, 0.95, 
                f'LCR = {lcr_data["lcr"]:.1f}%\n'
                f'(Minimum réglementaire: 100%)\n'
                f'HQLA Total: {lcr_data["total_hqla"]:.1f} Mrd €\n'
                f'Sorties nettes: {lcr_data["sorties_nettes"]:.1f} Mrd €', 
                fontsize=12, 
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8') 