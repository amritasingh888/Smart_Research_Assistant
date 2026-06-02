import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class PaperSummarizer:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

    # -----------------------------
    # GENERIC GENERATOR
    # -----------------------------

    def generate(
            self,
            prompt):

        response = self.llm.invoke(
            prompt
        )

        return response.content

    # -----------------------------
    # ABSTRACT SUMMARY
    # -----------------------------

    def abstract_summary(
            self,
            text):

        prompt = f"""
You are an academic research assistant.

Create a concise abstract-style summary
of the following research paper.

Length:
100-150 words.

RESEARCH PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # DETAILED SUMMARY
    # -----------------------------

    def detailed_summary(
            self,
            text):

        prompt = f"""
Create a detailed summary of the
following research paper.

Include:

- Objectives
- Methodology
- Findings
- Conclusion

Length:
300-500 words.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # EXECUTIVE SUMMARY
    # -----------------------------

    def executive_summary(
            self,
            text):

        prompt = f"""
Create an executive summary suitable
for professors, researchers and
decision makers.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # KEY FINDINGS
    # -----------------------------

    def key_findings(
            self,
            text):

        prompt = f"""
Extract only the key findings from
the research paper.

Return as bullet points.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # RESEARCH CONTRIBUTIONS
    # -----------------------------

    def research_contributions(
            self,
            text):

        prompt = f"""
Identify the main research
contributions.

Return as bullet points.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # FUTURE SCOPE
    # -----------------------------

    def future_scope(
            self,
            text):

        prompt = f"""
Identify future research directions
and future scope mentioned or implied
in the paper.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # COMPLETE PACK
    # -----------------------------

    def generate_full_report(
            self,
            text):

        return {

            "abstract_summary":
                self.abstract_summary(
                    text
                ),

            "detailed_summary":
                self.detailed_summary(
                    text
                ),

            "executive_summary":
                self.executive_summary(
                    text
                ),

            "key_findings":
                self.key_findings(
                    text
                ),

            "research_contributions":
                self.research_contributions(
                    text
                ),

            "future_scope":
                self.future_scope(
                    text
                )
        }