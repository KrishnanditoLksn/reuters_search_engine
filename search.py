import os
from pathlib import Path
from typing import List

import pandas as pd
from nltk.corpus import reuters
from sklearn.metrics import f1_score, precision_score, recall_score
from whoosh import scoring
from whoosh.fields import Schema, TEXT
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))


def search_index(indexdir, query_string):
    ix = open_dir(indexdir)
    print(ix.doc_count())
    with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        print(f"Searching for: '{query_string}'")
        query = QueryParser("content", ix.schema).parse(query_string)

        print("Parser", query)
        results = searcher.search(query, terms=True, limit=1000)

        result_list = []
        for result in results:
            result_list.append({
                "title": result['title'],
                "score": result.score,
                "doc_id": result['doc_id'],
                "topics": result['topics']
            })

        found_hits = results.scored_length()

        corrector = searcher.correct_query(query, query_string)

        if corrector.query != query:
            print("Did you mean : ", corrector.string, "?")

        field_name = "content"
        print(f"Number of results found: {len(results)}")
        print(type(results))
        print(found_hits)
        for hit in results:
            print("Matched:", hit.matched_terms())
            print("Rank:", hit.rank)
            print("Score:", hit.score)
        return result_list


def document_label() -> List:
    categories = []
    for fileId in reuters.categories():
        categories.append(fileId)
    return categories


def split_data_label():
    docs = reuters.fileids()
    texts = [reuters.raw(doc_id) for doc_id in docs]
    labels = [reuters.categories(doc_id) for doc_id in docs]
    df = pd.DataFrame({'text': texts, 'labels': labels})
    return df


def evaluate_query(index_dir, ground_truth_dir, query_text, query_name, top_k=10):
    # Path ke ground truth
    gt_path = os.path.join(ground_truth_dir, query_name)
    if not os.path.exists(gt_path):
        return None  # Ground truth tidak ditemukan

    # Ambil dokumen relevan (file name di dalam ./gt/query_name/)
    relevant_files = set(os.listdir(gt_path))

    # Jalankan pencarian (menggunakan search engine Anda)
    results = search_index(query_text,index_dir)[:top_k]  # diasumsikan Anda batasi top-k di sini
    retrieved_files = set(os.path.basename(r['path']) for r in results)

    # Gabungan semua dokumen
    all_files = list(relevant_files | retrieved_files)
    y_true = [1 if f in relevant_files else 0 for f in all_files]
    y_pred = [1 if f in retrieved_files else 0 for f in all_files]

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    return {
        "query": query_text,
        "query_name": query_name,
        "relevant": len(relevant_files),
        "retrieved": len(retrieved_files),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "top_retrieved": list(retrieved_files)
    }

if __name__ == "__main__":
    index_directory = './indexer'
    print("INPUT YOUR QUERY:")
    search_query = input(str())
    search_index(index_directory, search_query)
