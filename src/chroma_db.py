from pathlib import Path
from typing import List, Dict

import chromadb


class ChromaDb:
    def __init__(self):
        chroma_db_path = Path(__file__).parent.parent / 'chromadb'
        chroma_db_path.mkdir(parents=True, exist_ok=True)
        # self.client = chromadb.Client()  # ephemeral client
        self.client = chromadb.PersistentClient(path=str(chroma_db_path))

    def get_collection(self, name: str, should_create: bool = True):
        if should_create:
            return self.client.get_or_create_collection(name=name)
        else:
            return self.client.get_collection(name=name)

    def delete_collection(self, name: str):
        try:
            self.client.delete_collection(name=name)
            return True
        except ValueError:
            return False

    def add_data(self, collection_name: str, documents: List[str], metadatas: List[Dict]):
        collection = self.get_collection(collection_name)
        collection.add(
            ids=[str(i) for i in range(0, len(documents))],
            documents=documents,
            metadatas=metadatas
        )

    def get_data(self, collection_name: str, query_texts: List[str], results_per_query: int = 1):
        collection = self.get_collection(collection_name, should_create=False)
        return collection.query(
            query_texts=query_texts,
            n_results=results_per_query
        )

    def count_data(self, collection_name: str) -> int:
        collection = self.get_collection(collection_name)
        return collection.count()
