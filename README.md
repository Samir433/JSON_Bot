# Installation
git clone https://github.com/Samir433/JSON_Bot.git

cd JSON_Bot/


# Create .env Environment Variables

AZURE_OPENAI_KEY=<your-azure-openai-key>

AZURE_OPENAI_ENDPOINT=<your-azure-openai-endpoint>

ASTRA_DB_APPLICATION_TOKEN=<your-astra-db-application-token>

ASTRA_DB_ID=<your-astra-db-id>

ASTRA_DB_API_ENDPOINT=<your-astra-db-api-endpoint>

ASTRA_DB_COLLECTION_NAME=<your-collection-name>

SECRET_KEY=<your-flask-secret-key>



# Createand activate a virtual environment:
python3 -m venv venv

source venv/bin/activate

For Windows: venv\Scripts\activate

# Run Flask app

python app.py

# Install the dependencies:

pip install -r requirements.txt
