import json
from openai import OpenAI

from app.planner.models import QueryAnalyzer
from app.reterival.context_builder import ContextInfo
from app.prompt.query_analyzer_prompt import QUERY_ANALYZER_PROMPT

class QueryAnalyzerService:

    def __init__(self, openai_client: OpenAI, context_info: ContextInfo,user_input: str,):
        self.openai_client = openai_client
        self.context_info = context_info
        self.user_input = user_input

    def analyze_query(self) -> QueryAnalyzer:

        context = self.context_info.build_context()
        

        context_json = json.dumps(context.model_dump(),indent=2)
    
        prompt = QUERY_ANALYZER_PROMPT.format(
            reterival_context=context_json,
            user_query=self.user_input
        )

        response = self.openai_client.beta.chat.completions.parse(
            model="gpt-4.1-mini",
            messages=[{"role": "system", "content": prompt}],
            response_format=QueryAnalyzer
        )

        analysis_result: QueryAnalyzer = response.choices[0].message.parsed
        # analysis = QueryAnalyzer(**json.loads(analysis_result))
        return analysis_result
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    import json
    from pathlib import Path
    from app.reterival.metadata_retriever import MetadataRetriever
    from metadata.relationship import RelationshipGraph

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

    query_analyzer_service = QueryAnalyzerService(openai_client, context_info=context_info)  # You would need to initialize ContextInfo with actual implementations
    
    user_input = "What is the sales figures for the last quarter by region?"
    analysis_result = query_analyzer_service.analyze_query(user_input)
    
    print(analysis_result)