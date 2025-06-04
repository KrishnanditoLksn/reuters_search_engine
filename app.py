import os

import streamlit as st
from whoosh.index import open_dir

from indexer import create_index
from search import search_index

# Pilih aksi
option = st.sidebar.selectbox("Pilih Aksi", ["Index Dokumen", "Cari Dokumen", "Klasifikasi Dokumen"])

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
            st.write(f"Hasil ditemukan: {len(results)} dokumen")
            for r in results:
                st.write("------")
                st.write(f"ID Dokumen: {r['doc_id']}")
                st.write(f"Kategori Dokumen: {r['topics']}")
                st.write(f"Skor: {r['score']:.4f}")
                st.write(r['title'][:500])
elif option == "Klasifikasi Dokumen":
    st.header("Klasifikasi Dokumen")
    content = st.text_input("Masukkan Isi kontenmu dulu lah")
    if content is None:
        st.warning("Isian tidak boleh kosong !!! ")
    else:
        if st.button("Indeks Lagi"):
            if not content.strip():
                st.warning("Isian tidak boleh kosong!")
            else:
                try:
                    ix = open_dir(index_dir)
                    writer = ix.writer()
                    writer.add_document(title=content)
                    writer.commit()
                    st.success("Konten berhasil ditambahkan ke indeks.")
                except Exception as e:
                    st.error(f"Gagal menambahkan ke indeks: {e}")