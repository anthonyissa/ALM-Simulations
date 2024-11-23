import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def generate(x_values, data_dict, title="Stacked Bar Plot", xlabel="X axis", ylabel="Y axis"):
    """
    Generate a stacked bar plot
    
    Parameters:
    - x_values: list of x-axis values
    - data_dict: dictionary where keys are series names and values are lists of data
    - title: plot title
    - xlabel: x-axis label
    - ylabel: y-axis label
    """
    plt.figure(figsize=(8, 5))
    
    bottom = np.zeros(len(x_values))
    colors = plt.cm.Set3(np.linspace(0, 1, len(data_dict)))
    
    for i, (label, values) in enumerate(data_dict.items()):
        plt.bar(x_values, values, bottom=bottom, label=label, color=colors[i])
        bottom += np.array(values)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    # Add total values on top of each bar
    for i in range(len(x_values)):
        plt.text(x_values[i], bottom[i], f'{bottom[i]:.1f}', 
                ha='center', va='bottom')
    
    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8') 