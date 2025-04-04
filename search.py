from whoosh.fields import Schema, TEXT
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

# Define the schema for the index
schema = Schema(title=TEXT(stored=True), content=TEXT)


# Function to search the index
def search_index(indexdir, query_string):
    ix = open_dir(indexdir)
    with ix.searcher() as searcher:
        print(f"Searching for: '{query_string}'")
        query = QueryParser("content", ix.schema).parse(query_string)
        results = searcher.search(query, terms=True)
        found_hits = results.scored_length()

        print(f"Number of results found: {len(results)}")
        print(found_hits)
        for hit in results:
            print("Matched:", hit.matched_terms())

        print("List of documents")
        if len(results) == 0:
            print("No results found.")
        for result in results:
            print(f"Title: {result['title']}")


# Example usage
if __name__ == "__main__":
    text_directory = '.'
    index_directory = './Index_2.npy'
    search_query = input(str())
    search_index(index_directory, search_query)
