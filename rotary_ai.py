from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from elasticsearch import Elasticsearch
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Keys
es_api_key = os.getenv("ES_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Validate API keys
if not es_api_key or not openai_api_key:
    raise ValueError("Missing API keys! Please set ES_API_KEY and OPENAI_API_KEY in the .env file.")

# Initialize Flask app and configure CORS for your Wix domain
app = Flask(__name__)
CORS(app)

# Connect to Elasticsearch
es_client = Elasticsearch(
    "https://paypal-checkout-ffcafb.es.us-east-1.aws.elastic.cloud:443",
    api_key=es_api_key
)

# Connect to OpenAI
openai_client = OpenAI(api_key=openai_api_key)

# Define index source fields
index_source_fields = {
    "search-rotary": ["body"]
}

def get_elasticsearch_results(query):
    """
    Retrieve search results from Elasticsearch.
    """
    es_query = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title"]
            }
        },
        "size": 3
    }
    try:
        result = es_client.search(index="search-rotary", body=es_query)
        return result.get("hits", {}).get("hits", [])
    except Exception as e:
        return []

def create_openai_prompt(results):
    """
    Generate a context prompt from Elasticsearch results for OpenAI.
    """
    if not results:
        return "No relevant data found. Answer based on general knowledge."

    context = ""
    for hit in results:
        source_field = index_source_fields.get(hit["_index"], ["body"])[0]
        hit_context = hit["_source"].get(source_field, "")
        context += f"{hit_context}\n"

    prompt = f"""
Instructions:
- You are an assistant for answering questions.
- Answer based only on the given context. If unsure, say "I don't know."
- Cite sources using inline citations [].
- Use markdown for code.

Context:
{context}
"""
    return prompt

def generate_openai_completion(user_prompt, question):
    """
    Generate a response using OpenAI GPT.
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": user_prompt},
                {"role": "user", "content": question},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Error generating response from OpenAI."

@app.route("/ask", methods=["POST"])
def ask():
    """
    API endpoint to handle AI queries.
    """
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    elasticsearch_results = get_elasticsearch_results(question)
    context_prompt = create_openai_prompt(elasticsearch_results)
    response = generate_openai_completion(context_prompt, question)

    return jsonify({"answer": response})

if __name__ == "__main__":
    # Run on 0.0.0.0:8000 for Elastic Beanstalk compatibility
    app.run(host="0.0.0.0", port=8000, debug=True)