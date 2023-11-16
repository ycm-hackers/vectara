#app.py

from flask import Flask, render_template, request, redirect, url_for
import main
import ingest
import logging
import toml

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ticker', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        logging.info(f"Received ticker: {ticker}")
        ingest.main(ticker)
        logging.info("Redirecting to query page")
        return redirect(url_for('query'))

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        query_text = request.form.get('query')
        secrets = toml.load("secrets.toml")["default"]
        api_key = secrets["api_key"]
        customer_id = secrets["customer_id"]
        corpus_id = secrets["corpus_id"]
        response_json = main.send_query(query_text, api_key, customer_id, corpus_id)
        if response_json:
            formatted_response = main.format_response(response_json)
            return {"response": formatted_response}
        else:
            return {"error": "No response received from the query"}, 500
    else:
        return {"error": "This page is not accessible via GET request"}, 405

if __name__ == '__main__':
    app.run(debug=True)