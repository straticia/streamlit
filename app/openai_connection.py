import os
import openai
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")



def embed(docs: list[str]) -> list[list[float]]:
    res = openai.embeddings.create(
        input=docs,
        model="text-embedding-ada-002"
    )
    doc_embeds = [r.embedding for r in res.data]
    return doc_embeds

def search_docs(query, index):
    try:
        xq = embed([query])[0]
        res = index.query([xq], top_k=7, include_metadata=True)
        return [(match['metadata']['text'],
                 match['metadata'].get('full_text', 'Non disponible'),
                 match['score']) for match in res['matches']]
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return []