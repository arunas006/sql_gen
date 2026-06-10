import json
from pydantic import BaseModel
from typing import List, Dict, Any, Optional,Literal

class LightWeightAnalysis(BaseModel):
    analysis_type: str
    business_objective: str
    business_domain: str

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
    business_catalog: List[RetrieveMetadata]

class InvestigationContext(BaseModel):
    domain: str
    question: str
    priority: int

class InvestigationResult(BaseModel):
    investigation: List[InvestigationContext]

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
    aggregation: Literal["COUNT", "SUM", "AVG", "MIN", "MAX","COUNT_DISTINCT"]
    alias: str
    distinct: bool
    business_definition: Optional[str]=None

class DerivedMetric(BaseModel):
    name: str
    formula_type : Literal["ABSOLUTE_CHANGE", "PERCENT_CHANGE","AVERAGE_ORDER_VALUE","CONTRIBUTION_PERCENT","GROWTH_RATE","ORDERS_PER_CUSTOMER","CUSTOMER_RETENTION_RATE",
        "CUSTOMER_CHURN_RATE"]
    column: str

class BusinessDefinition(BaseModel):
    meteric: str
    definitions: str

class TimeContext(BaseModel):
    current_period: str
    comparison_period: Optional[str] = None

class FilterCondition(BaseModel):
    table: str
    column: str
    operator: str
    value: Optional[str] = None

class OrderBy(BaseModel):
    table: str
    column: str
    direction: str  # ASC or DESC

class PrimaryEntity(BaseModel):
    table: str
    column: str

class QueryAnalyzer(BaseModel):

    intent: str
    analysis_type: Literal["aggregation", "trend_analysis", "comparison", "ranking", "root_cause_analysis", "forecasting","detail"]
    fact_table: str
    fact_grain: Optional[str] = None
    dimensions: List[Dimension]
    measures: List[Measure]
    filters: List[FilterCondition]
    granularity: Optional[Literal["DAILY", "WEEKLY", "MONTHLY", "QUARTERLY", "YEARLY"]] = None
    sql_pattern: Optional[Literal["TREND_ANALYSIS", "PERIOD_COMPARISON","TOPN_RANKING","BOTTOMN_RANKING","CONTRIBUTION_ANALYSIS","SEGEMENT_COMPARISON","DETAIL_LOOKUP"]] = None
    comparison_type: Optional[Literal["TIME","DIMENSION"]] = None
    comparison_period: Optional[Literal["PREVIOUS_WEEK", "PREVIOUS_MONTH", "PREVIOUS_QUARTER", "PREVIOUS_YEAR","SAME_PERIOD_LAST_YEAR"]] = None
    comparison_metric: Optional[Literal["ABSOLUTE_CHANGE", "PERCENT_CHANGE","BOTH"]] = None
    ranking_type: Optional[Literal["TOPN", "BOTTOMN"]] = None
    result_type: Optional[Literal["SUMMARY", "DETAIL","RANKING","TREND_SERIES"]] = None
    primary_entity: Optional[PrimaryEntity] = None
    time_context: Optional[TimeContext] = None
    output_columns: List[str]=[]
    derived_metrics: List[DerivedMetric] = []
    business_definitions: List[BusinessDefinition] = []
    order_by: List[OrderBy] = []
    limit: Optional[int] = None
    requires_aggregation: bool
    requires_comparison: bool
    requires_trend_analysis: bool
    result_intent: Optional[Literal["INVESTIGATION_DECLINE","INVESTIGATION_GROWTH","TREND__MONITORING","RANKING","DETAIL_LOOKUP","SUMMARY"]] = None
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
    comparison_period: Optional[str] = None
    comparison_metric: Optional[str] = None
    time_context: Optional[TimeContext] = None
    derived_metrics: List[DerivedMetric] = []
    output_columns: List[str]=[]
    order_by: List[OrderBy] = []
    limit: Optional[int] = None
    sql_pattern: Optional[str] = None

class ExecutionPlanItem(BaseModel):
    question: str
    execution_plan: ExecutionPlan
 
class ExecutionPlanCollection(BaseModel):
    plans: List[ExecutionPlanItem]

class SQLResult(BaseModel):
    question: str
    sql: str
class SqlGenerator(BaseModel):
    sql: List[SQLResult]
    

    
