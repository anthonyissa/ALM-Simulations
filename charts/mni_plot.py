import matplotlib.pyplot as plt
import io
import json
import base64
import numpy as np

def generate():
    # Load JSON data
    with open('data/banking_data.json', 'r') as file:
        data = json.load(file)
    
    plt.figure(figsize=(8, 5))
    
    # Plot MNI data
    years = data['years']
    mni_values = data['data']['MNI']
    
    plt.plot(years, mni_values, 'b-', label='MNI')
    plt.title('Évolution du MNI')
    plt.xlabel('Années')
    plt.ylabel('MNI (en milliards €)')
    plt.grid(True)
    plt.legend()

    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8')