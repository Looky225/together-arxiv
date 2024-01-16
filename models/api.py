# Importez les modules requis de pydantic pour définir les modèles
from models.models import Document, DocumentMetadataFilter, Query, QueryResult
from pydantic import BaseModel
from typing import List, Optional

# Définissez un modèle "UpsertRequest" pour la requête d'ajout ou mise à jour de documents
class UpsertRequest(BaseModel):
    documents: List[Document]  # Liste des documents à ajouter ou mettre à jour

# Définissez un modèle "UpsertResponse" pour la réponse de la requête d'ajout ou mise à jour
class UpsertResponse(BaseModel):
    ids: List[str]  # Liste des identifiants des documents ajoutés ou mis à jour

# Définissez un modèle "QueryRequest" pour la requête de recherche de documents
class QueryRequest(BaseModel):
    queries: List[Query]  # Liste des requêtes de recherche

# Définissez un modèle "QueryResponse" pour la réponse de la requête de recherche
class QueryResponse(BaseModel):
    results: List[QueryResult]  # Liste des résultats de recherche

# Définissez un modèle "DeleteRequest" pour la requête de suppression de documents
class DeleteRequest(BaseModel):
    ids: Optional[List[str]] = None  # Liste des identifiants de documents à supprimer (optionnel)
    filter: Optional[DocumentMetadataFilter] = None  # Filtre de métadonnées pour la suppression (optionnel)
    delete_all: Optional[bool] = False  # Indicateur pour supprimer tous les documents (optionnel, par défaut False)

# Définissez un modèle "DeleteResponse" pour la réponse de la requête de suppression
class DeleteResponse(BaseModel):
    success: bool  # Indicateur de réussite de la suppression
