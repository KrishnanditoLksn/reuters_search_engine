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
        found_hits = results.scored_length()

        corrector = searcher.correct_query(query, query_string)

        if corrector.query != query:
            print("Did you mean : ", corrector.string, "?")

        print(f"Number of results found: {len(results)}")
        print(found_hits)
        for hit in results:
            print("Matched:", hit.matched_terms())
            print("Rank:" , hit.rank)
            print("Score:" , hit.score)
        print("==================================================")
        print("List of documents")
        if len(results) == 0:
            print("No results found.")
        for result in results:
            print(f"Title: {result['title']}")


if __name__ == "__main__":
    index_directory = './Index_8.npy'
    print("INPUT YOUR QUERY:")
    search_query = input(str())
    search_index(index_directory, search_query)
