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
        results = searcher.search(query)
        print(f"Number of results found: {len(results)}")
        if len(results) == 0:
            print("No results found.")
        for result in results:
            print("List of documents")
            print(f"Title: {result['title']}")


# Example usage
if __name__ == "__main__":
    text_directory = '.'
    index_directory = './Index_2.npy'
    search_query = "NASA"
    search_index(index_directory, search_query)
