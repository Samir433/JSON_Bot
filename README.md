# Installation
git clone https://github.com/MansiAlhat/your-repository-name.git

cd your-repository-name


# Create .env Environment Variables

AZURE_OPENAI_KEY=<your-azure-openai-key>

AZURE_OPENAI_ENDPOINT=<your-azure-openai-endpoint>

ASTRA_DB_APPLICATION_TOKEN=<your-astra-db-application-token>

ASTRA_DB_ID=<your-astra-db-id>

ASTRA_DB_API_ENDPOINT=<your-astra-db-api-endpoint>

ASTRA_DB_COLLECTION_NAME=<your-collection-name>

SECRET_KEY=<your-flask-secret-key>



# Create a virtual environment:
python3 -m venv venv

source venv/bin/activate  # For Windows: venv\Scripts\activate



# Install the dependencies:

pip install -r requirements.txt
