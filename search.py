import glob

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
import os

# Define the schema for the index
schema = Schema(title=TEXT(stored=True), content=TEXT)


# Function to create an index
def create_index(directory, indexdir):
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)
    writer = ix.writer()

    # Add documents to the index
    for filename in glob.glob(os.path.join(directory, '**', '*.txt'),  recursive=True):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                writer.add_document(title=filename, content=content)
        # print(f"Indexing file: {filename}")
    writer.commit()


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
            print(f"Title: {result['title']}, Content: {result['title'][:200]}...")



# Example usage
if __name__ == "__main__":
    # Directory containing .txt files
    text_directory = '.'
    # Directory to store the index
    index_directory = './Index_2.npy'

    # Create the index
    create_index(text_directory, index_directory)

    # Search the index
    search_query = "canadian"
    search_index(index_directory, search_query)
