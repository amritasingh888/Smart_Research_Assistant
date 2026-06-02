import re
from collections import Counter

import pandas as pd
import plotly.express as px
from wordcloud import WordCloud


class AnalyticsDashboard:

    def __init__(self):

        self.stop_words = {

            "the", "a", "an", "and",
            "or", "of", "to", "in",
            "on", "for", "with",
            "is", "are", "was",
            "were", "be", "been",
            "this", "that", "these",
            "those", "it", "its",
            "as", "by", "from",
            "at", "we", "our",
            "their", "they"
        }

    # -----------------------------
    # DOCUMENT STATS
    # -----------------------------

    def document_statistics(
            self,
            text):

        words = text.split()

        sentences = re.split(
            r"[.!?]+",
            text
        )

        return {

            "total_words":
                len(words),

            "total_characters":
                len(text),

            "total_sentences":
                len(sentences),

            "average_word_length":
                round(
                    sum(
                        len(word)
                        for word in words
                    ) / max(
                        len(words),
                        1
                    ),
                    2
                )
        }

    # -----------------------------
    # TOP KEYWORDS
    # -----------------------------

    def extract_keywords(
            self,
            text,
            top_n=20):

        words = re.findall(
            r"\b[a-zA-Z]+\b",
            text.lower()
        )

        words = [

            word

            for word in words

            if word not in self.stop_words
            and len(word) > 2
        ]

        freq = Counter(words)

        return freq.most_common(
            top_n
        )

    # -----------------------------
    # DATAFRAME
    # -----------------------------

    def keyword_dataframe(
            self,
            text):

        keywords = (
            self.extract_keywords(
                text
            )
        )

        df = pd.DataFrame(

            keywords,

            columns=[
                "Keyword",
                "Frequency"
            ]
        )

        return df

    # -----------------------------
    # BAR CHART
    # -----------------------------

    def frequency_chart(
            self,
            text):

        df = self.keyword_dataframe(
            text
        )

        fig = px.bar(

            df,

            x="Keyword",

            y="Frequency",

            title=
            "Top Research Keywords"
        )

        return fig

    # -----------------------------
    # WORD CLOUD
    # -----------------------------

    def generate_wordcloud(
            self,
            text):

        wc = WordCloud(

            width=1200,

            height=600,

            background_color=
            "white"

        ).generate(text)

        return wc

    # -----------------------------
    # RESEARCH INSIGHTS
    # -----------------------------

    def research_insights(
            self,
            text):

        stats = (
            self.document_statistics(
                text
            )
        )

        keywords = (
            self.extract_keywords(
                text,
                top_n=10
            )
        )

        return {

            "statistics":
                stats,

            "top_keywords":
                keywords
        }