import os

import streamlit as st

from search import search_index

option = st.sidebar.selectbox("Pilih Aksi", ["Cari Dokumen"])

dokumen_dir = "dokumen"
index_dir = "indexer"

if option == "Cari Dokumen":
    st.title("Cari  Berita")
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