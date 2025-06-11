import os

import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import multilabel_confusion_matrix, classification_report, ConfusionMatrixDisplay
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
elif option == "Klasifikasi Dokumen":
    # Streamlit interface
    st.title("Klasifikasi Dokumen Reuters")

    df = split_data_label()
    st.header("Dataset")
    st.write(df.head())

    st.write("TF-IDF Vectorization")
    tfidf = TfidfVectorizer(stop_words=stopwords.words('english'), max_features=5000)
    X = tfidf.fit_transform(df['text'])

    st.write("Encoding Label")
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(df['labels'])

    st.write("Split Data (80% Train, 20% Test)")
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = OneVsRestClassifier(MultinomialNB())
    model.fit(X_train, Y_train)
    y_pred = model.predict(X_test)

    st.subheader("Hasil Prediksi (Sample)")
    st.write(pd.DataFrame(y_pred, columns=mlb.classes_))

    # Confusion Matrices
    st.subheader("Confusion Matrix (Top 10 Label Paling Umum)")
    matrix = multilabel_confusion_matrix(Y_test, y_pred)

    # Hitung frekuensi label di test set
    label_freq = Y_test.sum(axis=0)
    top_labels_idx = label_freq.argsort()[::-1][:10]  # top 10

    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    axes = axes.ravel()
    for i, idx in enumerate(top_labels_idx):
        cm = matrix[idx]
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1])
        disp.plot(ax=axes[i], values_format='d')
        axes[i].set_title(f"Class: {mlb.classes_[idx]}")
        disp.im_.colorbar.remove()
    plt.tight_layout()
    st.pyplot(fig)

    # Classification report
    st.subheader("Evaluasi: Classification Report")
    report = classification_report(Y_test, y_pred, target_names=mlb.classes_, output_dict=True)
    st.dataframe(pd.DataFrame(report).transpose())
