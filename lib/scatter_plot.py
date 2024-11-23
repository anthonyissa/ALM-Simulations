import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def generate():
    plt.figure(figsize=(8, 5))
    # Generate random data
    np.random.seed(42)
    x = np.random.normal(0, 1, 100)
    y = np.random.normal(0, 1, 100)
    
    plt.scatter(x, y, alpha=0.5, label='Random Points')
    plt.title('Scatter Plot')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.grid(True)
    plt.legend()

    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8') 