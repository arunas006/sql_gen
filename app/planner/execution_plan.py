import uuid

from app.planner.models import JoinCondition,ExecutionPlan,QueryAnalyzer
import os

class ExecutionPlanService:

    def __init__(self,relationship):

        self.relationship = relationship

    def generate_execution_plan(self, query_analysis: QueryAnalyzer) -> ExecutionPlan:
        tables_required = self._get_required_tables(query_analysis)
        join_conditions = self._resolve_joins(query_analysis.fact_table, tables_required)
        
        execution_plan = ExecutionPlan(
            intent=query_analysis.intent,
            analysis_type=query_analysis.analysis_type,
            fact_table=query_analysis.fact_table,
            dimensions=query_analysis.dimensions,
            measures=query_analysis.measures,
            filters=query_analysis.filters,
            joins=join_conditions,
            granularity=query_analysis.granularity,
            order_by=query_analysis.order_by,
            limit=query_analysis.limit
        )

        return execution_plan
    
    def _get_required_tables(self, query_analysis: QueryAnalyzer) -> set:
        tables = set()
        tables.add(query_analysis.fact_table)

        for dimension in query_analysis.dimensions:
            tables.add(dimension.table)
        for measure in query_analysis.measures:
            tables.add(measure.table)
        for filter_cond in query_analysis.filters:
            tables.add(filter_cond.table)
        for order in query_analysis.order_by:
            tables.add(order.table)

        return tables
    
   
    def _resolve_joins(self,fact_table: str,required_tables: set) -> list[JoinCondition]:

        joins = []
        seen = set()

        for table in required_tables:

            if table == fact_table:
                continue

            path = self.relationship.find_join_path(
                fact_table,
                table
            )

            if not path:
                raise ValueError(
                    f"No join path found between "
                    f"{fact_table} and {table}"
                )

            for rel in path["relationship"]:

                key = (
                    rel["source_table"],
                    rel["source_column"],
                    rel["target_table"],
                    rel["target_column"]
                )

                if key not in seen:

                    joins.append(
                        JoinCondition(
                            left_table=rel["source_table"],
                            left_column=rel["source_column"],
                            right_table=rel["target_table"],
                            right_column=rel["target_column"]
                        )
                    )

                    seen.add(key)

        return joins   

    def save_execution_plan(self, execution_plan: ExecutionPlan,directory:str):
        os.makedirs(directory, exist_ok=True)
        file_name = f"{uuid.uuid4()}.json"
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w') as f:
            json.dump(execution_plan.model_dump(), f, indent=2)

        return file_path



if __name__ == "__main__":
    from metadata.relationship import RelationshipGraph
    from app.planner.query_analyzer import QueryAnalyzerService

    from dotenv import load_dotenv
    import os
    import json
    from pathlib import Path
    from app.reterival.metadata_retriever import MetadataRetriever
    from metadata.relationship import RelationshipGraph
    from openai import OpenAI
    from app.reterival.context_builder import ContextInfo

    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=openai_api_key)

    
    api_key = os.getenv("QDRANT_API_KEY")
    url = os.getenv("QDRANT_URL")
    relationships_path=r"/Users/arun/Documents/LLM_work/sql_gen/metadata/relationship.json"
    relationships_file = Path(relationships_path)
    retriever = MetadataRetriever(api_key=api_key, url=url)
    relationship_graph = RelationshipGraph(str(relationships_file))
    context_info = ContextInfo(metadata_retriever=retriever, relationship_graph=relationship_graph)
    print("Context Info Built")
    query_analyzer_service = QueryAnalyzerService(openai_client, context_info=context_info)  # You would need to initialize ContextInfo with actual implementations
    print
    user_input = "What is the sales figures for the last quarter by region?"
    analysis_result = query_analyzer_service.analyze_query(user_input)
    print("Query Analyzed")
    execution_plan_service = ExecutionPlanService(relationship_graph)
    execution_plan = execution_plan_service.generate_execution_plan(analysis_result)
    directory = "execution_plans"
    execution_plan_service.save_execution_plan(execution_plan, directory)
    print(execution_plan)