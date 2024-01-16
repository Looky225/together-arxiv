from typing import Dict
import json
import os
from loguru import logger
import openai
from models.models import Source

def extract_metadata_from_document(text: str) -> Dict[str, str]:
    sources = Source.__members__.keys()
    sources_string = ", ".join(sources)

    messages = [
        {
            "role": "system",
            "content": f"""
            Given a document representing an ArXiv search, from a user, try to extract the following metadata:
            - source: string, one of {sources_string}
            - url: string or don't specify
            - created_at: string or don't specify
            - author: string or don't specify

            Respond with a JSON containing the extracted metadata in key value pairs. If you don't find a metadata field, don't specify it.
            """,
        },
        {"role": "user", "content": text},
    ]

    # Initialize the OpenAI client with the provided API key and base URL
    client = openai.OpenAI(
        api_key="0c23cf90ee11d82d55c9d5dc390b84b9785d84a1f2f577f348ec35fcf16cbba3",
        base_url="https://api.together.xyz/v1",
    )

    # Call the OpenAI chat completion API with the provided request
    chat_completion = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=messages
    )

    # Extract the completion from the response
    completion = chat_completion.choices[0].message.content
    logger.info(f"Completion: {completion}")

    try:
        metadata = json.loads(completion)
    except:
        metadata = {}

    return metadata