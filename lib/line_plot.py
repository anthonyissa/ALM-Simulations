import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def generate():
    plt.figure(figsize=(8, 5))
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y, 'b-', label='Sine Wave')
    plt.title('Simple Line Plot')
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