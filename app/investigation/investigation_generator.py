import json
from app.planner.models import InvestigationContext, InvestigationResult
from app.investigation.investigation_prompt import INVESTIGATION_QUESTION_PROMPT
from openai import OpenAI

class InvestigationGenerator:

    def __init__(self, openai_client: OpenAI):
        self.openai = openai_client

    def _build_business_catalog_context(self, business_domains):

        return "\n\n".join(
            domain.content
            for domain in business_domains
        )
    
    def generate_investigation(self, question: str, business_domains) -> InvestigationResult:

        business_catalog = self._build_business_catalog_context(business_domains)

        prompt = INVESTIGATION_QUESTION_PROMPT.format(
            question=question,
            business_catalog_context=business_catalog
        )

        response = self.openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "system", "content": prompt}]
        )

        investigation_result = response.choices[0].message.content
        return InvestigationResult(**json.loads(investigation_result))

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    from app.reterival.metadata_retriever import MetadataRetriever

    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=openai_api_key)
    investigation_generator = InvestigationGenerator(openai_client)
    question = "What is the reason for decline in sales in the last quarter?"
    retriever = MetadataRetriever(api_key=os.getenv("QDRANT_API_KEY"), url=os.getenv("QDRANT_URL"))
    results = retriever.retrieve(question)
    primary_domain = results.business_catalog
    # print(primary_domain)
    investigation_result = investigation_generator.generate_investigation(question, primary_domain)
    print(investigation_result)
            