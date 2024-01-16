# Importez les modules requis de pydantic pour définir les modèles
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# Définissez une énumération "Source" pour représenter les sources possibles
class Source(str, Enum):
    email = "email"
    file = "file"
    chat = "chat"

# Définissez un modèle "DocumentMetadata" pour stocker les métadonnées d'un document
class DocumentMetadata(BaseModel):
    source: Optional[Source] = None     # Source du document (parmi les valeurs de l'énumération Source)
    source_id: Optional[str] = None     # ID de la source (chaîne optionnelle)
    url: Optional[str] = None           # URL du document (chaîne optionnelle)
    created_at: Optional[str] = None    # Date de création (chaîne optionnelle au format date)
    author: Optional[str] = None        # Auteur du document (chaîne optionnelle)

# Définissez un modèle "DocumentChunkMetadata" qui hérite de DocumentMetadata
class DocumentChunkMetadata(DocumentMetadata):
    document_id: Optional[str] = None   # ID du document associé (chaîne optionnelle)

# Définissez un modèle "DocumentChunk" pour stocker un fragment de document
class DocumentChunk(BaseModel):
    id: Optional[str] = None            # ID du fragment (chaîne optionnelle)
    text: str                           # Texte du fragment (chaîne requise)
    metadata: DocumentChunkMetadata     # Métadonnées du fragment
    embedding: Optional[List[float]] = None  # Vecteur d'incorporation (liste de nombres optionnelle)

# Définissez un modèle "DocumentChunkWithScore" qui hérite de DocumentChunk
class DocumentChunkWithScore(DocumentChunk):
    score: float                        # Score du fragment (nombre flottant requis)

# Définissez un modèle "Document" pour stocker un document complet
class Document(BaseModel):
    id: Optional[str] = None            # ID du document (chaîne optionnelle)
    text: str                           # Texte du document (chaîne requise)
    metadata: Optional[DocumentMetadata] = None  # Métadonnées du document (optionnel)

# Définissez un modèle "DocumentWithChunks" qui hérite de Document
class DocumentWithChunks(Document):
    chunks: List[DocumentChunk]         # Liste des fragments associés au document

# Définissez un modèle "DocumentMetadataFilter" pour filtrer les documents par métadonnées
class DocumentMetadataFilter(BaseModel):
    document_id: Optional[str] = None   # ID du document (chaîne optionnelle)
    source: Optional[Source] = None     # Source du document (parmi les valeurs de l'énumération Source)
    source_id: Optional[str] = None     # ID de la source (chaîne optionnelle)
    author: Optional[str] = None        # Auteur du document (chaîne optionnelle)
    start_date: Optional[str] = None    # Date de début (chaîne optionnelle au format date)
    end_date: Optional[str] = None      # Date de fin (chaîne optionnelle au format date)

# Définissez un modèle "Query" pour représenter une requête de recherche
class Query(BaseModel):
    query: str                           # Texte de la requête (chaîne requise)
    filter: Optional[DocumentMetadataFilter] = None  # Filtre de métadonnées (optionnel)
    top_k: Optional[int] = 3            # Nombre de résultats souhaités (entier optionnel)

# Définissez un modèle "QueryWithEmbedding" qui hérite de Query
class QueryWithEmbedding(Query):
    embedding: List[float]               # Vecteur d'incorporation de la requête (liste de nombres requise)

# Définissez un modèle "QueryResult" pour stocker les résultats de la requête
class QueryResult(BaseModel):
    query: str                           # Texte de la requête (chaîne requise)
    results: List[DocumentChunkWithScore]  # Liste des résultats avec score
