
from app.planner.models import ContextBuilder
from metadata.relationship import RelationshipGraph
from app.reterival.metadata_retriever import MetadataRetriever


class ContextInfo:

    def __init__(self, metadata_retriever: MetadataRetriever, relationship_graph: RelationshipGraph):
        self.metadata_retriever = metadata_retriever
        self.relationship_graph = relationship_graph


    def build_context(self,question:str) -> ContextBuilder:

        reterival_context = self.metadata_retriever.retrieve(question)
        table_name  = [table.name for table in reterival_context.tables]
        relationship = self.relationship_graph.get_relationship(table_name)
        return ContextBuilder(
            tables=reterival_context.tables,
            columns=reterival_context.columns,
            kpis=reterival_context.kpis,
            glossary=reterival_context.glossary,
            relationship=relationship
        )

if __name__ == "__main__":
    import os
    import json
    from pathlib import Path
    api_key = os.getenv("QDRANT_API_KEY")
    url = os.getenv("QDRANT_URL")
    relationships_path=r"/Users/arun/Documents/LLM_work/sql_gen/metadata/relationship.json"
    relationships_file = Path(relationships_path)
    retriever = MetadataRetriever(api_key=api_key, url=url)
    relationship_graph = RelationshipGraph(str(relationships_file))
    context_info = ContextInfo(metadata_retriever=retriever, relationship_graph=relationship_graph)
    context = context_info.build_context("What is the sales figures for the last quarter by region?")

    print(context)
