import json
from collections import defaultdict, deque
from pathlib import Path

class RelationshipGraph:

    def __init__(self, relationships_file: str):
        self.graph = defaultdict(list)

        with open(relationships_file, 'r') as f:
            data=json.load(f)

        self._build_graph(data["relationships"])

    def _build_graph(self, relationships):
        for rel in relationships:
            source = rel['source_table']
            target = rel['target_table']
            
            self.graph[source].append({
                'table': target,
                'relationship': rel
            })

            self.graph[target].append({
                'table': source,
                'relationship': rel
            })

    def get_relationship(self, tables:list[str]):

        relationships = []
        seen = set()
        tables_set = set(tables)
        for table in tables_set:
            for edge in self.graph.get(table, []):
                rel = edge['relationship']
                source = rel['source_table']
                target = rel['target_table']
                if (source in tables_set and target in tables_set):
                    key =(source, target)
                    if key not in seen:
                        relationships.append(rel)
                        seen.add(key)
        return relationships

    def find_join_path(self, source, target):
        queue = deque([
            (
                source, 
                [source],
                []
            )
        ])
        visited = set()
        visited.add(source)
        while queue:
            current, table_path, relationship_path = queue.popleft()
            if current == target:
                return {
                    "table": table_path,
                    "relationship": relationship_path
                }

            for edge in self.graph.get(current, []):
                neighbor = edge['table']
                relationship = edge['relationship']
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, table_path + [neighbor], relationship_path + [relationship]))
        return None
      


if __name__ == "__main__":
    
    relationships_path=r"/Users/arun/Documents/LLM_work/sql_gen/metadata/relationship.json"
    relationships_file = Path(relationships_path)
    graph = RelationshipGraph(str(relationships_file))
    tables = ["sales", "products", "customer"]
    relationships = graph.get_relationship(tables)
    print(json.dumps(relationships, indent=2))
    join_path = graph.find_join_path("purchase", "customer")
    print(join_path)