from openai import OpenAI
import json
import os
from app.planner.models import SqlGenerator
from app.sql_generation.sql_generator_prompt import SQL_GENERATOR_PROMPT
from pathlib import Path

class SQLGenerationService:


    def __init__(self, openai_client: OpenAI):
        self.openai = openai_client

    def generate_sql(self, user_query: str,execution_plan:Path) -> SqlGenerator:
        
        with open(execution_plan, 'r') as f:
            execution_plan_data = json.load(f)

        prompt = SQL_GENERATOR_PROMPT.format(
            execution_plan=json.dumps(execution_plan_data, indent=2),
            user_query=user_query
        )

        response = self.openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "system", "content": prompt}]
        )

        sql_result = response.choices[0].message.content
        return SqlGenerator(sql=sql_result)
    
    def generate_sql_for_folder(self, user_query: str, execution_plan_folder: Path, output_folder: Path) -> SqlGenerator:
        output_folder.mkdir(parents=True, exist_ok=True)
        json_files = list(execution_plan_folder.glob("*.json"))
        for json_file in json_files:
            sql_result = self.generate_sql(user_query, json_file)
            output_file = output_folder / f"{json_file.stem}_sql.txt"
            with open(output_file, 'w') as f:
                f.write(sql_result.sql)
        return output_file
        
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=openai_api_key)

    sql_generation_service = SQLGenerationService(openai_client)

    user_query = "What is the sales figures for the last quarter by region?"
    execution_plan_path = r"/Users/arun/Documents/LLM_work/sql_gen/execution_plans"
    sql_result = sql_generation_service.generate_sql_for_folder(user_query, Path(execution_plan_path), Path("SQL_output"))
    print(sql_result)