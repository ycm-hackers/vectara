import requests
import json

# Constants for the Vectara API
API_KEY = "zwt_z2MupAEqaFNRDQhWISr9Yvt4g7X8_WM2MQa-Ng"  # Replace with your actual API key
CUSTOMER_ID = 3479383716  # Replace with your actual customer ID
CORPUS_ID = 3  # Replace with your actual corpus ID
API_ENDPOINT = "https://api.vectara.io/v1/query"  # Replace with the actual API endpoint if different

# Function to create the query JSON
def create_query_json(query_text):
    return json.dumps({
        "query": [
            {
                "query": query_text,
                "numResults": 10,
                "corpusKey": [
                    {
                        "customerId": CUSTOMER_ID,
                        "corpusId": CORPUS_ID
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

# Function to send the query to Vectara
def send_query(query_text):
    headers = {
        "customer-id": str(CUSTOMER_ID),
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(API_ENDPOINT, data=create_query_json(query_text), headers=headers)
    if response.status_code == 200:
        return response.json()  # You'll need to parse this JSON response appropriately.
    else:
        return f"Error: {response.text}"

# Main function for the chatbot
def main():
    print("Welcome to the Vectara Chatbot. Type 'exit' to leave the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response_json = send_query(user_input)
        if response_json.get("responseSet"):
            for response in response_json["responseSet"]:
                if response.get("summary"):
                    for summary in response["summary"]:
                        print("Bot:", summary["text"])
                else:
                    print("Bot: No summary available.")
        else:
            print("Bot:", json.dumps(response_json, indent=2))

if __name__ == "__main__":
    main()
