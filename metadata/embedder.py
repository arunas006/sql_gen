from typing import List, Dict, Any
from openai import OpenAI

from app.planner.models import EmbeddingDocument, MetadataDocument
from uuid import uuid4

class Embedder:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def embed(self, text: str) -> List[float]:
        
        response = self.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
        return response.data[0].embedding
    
    def embed_document(self, document: List[MetadataDocument],batch_size: int = 100) -> List[EmbeddingDocument]:

        embedding_documents=[]
        for i in range(0, len(document), batch_size):
            batch = document[i:i+batch_size]
            batch_text = [
                doc.content for doc in batch
            ]
            response = self.client.embeddings.create(
                input=batch_text,
                model="text-embedding-3-small"
            )
            
            for doc, embedding in zip(batch, response.data):
                embedding_documents.append(EmbeddingDocument(
                    id=str(uuid4()),
                    embedding=embedding.embedding,
                    payload={
                        "id": doc.id,
                        "object_type": doc.object_type,
                        "name": doc.name,
                        "content": doc.content,
                        "metadata": doc.metadata
                    }
                ))
        return embedding_documents

