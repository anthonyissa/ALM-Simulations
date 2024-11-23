import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def generate():
    plt.figure(figsize=(8, 5))
    categories = ['A', 'B', 'C', 'D', 'E']
    values = np.random.randint(1, 30, size=5)
    
    plt.bar(categories, values, color='skyblue')
    plt.title('Bar Plot')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.grid(True, axis='y')

    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8') 