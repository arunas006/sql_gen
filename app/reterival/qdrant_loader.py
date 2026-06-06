from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PayloadSchemaType,
    VectorParams,
    PointStruct
)
from app.planner.models import EmbeddingDocument
from uuid import uuid4

class QdrantLoader:
    COLLECTION_NAME = "metadata_collection"

    def __init__(self, api_key: str, url: str):
        self.client = QdrantClient(
            url=url,
            api_key=api_key
        )
        
    def create_collection(self):
        collections = self.client.get_collections()
        existing = [col.name for col in collections.collections]
        if self.COLLECTION_NAME in existing:
            print(f"Collection '{self.COLLECTION_NAME}' already exists.")
            return
        self.client.recreate_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{self.COLLECTION_NAME}' created successfully.")

        self.client.create_payload_index(
            collection_name=self.COLLECTION_NAME,
            field_name="object_type",
            field_schema=PayloadSchemaType.KEYWORD
        )

        print("Index created")

    def delete_collection(self):
        collection = self.client.get_collection(collection_name=self.COLLECTION_NAME)
        existing = [col.name for col in collection.collections]
        if self.COLLECTION_NAME not in existing:
            print(f"Collection '{self.COLLECTION_NAME}' does not exist.")
            return
        self.client.delete_collection(collection_name=self.COLLECTION_NAME)
        print(f"Collection '{self.COLLECTION_NAME}' deleted successfully.")

    
    def insert_embeddings(self, embedding_documents: List[EmbeddingDocument]):
        points = []
        for doc in embedding_documents:
            points.append(PointStruct(
                id=doc.id,
                vector=doc.embedding,
                payload=doc.payload
            ))
        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points
        )
        print(f"Inserted {len(points)} embedding documents into '{self.COLLECTION_NAME}' collection.")
