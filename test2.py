import openai

system_content = "You are a travel agent. Be descriptive and helpful."
user_content = "Tell me about San Francisco"

client = openai.OpenAI(
    api_key="0c23cf90ee11d82d55c9d5dc390b84b9785d84a1f2f577f348ec35fcf16cbba3",
    base_url="https://api.together.xyz/v1",
    )

# Appelez l'API de complétion de chat OpenAI avec le message utilisateur uniquement
chat_completion = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[
        {"role": "user", "content": user_content},
    ]
)

# Extrait la complétion de la réponse
response = chat_completion.choices[0].message.content.strip()
print(response)