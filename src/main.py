from pathlib import Path
import random
from typing import List, Dict

from chroma_db import ChromaDb
from util import load_json_file

SCIQ_COLLECTION = "sciq_supports"

chroma_db = ChromaDb()


def load_sciq_data() -> (List[Dict], int):
    sciq_path = Path(__file__).parent.parent / 'data' / 'SciQ-dataset' / 'valid.json'
    dataset = load_json_file(sciq_path)
    dataset = [d for d in dataset if d["support"] != ""]
    count = len(dataset)
    print(f"Number of questions with support: {count}")
    return dataset, count


def initialise_sciq_collection(dataset: List[Dict], count: int):
    documents = [d["support"] for d in dataset]
    metadatas = [{"type": "support"} for _ in range(0, count)]
    chroma_db.add_data(SCIQ_COLLECTION, documents, metadatas)


if __name__ == '__main__':
    dataset, count = load_sciq_data()
    if chroma_db.count_data(SCIQ_COLLECTION) < count:
        initialise_sciq_collection(dataset, count)

    sample_data = random.sample(dataset, 10)
    sample_questions = [d["question"] for d in sample_data]
    results = chroma_db.get_data(SCIQ_COLLECTION, sample_questions)

    for i, q in enumerate(sample_questions):
        print(f"Question: {q}")
        print(f"Retrieved support: {results['documents'][i][0]}")
        print()
