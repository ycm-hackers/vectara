#main.py

import subprocess
import json
import requests
import toml

def create_query_json(query_text, customer_id, corpus_id):
    return json.dumps({
        "query": [
            {
                "query": query_text,
                "numResults": 10,
                "corpusKey": [
                    {
                        "customerId": customer_id,
                        "corpusId": corpus_id
                    }
                ],
                "summary": [
                    {
                        "summarizerPromptName": "vectara-summary-ext-v1.2.0",
                        "responseLang": "en",
                        "maxSummarizedResults": 5
                    }
                ]
            }
        ]
    })

def send_query(query_text, api_key, customer_id, corpus_id):
    api_endpoint = "https://api.vectara.io/v1/query"
    headers = {
        "customer-id": str(customer_id),
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(api_endpoint, data=create_query_json(query_text, customer_id, corpus_id), headers=headers)
    return response.json() if response.status_code == 200 else None

def format_response(response_json):
    responses = []
    if response_json and "responseSet" in response_json:
        for response in response_json["responseSet"]:
            if "summary" in response:
                for summary in response["summary"]:
                    responses.append(summary["text"])
            else:
                responses.append("No summary available.")
    else:
        responses.append("I'm sorry, I couldn't fetch the data.")
    return ' '.join(responses)

def main():
    secrets = toml.load("secrets.toml")["default"]
    api_key = secrets["api_key"]
    customer_id = secrets["customer_id"]
    corpus_id = secrets["corpus_id"]

    ticker = input("Enter the ticker for the company you want to crawl: ").upper()
    subprocess.run(["python", "ingest.py", ticker])
    
    print("Crawl finished. You can now chat with the data.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response_json = send_query(user_input, api_key, customer_id, corpus_id)
        print(format_response(response_json))

if __name__ == "__main__":
    main()