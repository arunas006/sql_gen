import json
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryAnalyzer(BaseModel):

    intent: str
    primary_entities: List[str]
    candidate_tables: List[str]
    candidate_columns: List[str]
    requires_aggregation: bool
    requires_comparison: bool
    requires_trend_analysis: bool
    time_frame: Optional[str]
    filters: Optional[Dict[str, Any]]
    needs_clarification: bool
    clarification_questions: Optional[List[str]]

class MetadataDocument(BaseModel):
    id: str
    object_type: str
    name: str
    content:str
    metadata: Dict[str, Any]

class EmbeddingDocument(BaseModel):
    id: str
    embedding: List[float]
    payload: Optional[Dict[str, Any]] = None

class RetrieveMetadata(BaseModel):
    id: str
    score: float
    object_type: str
    name: str
    content: str
    metadata: Dict[str, Any]

class Relatationship(BaseModel):
    source_table: str
    source_column: str
    target_table: str
    target_column: str
    relationship_type: str
    
class ReterivalContext(BaseModel):
    tables: List[RetrieveMetadata]
    columns: List[RetrieveMetadata]
    kpis: List[RetrieveMetadata]
    glossary: List[RetrieveMetadata]

class ContextBuilder(BaseModel):
    tables: List[RetrieveMetadata]
    columns: List[RetrieveMetadata]
    kpis: List[RetrieveMetadata]
    glossary: List[RetrieveMetadata]
    relationship: List[Relatationship]

    
   
    
