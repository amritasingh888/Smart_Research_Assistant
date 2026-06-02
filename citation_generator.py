import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class CitationGenerator:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

    # -----------------------------
    # GENERIC
    # -----------------------------

    def generate(
            self,
            prompt):

        response = self.llm.invoke(
            prompt
        )

        return response.content

    # -----------------------------
    # EXTRACT METADATA
    # -----------------------------

    def extract_metadata(
            self,
            text):

        prompt = f"""
Extract the following information
from the research paper.

Return JSON format.

Fields:

- title
- authors
- journal
- conference
- publisher
- year
- doi

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # APA
    # -----------------------------

    def apa_citation(
            self,
            text):

        prompt = f"""
Generate APA 7th edition citation.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # MLA
    # -----------------------------

    def mla_citation(
            self,
            text):

        prompt = f"""
Generate MLA citation.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # IEEE
    # -----------------------------

    def ieee_citation(
            self,
            text):

        prompt = f"""
Generate IEEE citation.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # CHICAGO
    # -----------------------------

    def chicago_citation(
            self,
            text):

        prompt = f"""
Generate Chicago citation.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # BIBTEX
    # -----------------------------

    def bibtex_citation(
            self,
            text):

        prompt = f"""
Generate BibTeX entry.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # ALL CITATIONS
    # -----------------------------

    def generate_all(
            self,
            text):

        return {

            "APA":
                self.apa_citation(
                    text
                ),

            "MLA":
                self.mla_citation(
                    text
                ),

            "IEEE":
                self.ieee_citation(
                    text
                ),

            "Chicago":
                self.chicago_citation(
                    text
                ),

            "BibTeX":
                self.bibtex_citation(
                    text
                )
        }