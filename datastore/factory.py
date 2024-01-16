from datastore.datastore import DataStore
import os


async def get_datastore() -> DataStore:
    datastore = os.environ.get("DATASTORE")
    assert datastore is not None

    if datastore == "weaviate":
        from datastore.providers.weaviate_datastore import WeaviateDataStore
        return WeaviateDataStore()
    else:
        raise ValueError(
            f"Unsupported vector database: {datastore}. "
            f"Try one of the following: llama, elasticsearch, pinecone, weaviate, milvus, zilliz, redis, azuresearch, or qdrant"
        )
