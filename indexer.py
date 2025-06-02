import os

import nltk
from nltk.corpus import reuters
from whoosh.fields import Schema, TEXT, ID, KEYWORD
from whoosh.index import create_in

schema = Schema(
    doc_id=ID(stored=True, unique=True),
    title=TEXT(stored=True),
    content=TEXT,
    topics=KEYWORD(stored=True)
)


def create_index(indexdir):
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)

    ix = create_in(indexdir, schema)
    writer = ix.writer()

    print("Indexing documents from NLTK Reuters corpus...")

    for fileid in reuters.fileids():
        try:
            content = reuters.raw(fileid)
            title = nltk.sent_tokenize(content)[0] if nltk.sent_tokenize(content) else fileid
            topics = ",".join(reuters.categories(fileid))
            writer.add_document(doc_id=fileid, title=title, content=content, topics=topics)
            print(f"Indexed: {fileid}")
        except Exception as e:
            print(f"Failed to index {fileid}: {e}")

    writer.commit(optimize=True)
    print("Indexing complete.")
