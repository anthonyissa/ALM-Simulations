from flask import Flask, render_template

from lib import line_plot, scatter_plot, bar_plot
from charts import mni_plot, pnb_decomposition, mni_proportion_plot, eve_npv_plot, gap_taux_plots

app = Flask(__name__)

@app.route('/')
def home():
    plots = {
        'line_plot': line_plot.generate(),
        'scatter_plot': scatter_plot.generate(),
        'bar_plot': bar_plot.generate(),
        'mni_plot': mni_plot.generate(),
        'pnb_decomposition': pnb_decomposition.generate(),
        'mni_proportion': mni_proportion_plot.generate(),
        'eve_npv_plot': eve_npv_plot.generate(),
        'gap_taux_plot': gap_taux_plots.generate()
    }
    return render_template('index.html', plots=plots)

if __name__ == '__main__':
    app.run(debug=True) 