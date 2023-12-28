import pinecone
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()
pinecone_api_key = os.environ.get("PINECONE_API_KEY")



def init_pinecone(index_name:str="recherche-documentaire-dans-le-droit"):
    pinecone.init(
        api_key=pinecone_api_key,
        environment="gcp-starter"
    )
    index = pinecone.Index(index_name)
    return index