from openai import OpenAI

# Remplacez 'YOUR_API_KEY' par votre clé API réelle
api_key = '0c23cf90ee11d82d55c9d5dc390b84b9785d84a1f2f577f348ec35fcf16cbba3'

# Initialisez l'instance OpenAI avec votre clé API et l'URL de base
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")

# Texte que vous voulez encoder en embedding
input_text = "hello world"

# Modèle que vous voulez utiliser
model_name = "togethercomputer/m2-bert-80M-32k-retrieval"

# Appelez la méthode pour obtenir l'embedding
response = client.embeddings.create(
    input=input_text,
    model=model_name
)

# Extrait l'embedding du résultat
embedding = response.data[0].embedding

# Affiche l'embedding
print(embedding)
