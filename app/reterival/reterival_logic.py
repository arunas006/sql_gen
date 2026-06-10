from openai import OpenAI
from app.planner.intent_analyser import IntentAnalyzer
from app.reterival.metadata_retriever import MetadataRetriever
from app.investigation.investigation_generator import InvestigationGenerator
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
class ReterivalRouter:

    def __init__(self, openai_client: OpenAI, user_query: str, business_catalog_path: Path):
        self.user_query = user_query
        self.openai = openai_client
        self.business_catalog_path = business_catalog_path
        self.intent_analyzer = IntentAnalyzer(openai_client, business_catalog_path)
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.retriever = MetadataRetriever(api_key=self.qdrant_api_key, url=self.qdrant_url)
        self.investigation_generator = InvestigationGenerator(openai_client)

    def route(self):
        intent_analyzer_info = self.intent_analyzer.analyze_intent(self.user_query)
        analysis_type = intent_analyzer_info.analysis_type
        # print(f"Identified analysis type: {analysis_type}")
        if analysis_type != "root_cause_analysis":
            return {
                "retrieval_context": self.retriever.retrieve(self.user_query),
                "intent_analyzer_info": intent_analyzer_info
            }
        else:
            reterival= self.retriever.retrieve(self.user_query)
            primary_domain = reterival.business_catalog
            investigation_result=self.investigation_generator.generate_investigation(self.user_query, primary_domain)
            extented_question = [item.question for item in sorted(investigation_result.investigation, key=lambda x: x.priority)]
            investigations = []
            for question in extented_question[:3]:
                # print("Working on question no.", idx, question)
                reterival = self.retriever.retrieve(question)
                investigations.append({
                    "question": question, "retrieval_context":reterival
                    })
            return {
                "investigations": investigations,
                "intent_analyzer_info": intent_analyzer_info,

            }

if __name__ == "__main__":
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=openai_api_key)
    business_catalog_path = Path(r"/Users/arun/Documents/LLM_work/sql_gen/metadata/business_catalog.json")
    user_query = "What is the reason for decline in sales in the last quarter?"
    # user_query = "What is the sales figure for the last quarter by region?"
    router = ReterivalRouter(openai_client, user_query, business_catalog_path)
    result = router.route(user_query)
    print(result)