import glob
import os

from whoosh.fields import Schema, TEXT
from whoosh.index import create_in


# Define the schema for the index
schema = Schema(title=TEXT(stored=True), content=TEXT)
def create_index(directory, indexdir):
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)
    writer = ix.writer()

    # Add documents to the index
    for filename in glob.glob(os.path.join(directory, '**', '*.txt'), recursive=True):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                writer.add_document(title=filename, content=content)
        print(f"Indexing file: {filename}")
    writer.commit()

if __name__ == '__main__':
    directorys = "./"
    index_directory = './Index_8.npy'
    create_index(directorys, index_directory)