import os

import streamlit as st
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MultiLabelBinarizer

from indexer import create_index
from search import search_index, split_data_label

# Pilih aksi
option = st.sidebar.selectbox("Pilih Aksi",
                              ["Index Dokumen", "Cari Dokumen", "Klasifikasi Dokumen"])

# Jalur direktori
dokumen_dir = "dokumen"
index_dir = "indexer"

if option == "Index Dokumen":
    st.header("Indexing Dokumen")
    if st.button("Mulai Indexing"):
        if not os.path.exists(dokumen_dir):
            st.error("Folder dokumen tidak ditemukan.")
        else:
            create_index(index_dir)
            st.success("Indexing selesai.")
elif option == "Cari Dokumen":
    st.title("Aplikasi Pencarian Dokumen")
    st.header("Pencarian")
    query = st.text_input("Masukkan kata kunci")
    if st.button("Cari"):
        if not os.path.exists(index_dir):
            st.error("Index belum dibuat. Silakan lakukan indexing terlebih dahulu.")
        elif not query:
            st.warning("Silakan masukkan kata kunci.")
        else:
            results = search_index(index_dir, query)

            if len(results) <= 0:
                st.write("Hasil Pencarian Tidak ditemukan")
            else:
                st.write(f"Hasil ditemukan: {len(results)} dokumen")
                for r in results:
                    st.write("------")
                    st.write(f"ID Dokumen: {r['doc_id']}")
                    st.write(f"Kategori Dokumen: {r['topics']}")
                    st.write(f"Skor: {r['score']:.4f}")
                    st.write(r['title'][:500])
            #
            # ground_truth_dir = "./gt"
            # query_name = "weather"
            # if os.path.exists(ground_truth_dir):
            #     metrics = evaluate_query(index_dir, ground_truth_dir, query, query_name)
            #     if metrics:
            #         st.subheader("📊 Evaluasi Quer
            #         y Ini")
            #         st.write(f"Precision: {metrics['precision']}")
            #         st.write(f"Recall: {metrics['recall']}")
            #         st.write(f"F1-Score: {metrics['f1']}")
            #         st.caption(f"Relevant: {metrics['relevant']} | Retrieved: {metrics['retrieved']}")
            #     else:
            #         st.info("Tidak ada ground truth untuk query ini.")


elif option == "Klasifikasi Dokumen":
    st.write("Informasi Kelas Dokumen")
    df = split_data_label()
    st.header("DATASET ROUTERS")
    st.write(df)

    tfidf = TfidfVectorizer(stop_words=stopwords.words('english'), max_features=5000)
    X = tfidf.fit_transform(df['text'])

    st.write("Encode Label")
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(df['labels'])  # y = array (n_samples, n_labels)

    st.write("Split 80% training dan 20% test")
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, train_size=0.8)

    model = OneVsRestClassifier(MultinomialNB())
    model.fit(X_train, Y_train)
    y_pred = model.predict(X_test)

    st.write(y_pred)
    # st.header("Matrix Confusion")
    # st.write(confusion_matrix(Y_test, y_pred, labels=mlb.classes_))
