from pathlib import Path
from typing import List, Dict, Any
from app.planner.models import MetadataDocument, EmbeddingDocument
from app.reterival.qdrant_loader import QdrantLoader
from metadata.embedder import Embedder
from metadata.metadata_builder import MetadataBuilder
from dotenv import load_dotenv
import os
from qdrant_client.http.exceptions import UnexpectedResponse


class IngestionPipeline:

    print("Starting ingestion pipeline...")
    metadata_builder = MetadataBuilder(
        schema_path="/Users/arun/Documents/LLM_work/sql_gen/metadata/schema.json",
        # relationships_path="/Users/arun/Documents/LLM_work/sql_gen/metadata/relationship.json",
        glossary_path="/Users/arun/Documents/LLM_work/sql_gen/metadata/glossary.json",
        kpi_definitions_path="/Users/arun/Documents/LLM_work/sql_gen/metadata/kpi.json"
    )
    print("MetadataBuilder initialized.")
    docs = metadata_builder.build_all_metadata_documents()
    print("Metadata documents built.")
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    print("Environment variables loaded.")
    embedder = Embedder(api_key=openai_api_key)
    embeded_docs = embedder.embed_document(docs)
    print("Documents embedded.")
    qdrant_loader = QdrantLoader(api_key=qdrant_api_key, url=qdrant_url)
    qdrant_loader.create_collection()
    print("Collection created.")
    COLLECTION_NAME = "metadata_collection"
    try:
        qdrant_loader.insert_embeddings(embeded_docs)
    except UnexpectedResponse as e:
        print("Status:", e.status_code)
        print("Response:", e.content)
        raise
 

    print("Ingestion pipeline completed.")

if __name__ == "__main__":
    IngestionPipeline()





