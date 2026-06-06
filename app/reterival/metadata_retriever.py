from typing import List

from numpy import rint
from app.planner.models import RetrieveMetadata
from qdrant_client import QdrantClient, qdrant_client
from qdrant_client.http.exceptions import UnexpectedResponse
from dotenv import load_dotenv
from metadata.embedder import Embedder
from app.planner.models import RetrieveMetadata, Relatationship, ReterivalContext
from qdrant_client.models import (
    Filter, FieldCondition, MatchValue,
)
import os

class MetadataRetriever:
    COLLECTION_NAME = "metadata_collection"

    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")

    def __init__(self, api_key: str, url: str):
        self.client = QdrantClient(
            url=url,
            api_key=api_key
        )
        self.embedder = Embedder(api_key=self.openai_api_key)

    def _search_by_type(self, query_vector: List[float], object_type:str, top_k:int = 10) -> List[RetrieveMetadata]:
        
        try:
            results = self.client.query_points(
                collection_name=self.COLLECTION_NAME,
                query=query_vector,
                query_filter=Filter(
                    must=[
                        FieldCondition(
                        key="object_type",
                        match=MatchValue(value=object_type)
                    )
                ]
            ),
            limit=top_k
            )   

            retrieved_metadata = []
            for result in results.points:
                payload = result.payload
                retrieved_metadata.append(RetrieveMetadata(
                id=str(payload["id"]),
                score=result.score,
                object_type=payload["object_type"],
                name=payload["name"],
                content=payload["content"],
                metadata=payload["metadata"]
            ))

        except UnexpectedResponse as e:
            print("Status:", e.status_code)
            print("Response:", e.content)
            raise

        return retrieved_metadata

    def retrieve(self, query:str) -> List[ReterivalContext]:
        query_embedding = self.embedder.embed(query)
        tables = self._search_by_type(query_embedding, "table",top_k=3)
        columns = self._search_by_type(query_embedding, "column",top_k=8)
        kpis = self._search_by_type(query_embedding, "kpi",top_k=3)
        glossary = self._search_by_type(query_embedding, "glossary",top_k=3)

        return ReterivalContext(
            tables=tables,
            columns=columns,
            kpis=kpis,
            glossary=glossary
        )
    
if __name__ == "__main__":
    retriever = MetadataRetriever(api_key=os.getenv("QDRANT_API_KEY"), url=os.getenv("QDRANT_URL"))
    results = retriever.retrieve("What is the sales figures for the last quarter by region?")
    for result in (results.tables):
        print(result)
        print("-" * 20)
    for result in (results.columns):
        print(result)
        print("-" * 20)
    
   
    

       