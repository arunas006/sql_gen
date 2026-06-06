import json
from pathlib import Path
from typing import Dict, Any,List

from app.planner.models import MetadataDocument

class MetadataBuilder:
    
    def __init__(self, schema_path: str, glossary_path: str, kpi_definitions_path: str):
        self.schema_path = schema_path
        # self.relationships_path = relationships_path
        self.glossary_path = glossary_path
        self.kpi_definitions_path = kpi_definitions_path

    def _load_json(self, path: str):
        with open(path ,"r",encoding="utf-8") as f:
            return json.load(f)
    
    def _build_table_documents(self,schema:Dict):
        docs =[]
        for table in schema.get("tables",[]):
            
            table_name = table.get("table_name")
            column_details = []
            for col in table.get("columns", []):
                column_details.append(
                f"- {col['name']} ({col['data_type']}): {col.get('description', '')}"
            )
            
            content =(
                f"Table: {table_name}\n"
                f"primary_key: {table.get('primary_key')}\n"
                    f"Columns: {', '.join(column_details)}\n"

                )
            docs.append(
                MetadataDocument(
                    id=f"table_{table_name}",
                    object_type="table",
                    name=table_name,
                    content=content,
                    metadata={
                        "primary_key": table.get("primary_key"),
                        "table_name": table_name,
                        }
                    )
                )
        return docs
    
    # def _build_relationship_documents(self, relationships:Dict):
    #     docs = []
    #     for rel in relationships.get("relationships",[]):
    #         content = (
    #             f"Relationship between "
    #             f"{rel.get('source_table',[])} and "
    #             f"{rel.get('target_table',[])}."
    #             f"{rel.get('source_table',[])}.{rel.get('source_column',[])} joins with "
    #             f"{rel.get('target_table',[])}.{rel.get('target_column',[])}"
    #         )
    #         docs.append(
    #             MetadataDocument(
    #                 id=(f"relationship_ "
    #                     f"{rel.get("source_table",[])}-{rel.get('target_table',[])}"),
    #                 object_type="relationship",
    #                 name=f"{rel.get("source_table",[])}-{rel.get('target_table',[])}",
    #                 content=content,
    #                 metadata=rel
    #             )
    #         )
    #     return docs
    
    def _build_glossary_documents(self, glossary: Dict):
        docs = []

        for item in glossary.get("business_terms", []):
            term = item.get("term", "")
            definition = item.get("definition", "")

            content = (
                f"Business Term: {term}\n"
                f"Definition: {definition}"
            )

            docs.append(
                MetadataDocument(
                    id=f"glossary_{term.lower().replace(' ', '_')}",
                    object_type="glossary",
                    name=term,
                    content=content,
                    metadata={
                        "term": term,
                        "definition": definition
                    }
                )
            )

        return docs
    
    def _build_column_documents(self, schema: Dict):

        docs = []

        for table in schema.get("tables", []):

            table_name = table.get("table_name")

            for column in table.get("columns", []):

                column_name = column.get("name")
                data_type = column.get("data_type")
                description = column.get("description", "")

                content = (
                    f"Column {column_name} "
                    f"in table {table_name}. "
                    f"Data type is {data_type}. "
                    f"Description: {description}"
                )

                docs.append(
                    MetadataDocument(
                        id=f"column_{table_name}_{column_name}",
                        object_type="column",
                        name=column_name,
                        content=content,
                        metadata={
                            "table_name": table_name,
                            "column_name": column_name,
                            "data_type": data_type
                        }
                    )
                )

        return docs
        
    def _build_kpi_documents(self, kpi_definitions: Dict):
        docs = []

        for item in kpi_definitions.get("kpis", []):
            kpi_name = item.get("kpi_name", "")
            formula = item.get("formula", "")
            description = item.get("description", "")

            content = (
                f"KPI Name: {kpi_name}\n"
                f"Formula: {formula}\n"
                f"Description: {description}"
            )

            docs.append(
                MetadataDocument(
                    id=f"kpi_{kpi_name.lower().replace(' ', '_')}",
                    object_type="kpi",
                    name=kpi_name,
                    content=content,
                    metadata={
                        "kpi_name": kpi_name,
                    }
                )
            )

        return docs
    
    def build_all_metadata_documents(self) -> List[MetadataDocument]:

        documents = []

        schema = self._load_json(self.schema_path)
        # relationships = self._load_json(self.relationships_path)
        glossary = self._load_json(self.glossary_path)
        kpi_definitions = self._load_json(self.kpi_definitions_path)

        table_docs = self._build_table_documents(schema)
        # relationship_docs = self._build_relationship_documents(relationships)
        glossary_docs = self._build_glossary_documents(glossary)
        kpi_docs = self._build_kpi_documents(kpi_definitions)
        col_docs = self._build_column_documents(schema)

        documents.extend(table_docs)
        # documents.extend(relationship_docs)
        documents.extend(glossary_docs)
        documents.extend(kpi_docs)
        documents.extend(col_docs)
        return documents

if __name__ == "__main__":
    metadata_builder = MetadataBuilder(
        schema_path="/Users/arun/Documents/LLM_work/sql_gen/metadata/schema.json",
        # relationships_path="/Users/arun/Documents/LLM_work/sql_gen/metadata/relationship.json",
        glossary_path="/Users/arun/Documents/LLM_work/sql_gen/metadata/glossary.json",
        kpi_definitions_path="/Users/arun/Documents/LLM_work/sql_gen/metadata/kpi.json"
    )

    schema = metadata_builder._load_json(metadata_builder.schema_path)
    # relationships = metadata_builder._load_json(metadata_builder.relationships_path)
    glossary = metadata_builder._load_json(metadata_builder.glossary_path)
    kpi_definitions = metadata_builder._load_json(metadata_builder.kpi_definitions_path)

    # table_docs = metadata_builder._build_table_documents(schema)
    # relationship_docs = metadata_builder._build_relationship_documents(relationships)
    # glossary_docs = metadata_builder._build_glossary_documents(glossary)
    # kpi_docs = metadata_builder._build_kpi_documents(kpi_definitions)
    col_docs = metadata_builder._build_column_documents(schema)
    # docs = metadata_builder.build_all_metadata_documents()
    print(col_docs)
  

