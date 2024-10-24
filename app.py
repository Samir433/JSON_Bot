from flask import Flask, render_template, request, session, jsonify, current_app
from flask_session import Session
import os
from openai import AzureOpenAI
from astrapy.db import AstraDB
from langchain_astradb import AstraDBVectorStore
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview"
)

# Initialize these variables at the top of your script
ASTRA_DB_APPLICATION_TOKEN = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
ASTRA_DB_ID = os.getenv('ASTRA_DB_ID')
ASTRA_DB_API_ENDPOINT = os.getenv('ASTRA_DB_API_ENDPOINT')
ASTRA_DB_COLLECTION_NAME = os.getenv('ASTRA_DB_COLLECTION_NAME')
AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')

# Global variable to hold the AstraDB vector store
astra_vector_store = None


def initialize_astra_vector_store(table_name):
    embedding = AzureOpenAIEmbeddings(azure_deployment="text-embedding-ada-002", api_key=AZURE_OPENAI_KEY,
                                      azure_endpoint=AZURE_OPENAI_ENDPOINT)
    global astra_vector_store
    if astra_vector_store is None:  # Only initialize if it's not already done
        astra_vector_store = AstraDBVectorStore(
            embedding=embedding,
            collection_name=table_name,
            api_endpoint=ASTRA_DB_API_ENDPOINT,
            token=ASTRA_DB_APPLICATION_TOKEN
        )
        print(f"Vector store initialized for collection: {table_name}")
    else:
        print("Using existing vector store.")


def perform_query(query_text, astra_vector_store):
    vectorDB_answer = astra_vector_store.similarity_search_with_score(query_text, k=1)
    res, score = vectorDB_answer[0]
    return res.page_content, score


def perform_query_chat(message_history):
    response = client.chat.completions.create(
        model="gpt35turbo16k",
        messages=message_history,
        temperature=0,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return response


@app.route('/')
def index():
    return render_template('index.html')


message_history = []


@app.route('/chat', methods=['POST'])
def chatbot():
    user_message = request.form.get('user_message')

    if user_message:
        initialize_astra_vector_store(ASTRA_DB_COLLECTION_NAME)  # Only call this once to initialize

        if astra_vector_store is not None:
            vectorDB_answer, score = perform_query(user_message, astra_vector_store)

            prompt = f"""
                You are an AI assistant that helps people generate relevant content based on the context provided.

                Context:
                {vectorDB_answer}

                User's query:
                {user_message}

                Please generate a response based on the above context and query.
            """

            message_history.append({"role": "user", "content": prompt})
            response = perform_query_chat(message_history)

            message_history.append({"role": "assistant", "content": response.choices[0].message.content})

            return jsonify({"response": response.choices[0].message.content})
        else:
            return jsonify({"response": "Vector store is not initialized!"})
    return jsonify({"response": "Please provide a message!"})


if __name__ == '__main__':
    app.run(debug=True)
