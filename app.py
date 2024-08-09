from flask import Flask, render_template, send_file
import pandas as pd
import numpy as np
from io import BytesIO
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

# Generate a sample DataFrame with 50 columns and 100 rows
np.random.seed(0)  # For reproducibility
dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
data = np.random.randn(100, 50)  # Random data for 50 columns
columns = [f'Column_{i}' for i in range(1, 51)]
df = pd.DataFrame(data, columns=columns, index=dates)

# Add some identifiable columns for demonstration
df['Time'] = df.index.time
df['Spot Price'] = np.random.uniform(90, 110, size=100)
df['Call Change OI'] = np.random.randint(100, 300, size=100)
df['Put Change OI'] = np.random.randint(100, 300, size=100)
df['PCR'] = df['Call Change OI'] / (df['Call Change OI'] + df['Put Change OI'])

@app.route('/')
def index():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Spot Price'], mode='lines+markers', name='Spot Price'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Call Change OI'], mode='lines+markers', name='Call Change OI'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Put Change OI'], mode='lines+markers', name='Put Change OI'))
    
    fig.update_layout(title='Interactive Data Plot',
                      xaxis_title='Date',
                      yaxis_title='Values',
                      template='plotly_dark')
    
    plot_html = pio.to_html(fig, full_html=False)
    
    # Convert the DataFrame to HTML with pagination
    table_html = df.to_html(classes='table table-dark table-striped', index=True)  # Display all rows
    
    return render_template('index.html', table=table_html, plot=plot_html)

@app.route('/download_csv')
def download_csv():
    csv = df.to_csv()
    return send_file(BytesIO(csv.encode()), attachment_filename='data.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
