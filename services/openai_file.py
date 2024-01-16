from typing import List
from openai import OpenAI
from loguru import logger
import os
import openai

from tenacity import retry, wait_random_exponential, stop_after_attempt



def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Embed texts using OpenAI's Ada model.

    Args:
        texts: The list of texts to embed.

    Returns:
        A list of embeddings, each of which is a list of floats.

    Raises:
        Exception: If the OpenAI API call fails.
    """
    # Create an instance of the OpenAI client with your API key
    client = OpenAI(api_key='0c23cf90ee11d82d55c9d5dc390b84b9785d84a1f2f577f348ec35fcf16cbba3', base_url="https://api.together.xyz/v1")

    # Define the model name
    model_name = "togethercomputer/m2-bert-80M-32k-retrieval"

    try:
        # Make a single call to the OpenAI API for all texts
        response = client.embeddings.create(
           input=texts,
           model=model_name
       )
        logger.debug(f"Embedding response: {response}")

        # Extract the embeddings from the response
        return [response.data[i].embedding for i in range(len(texts))]
    except Exception as e:
        # Log or handle the exception as needed
        raise Exception(f"Failed to get embeddings: {str(e)}")

def get_chat_completion(
    messages,
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    api_key='0c23cf90ee11d82d55c9d5dc390b84b9785d84a1f2f577f348ec35fcf16cbba3',
    base_url="https://api.together.xyz/v1"
):
    """
    Generate a chat completion using OpenAI's chat completion API.

    Args:
        messages: The list of messages in the chat history.

    Returns:
        A string containing the chat completion.

    Raises:
        Exception: If the OpenAI API call fails.
    """
    # Initialize the OpenAI client with the provided API key and base URL
    client = openai.OpenAI(api_key=api_key, base_url=base_url)

    # Call the OpenAI chat completion API with the given messages
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    # Extract the completion from the response
    completion = response.choices[0].message.content.strip()
    logger.info(f"Completion: {completion}")
    return completion
