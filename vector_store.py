import os
from pathlib import Path

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)


class VectorStoreManager:

    def __init__(self):

        Path(
            "vector_db"
        ).mkdir(
            exist_ok=True
        )

        self.index_path = (
            "vector_db/faiss_index"
        )

        # --------------------------
        # Embedding Model
        # --------------------------

        self.embeddings = (
            HuggingFaceEmbeddings(
                model_name=
                "sentence-transformers/all-MiniLM-L6-v2"
            )
        )

        # --------------------------
        # Text Splitter
        # --------------------------

        self.text_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=[
                    "\n\n",
                    "\n",
                    ".",
                    " ",
                    ""
                ]
            )
        )

        self.vector_store = None

    # ----------------------------------
    # CREATE CHUNKS
    # ----------------------------------

    def create_chunks(
            self,
            text):

        chunks = (
            self.text_splitter
            .split_text(text)
        )

        return chunks

    # ----------------------------------
    # CREATE VECTOR STORE
    # ----------------------------------

    def create_vector_store(
            self,
            text):

        chunks = self.create_chunks(
            text
        )

        self.vector_store = (
            FAISS.from_texts(
                texts=chunks,
                embedding=self.embeddings
            )
        )

        return {
            "status":
                "Vector Store Created",

            "total_chunks":
                len(chunks)
        }

    # ----------------------------------
    # SAVE INDEX
    # ----------------------------------

    def save_index(self):

        if self.vector_store:

            self.vector_store.save_local(
                self.index_path
            )

            return True

        return False

    # ----------------------------------
    # LOAD INDEX
    # ----------------------------------

    def load_index(self):

        if not os.path.exists(
                self.index_path):

            return False

        self.vector_store = (
            FAISS.load_local(
                self.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        )

        return True

    # ----------------------------------
    # SEARCH
    # ----------------------------------

    def search(
            self,
            query,
            k=4):

        if not self.vector_store:

            raise Exception(
                "Vector Store Not Loaded"
            )

        results = (
            self.vector_store
            .similarity_search(
                query,
                k=k
            )
        )

        return results

    # ----------------------------------
    # SEARCH WITH SCORE
    # ----------------------------------

    def search_with_score(
            self,
            query,
            k=4):

        if not self.vector_store:

            raise Exception(
                "Vector Store Not Loaded"
            )

        results = (
            self.vector_store
            .similarity_search_with_score(
                query,
                k=k
            )
        )

        return results

    # ----------------------------------
    # VECTOR STATS
    # ----------------------------------

    def get_statistics(
            self,
            text):

        chunks = self.create_chunks(
            text
        )

        return {

            "characters":
                len(text),

            "words":
                len(
                    text.split()
                ),

            "chunks":
                len(chunks),

            "chunk_size":
                1000,

            "chunk_overlap":
                200
        }