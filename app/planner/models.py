import json
from pydantic import BaseModel
from typing import List, Dict, Any, Optional



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

class Dimension(BaseModel):
    table: str
    column: str

class Measure(BaseModel):
    table: str
    column: str
    aggregation: Optional[str] = None
    alias: Optional[str] = None

class FilterCondition(BaseModel):
    table: str
    column: str
    operator: str
    value: Optional[str] = None

class OrderBy(BaseModel):
    table: str
    column: str
    direction: str  # ASC or DESC

class QueryAnalyzer(BaseModel):

    intent: str

    analysis_type: str

    fact_table: str

    dimensions: List[Dimension]

    measures: List[Measure]

    filters: List[FilterCondition]

    granularity: Optional[str] = None

    order_by: List[OrderBy] = []

    limit: Optional[int] = None

    requires_aggregation: bool

    requires_comparison: bool

    requires_trend_analysis: bool

    needs_clarification: bool

    clarification_questions: List[str] = []

class JoinCondition(BaseModel):
    left_table: str
    left_column: str
    right_table: str
    right_column: str
    

class ExecutionPlan(BaseModel):
    intent: str
    analysis_type: str
    fact_table: str
    dimensions: List[Dimension]
    measures: List[Measure]
    filters: List[FilterCondition]
    joins: List[JoinCondition]
    granularity: Optional[str] = None
    order_by: List[OrderBy] = []
    limit: Optional[int] = None
 
class SqlGenerator(BaseModel):
    sql: str
    

    
