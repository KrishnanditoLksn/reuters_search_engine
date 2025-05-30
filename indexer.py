import glob
import os

from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in

# Define the schema for the index
stem_analyzer = StemmingAnalyzer()
schema = Schema(title=TEXT(stored=True, analyzer=stem_analyzer), content=TEXT)


import os
import glob
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT

# Define schema
schema = Schema(title=TEXT(stored=True), content=TEXT)

def create_index(directory, indexdir):
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)

    ix = create_in(indexdir, schema)
    writer = ix.writer()

    print(f"Scanning directory: {directory}")

    for filepath in glob.glob(os.path.join(directory, '**', '*'), recursive=True):
        if os.path.isfile(filepath):  # pastikan ini file, bukan folder
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    writer.add_document(title=content, content=content)
                    print(f"Indexed file: {filepath}")
            except Exception as e:
                print(f"Failed to read {filepath}: {e}")

    writer.commit(optimize=True)



if __name__ == '__main__':
    directorys = "./dokumen"
    index_directory = './Index_8.npy'
    create_index(directorys, index_directory)
