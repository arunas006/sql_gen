from dotenv import load_dotenv
import os
from openai import OpenAI
from pathlib import Path
from app.reterival.metadata_retriever import MetadataRetriever
from app.planner.query_analyzer import QueryAnalyzerService
from app.reterival.metadata_retriever import MetadataRetriever
from metadata.relationship import RelationshipGraph
from app.reterival.context_builder import ContextInfo
from app.reterival.reterival_logic import ReterivalRouter
from app.planner.execution_plan import ExecutionPlanService
from app.planner.models import ExecutionPlanCollection, ExecutionPlanItem


load_dotenv()

class CompletePlan:
    def __init__(self, user_query: str):
        self.user_query = user_query
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.url = os.getenv("QDRANT_URL")
        relationships_path=r"/Users/arun/Documents/LLM_work/sql_gen/metadata/relationship.json"
        self.relationships_file = Path(relationships_path)
        self.relationship_graph = RelationshipGraph(str(self.relationships_file))
        execution_plan_service = ExecutionPlanService(self.relationship_graph)
        self.business_catalog_path = Path(r"/Users/arun/Documents/LLM_work/sql_gen/metadata/business_catalog.json")
        self.retriever = MetadataRetriever(api_key=self.api_key, url=self.url)
        self.router = ReterivalRouter(self.openai_client, self.user_query, self.business_catalog_path)
        reterived_info = self.router.route()
        if "investigations" not in reterived_info:
            retrieval_context = reterived_info['retrieval_context']
            self.context_info = ContextInfo(relationship_graph=self.relationship_graph, reterival_context=retrieval_context)
            print("Context Info Built completed")
            self.query_analyzer_service = QueryAnalyzerService(self.openai_client, context_info=self.context_info, user_input=self.user_query)
            analysis_result = self.query_analyzer_service.analyze_query()
            print("Query Analyzed")
            execution_plan = execution_plan_service.generate_execution_plan(analysis_result)
            execution_plan_item = ExecutionPlanItem(question=self.user_query, execution_plan=execution_plan)
            execution_plan_collection = ExecutionPlanCollection(plans=[execution_plan_item])
            directory = "execution_plans"
            execution_plan_service.save_execution_plan(execution_plan_collection, directory)
            print(execution_plan)
        else:
            print("Root Cause Analysis")
            plan_list = []
            investigations = reterived_info['investigations']
            for idx, investigation in enumerate(investigations):
                generated_query = investigation['question']
                retrieval_context = investigation['retrieval_context']
                self.context_info = ContextInfo(relationship_graph=self.relationship_graph, reterival_context=retrieval_context)
                print("Context Info Built completed", idx, generated_query)
                self.query_analyzer_service = QueryAnalyzerService(self.openai_client, context_info=self.context_info, user_input=generated_query)
                analysis_result = self.query_analyzer_service.analyze_query()
                print("Query Analyzed")
                execution_plan = execution_plan_service.generate_execution_plan(analysis_result)
                plan_list.append(ExecutionPlanItem(question=generated_query, execution_plan=execution_plan))
                
            execution_plan_collection = ExecutionPlanCollection(plans=plan_list)
            directory = "execution_plans"
            execution_plan_service.save_execution_plan(execution_plan_collection, directory)
            print(execution_plan_collection)

if __name__ == "__main__":
    # user_query = "What is the sales figures for the last quarter by region?"
    user_query = "What is the reason for decline in sales in the last quarter?"
    # user_query = "What are the top 5 products by revenue in the last month?"
    complete_plan = CompletePlan(user_query)