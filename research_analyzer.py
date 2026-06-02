import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class ResearchAnalyzer:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

    # --------------------------------
    # GENERIC FUNCTION
    # --------------------------------

    def generate(
            self,
            prompt):

        response = self.llm.invoke(
            prompt
        )

        return response.content

    # --------------------------------
    # RESEARCH OBJECTIVES
    # --------------------------------

    def extract_objectives(
            self,
            text):

        prompt = f"""
Extract the research objectives
from the paper.

Return as bullet points.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # --------------------------------
    # METHODOLOGY
    # --------------------------------

    def extract_methodology(
            self,
            text):

        prompt = f"""
Identify the methodology used
in the research paper.

Explain clearly.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # --------------------------------
    # DATASET USED
    # --------------------------------

    def extract_dataset(
            self,
            text):

        prompt = f"""
Identify any dataset,
data source,
or experimental data used.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # --------------------------------
    # RESULTS
    # --------------------------------

    def extract_results(
            self,
            text):

        prompt = f"""
Extract the major results
and outcomes.

Return as bullet points.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # --------------------------------
    # LIMITATIONS
    # --------------------------------

    def extract_limitations(
            self,
            text):

        prompt = f"""
Identify research limitations.

Return as bullet points.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # --------------------------------
    # FUTURE WORK
    # --------------------------------

    def extract_future_work(
            self,
            text):

        prompt = f"""
Identify future work
and future improvements.

Return as bullet points.

PAPER:

{text}
"""

        return self.generate(
            prompt
        )

    # --------------------------------
    # COMPLETE ANALYSIS
    # --------------------------------

    def analyze_paper(
            self,
            text):

        return {

            "objectives":
                self.extract_objectives(
                    text
                ),

            "methodology":
                self.extract_methodology(
                    text
                ),

            "dataset":
                self.extract_dataset(
                    text
                ),

            "results":
                self.extract_results(
                    text
                ),

            "limitations":
                self.extract_limitations(
                    text
                ),

            "future_work":
                self.extract_future_work(
                    text
                )
        }