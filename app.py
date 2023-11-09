# app.py
from flask import Flask, render_template, request, redirect, url_for
import main
import ingest

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ticker', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        ingest.main(ticker)
        return redirect(url_for('query'))
    

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        query_text = request.form.get('query')
        response_json = main.send_query(query_text)
        response = main.format_response(response_json)
        return response_json

if __name__ == '__main__':
    app.run(debug=True)