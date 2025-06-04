from typing import List

import pandas as pd
from nltk.corpus import reuters
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


if __name__ == "__main__":
    index_directory = './indexer'
    print("INPUT YOUR QUERY:")
    search_query = input(str())
    search_index(index_directory, search_query)
