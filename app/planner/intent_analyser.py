from app.planner.models import LightWeightAnalysis
from app.planner.light_weight_analysis_prompt import INTENT_ANALYZER_PROMPT
from openai import OpenAI
import json
from pathlib import Path

class IntentAnalyzer:
    def __init__(self, openai_client: OpenAI, business_catalog_path: Path):
        self.openai = openai_client
        self.business_catalog_path = business_catalog_path

        with open(self.business_catalog_path, 'r') as f:
            self.business_catalog = json.load(f)

    def _get_available_business_domains(self):
        return [item['domain_name'] for item in self.business_catalog.get('domains', [])]   


    def analyze_intent(self, user_query: str) -> LightWeightAnalysis:
        available_domains = self._get_available_business_domains()
        prompt = INTENT_ANALYZER_PROMPT.format(
            user_query=user_query,
            available_domains=json.dumps(available_domains, indent=2)
        )

        response = self.openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "system", "content": prompt}]
        )

        analysis_result = response.choices[0].message.content
        return LightWeightAnalysis(**json.loads(analysis_result))
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=openai_api_key)
    business_catalog_path = Path(r"/Users/arun/Documents/LLM_work/sql_gen/metadata/business_catalog.json")
    intent_analyzer = IntentAnalyzer(openai_client, business_catalog_path)
    # user_query = "What are the sales figures for the last quarter by region?"
    user_query = "What are the top 5 products by revenue in the last month?"
    analysis = intent_analyzer.analyze_intent(user_query)
    print(analysis)
