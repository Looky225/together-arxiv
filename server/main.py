import os
from typing import Optional
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, Depends, Body, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from loguru import logger
import arxiv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
import aiofiles 

from models.api import (
    DeleteRequest,
    DeleteResponse,
    QueryRequest,
    QueryResponse,
    UpsertRequest,
    UpsertResponse,
)
from datastore.factory import get_datastore
from services.file import get_document_from_file

from models.models import DocumentMetadata, Source

bearer_scheme = HTTPBearer()
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
assert BEARER_TOKEN is not None


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials


app = FastAPI(dependencies=[Depends(validate_token)])
# app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

# Set CORS middleware
origins = [
    "https://editor.swagger.io",
    "https://chat.openai.com",
    ["*"]
    # add any other origins that you want to allow,
    # or use ["*"] to allow all origins in development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specific allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Create a sub-application, in order to access just the query endpoint in an OpenAPI schema, found at http://0.0.0.0:8000/sub/openapi.json when the app is running locally
sub_app = FastAPI(
    title="Retrieval Plugin API",
    description="A retrieval API for querying and filtering documents based on natural language queries and metadata",
    version="1.0.0",
    servers=[{"url": "https://your-app-url.com"}],
    dependencies=[Depends(validate_token)],
)
app.mount("/sub", sub_app)





@app.post(
    "/upsert-file",
    response_model=UpsertResponse,
)
async def upsert_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
):
    try:
        metadata_obj = (
            DocumentMetadata.parse_raw(metadata)
            if metadata
            else DocumentMetadata(source=Source.file)
        )
    except:
        metadata_obj = DocumentMetadata(source=Source.file)

    document = await get_document_from_file(file, metadata_obj)
    try:

        ids = await datastore.upsert([document])
        
        return UpsertResponse(ids=ids)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.post(
    "/download-and-upsert-arxiv",
    response_model=UpsertResponse,
)
async def download_and_upsert_arxiv(
    search_id: str,  # Ajoutez un paramètre pour le numéro de recherche arXiv
    metadata: Optional[str] = Form(None),
):
    try:
        # Utilisez le numéro de recherche arXiv pour récupérer le papier correspondant
        paper = next(arxiv.Client().results(arxiv.Search(id_list=[search_id])))

        # Téléchargez le PDF dans le répertoire de travail avec un nom de fichier personnalisé.
        # Vous pouvez personnaliser davantage le nom du fichier si nécessaire.
        pdf_filename = f"{search_id}.pdf"
        paper.download_pdf(filename=pdf_filename)

        # Créez un objet DocumentMetadata à partir des métadonnées fournies (si disponibles)
        try:
            metadata_obj = (
                DocumentMetadata.parse_raw(metadata)
                if metadata
                else DocumentMetadata(source=Source.file)
            )
        except:
            metadata_obj = DocumentMetadata(source=Source.file)

        # Utilisez la fonction my_get_document_from_file pour obtenir un objet Document à partir du fichier téléchargé
        document = await get_document_from_file(pdf_filename, metadata_obj)

        # Utilisez la datastore pour ajouter le document à la base de données
        ids = await datastore.upsert([document])

        return UpsertResponse(ids=ids)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"str({e})")

@app.post(
    "/upsert",
    response_model=UpsertResponse,
)
async def upsert(
    request: UpsertRequest = Body(...),
):
    try:
        ids = await datastore.upsert(request.documents)
        return UpsertResponse(ids=ids)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

@sub_app.post(
    "/upsert",
    response_model=UpsertResponse,
    # NOTE: We are describing the shape of the API endpoint input due to a current limitation in parsing arrays of objects from OpenAPI schemas. This will not be necessary in the future.
    description="Save chat information. Accepts an array of documents with text (potential questions + conversation text), metadata (source 'chat' and timestamp, no ID as this will be generated). Confirm with the user before saving, ask for more details/context.",
)
async def upsert(
    request: UpsertRequest = Body(...),
    token: HTTPAuthorizationCredentials = Depends(validate_token),
):
    try:
        # Séparez les documents de mémoire des autres documents
        memory_documents = []
        chat_documents = []

        for document in request.documents:
            if document.metadata.source == "memory":
                memory_documents.append(document)
            elif document.metadata.source == "chat":
                chat_documents.append(document)

        # Sauvegardez les documents de mémoire dans la base de données de vecteurs
        if memory_documents:
            memory_ids = await datastore.upsert(memory_documents)
        else:
            memory_ids = []

        # Vous pouvez également effectuer d'autres actions ici, par exemple, marquer la conversation comme enregistrée en mémoire.

        # Pour le reste des documents (documents de conversation), procédez comme d'habitude
        if chat_documents:
            chat_ids = await datastore.upsert(chat_documents)
        else:
            chat_ids = []

        return UpsertResponse(ids=memory_ids + chat_ids)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.post(
    "/query",
    response_model=QueryResponse,
)
async def query_main(
    request: QueryRequest = Body(...),
):
    try:
        results = await datastore.query(
            request.queries,
        )
        return QueryResponse(results=results)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@sub_app.post(
    "/query",
    response_model=QueryResponse,
    # NOTE: We are describing the shape of the API endpoint input due to a current limitation in parsing arrays of objects from OpenAPI schemas. This will not be necessary in the future.
    description="Accepts search query objects array each with query and optional filter. Break down complex questions into sub-questions. Refine results by criteria, e.g. time / source, don't do this often. Split queries if ResponseTooLargeError occurs.",
)
async def query(
    request: QueryRequest = Body(...),
):
    try:
        results = await datastore.query(
            request.queries,
        )
        return QueryResponse(results=results)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.delete(
    "/delete",
    response_model=DeleteResponse,
)
async def delete(
    request: DeleteRequest = Body(...),
):
    if not (request.ids or request.filter or request.delete_all):
        raise HTTPException(
            status_code=400,
            detail="One of ids, filter, or delete_all is required",
        )
    try:
        success = await datastore.delete(
            ids=request.ids,
            filter=request.filter,
            delete_all=request.delete_all,
        )
        return DeleteResponse(success=success)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.on_event("startup")
async def startup():
    global datastore
    datastore = await get_datastore()


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)