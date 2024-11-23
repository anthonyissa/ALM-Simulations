from flask import Flask, render_template
from lib import line_plot, scatter_plot, bar_plot

app = Flask(__name__)

@app.route('/')
def home():
    plots = {
        'line_plot': line_plot.generate(),
        'scatter_plot': scatter_plot.generate(),
        'bar_plot': bar_plot.generate()
    }
    return render_template('index.html', plots=plots)

if __name__ == '__main__':
    app.run(debug=True) 