import streamlit as st

from research_loader import ResearchLoader
from paper_summarizer import PaperSummarizer
from research_analyzer import ResearchAnalyzer
from citation_generator import CitationGenerator
from vector_store import VectorStoreManager
from qa_assistant import ResearchQA
from analytics_dashboard import AnalyticsDashboard
from report_generator import ReportGenerator

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Smart Academic Research Assistant",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------------
# MODERN CSS
# -----------------------------------

st.markdown("""
<style>

.main {
    padding-top: 0rem;
}

.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #00D4FF,
        #0047FF
    );
    color: white;
    margin-bottom: 20px;
}

.metric-card {
    background: #1c1c1c;
    padding: 20px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SESSION STATE
# -----------------------------------

defaults = {

    "paper_text": "",

    "summary": "",

    "analysis": None,

    "citations": None,

    "chatbot": None,

    "processed": False,

    "file_name": None
}

for k, v in defaults.items():

    if k not in st.session_state:

        st.session_state[k] = v

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown("""
<div class="hero">

<h1>🎓 Smart Academic Research Assistant</h1>

<h4>
Research Paper Analysis,
Summarization and AI Chat
</h4>

</div>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.title("📚 Research AI")

    uploaded_file = st.file_uploader(

        "Upload Research Paper",

        type=[
            "pdf",
            "docx",
            "txt"
        ]
    )

    st.markdown("---")

    st.info(
        """
Supported Files

• PDF
• DOCX
• TXT
"""
    )

# -----------------------------------
# PROCESS FILE
# -----------------------------------

if uploaded_file:

    if (
        st.session_state.file_name
        != uploaded_file.name
    ):

        st.session_state.processed = False

        st.session_state.file_name = (
            uploaded_file.name
        )

    if not st.session_state.processed:

        temp_file = uploaded_file.name

        with open(
            temp_file,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        # Loader

        with st.spinner(
            "Loading Research Paper..."
        ):

            loader = ResearchLoader()

            data = (
                loader.load_document(
                    temp_file
                )
            )

            text = data["text"]

            st.session_state.paper_text = (
                text
            )

        # Summary

        with st.spinner(
            "Generating Summary..."
        ):

            summarizer = (
                PaperSummarizer()
            )

            st.session_state.summary = (
                summarizer.abstract_summary(
                    text[:12000]
                )
            )

        # Analysis

        with st.spinner(
            "Analyzing Research..."
        ):

            analyzer = (
                ResearchAnalyzer()
            )

            st.session_state.analysis = (
                analyzer.analyze_paper(
                    text[:12000]
                )
            )

        # Citations

        with st.spinner(
            "Generating Citations..."
        ):

            citation = (
                CitationGenerator()
            )

            st.session_state.citations = (
                citation.generate_all(
                    text[:12000]
                )
            )

        # Vector Store

        with st.spinner(
            "Building AI Knowledge Base..."
        ):

            vector_db = (
                VectorStoreManager()
            )

            vector_db.create_vector_store(
                text
            )

            st.session_state.chatbot = (
                ResearchQA(
                    vector_db
                )
            )

        st.session_state.processed = True

# -----------------------------------
# TABS
# -----------------------------------

tabs = st.tabs([

    "📄 Summary",

    "🔬 Analysis",

    "💬 Chat",

    "📊 Analytics",

    "📚 Citations",

    "📥 Export"
])

# -----------------------------------
# SUMMARY TAB
# -----------------------------------

with tabs[0]:

    st.subheader(
        "📄 Research Summary"
    )

    if st.session_state.summary:

        st.write(
            st.session_state.summary
        )

    else:

        st.info(
            "Upload a paper."
        )

# -----------------------------------
# ANALYSIS TAB
# -----------------------------------

with tabs[1]:

    st.subheader(
        "🔬 Research Analysis"
    )

    analysis = (
        st.session_state.analysis
    )

    if analysis:

        st.markdown(
            "### Objectives"
        )

        st.write(
            analysis["objectives"]
        )

        st.markdown(
            "### Methodology"
        )

        st.write(
            analysis["methodology"]
        )

        st.markdown(
            "### Dataset"
        )

        st.write(
            analysis["dataset"]
        )

        st.markdown(
            "### Results"
        )

        st.write(
            analysis["results"]
        )

        st.markdown(
            "### Limitations"
        )

        st.write(
            analysis["limitations"]
        )

        st.markdown(
            "### Future Work"
        )

        st.write(
            analysis["future_work"]
        )

        # -----------------------------------
# CHAT TAB
# -----------------------------------

with tabs[2]:

    st.subheader(
        "💬 AI Research Assistant"
    )

    if st.session_state.chatbot:

        if (
            "messages"
            not in st.session_state
        ):
            st.session_state.messages = []

        for msg in (
            st.session_state.messages
        ):

            with st.chat_message(
                msg["role"]
            ):
                st.write(
                    msg["content"]
                )

        if prompt := st.chat_input(
            "Ask about this research paper..."
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            with st.chat_message(
                "user"
            ):
                st.write(prompt)

            with st.spinner(
                "Analyzing paper..."
            ):

                answer = (
                    st.session_state.chatbot.ask(
                        prompt
                    )
                )

            with st.chat_message(
                "assistant"
            ):
                st.write(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

    else:

        st.info(
            "Upload a research paper first."
        )

        # -----------------------------------
# ANALYTICS TAB
# -----------------------------------

with tabs[3]:

    st.subheader(
        "📊 Research Analytics"
    )

    if st.session_state.paper_text:

        analytics = (
            AnalyticsDashboard()
        )

        stats = (
            analytics.document_statistics(
                st.session_state.paper_text
            )
        )

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        col1.metric(
            "Words",
            stats["total_words"]
        )

        col2.metric(
            "Characters",
            stats["total_characters"]
        )

        col3.metric(
            "Sentences",
            stats["total_sentences"]
        )

        col4.metric(
            "Avg Word Length",
            stats["average_word_length"]
        )

        st.markdown("---")

        st.subheader(
            "Top Keywords"
        )

        keywords = (
            analytics.extract_keywords(
                st.session_state.paper_text
            )
        )

        keyword_df = (
            analytics.keyword_dataframe(
                st.session_state.paper_text
            )
        )

        st.dataframe(
            keyword_df,
            use_container_width=True
        )

        st.markdown("---")

        fig = (
            analytics.frequency_chart(
                st.session_state.paper_text
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Upload a research paper first."
        )

        # -----------------------------------
# CITATIONS TAB
# -----------------------------------

with tabs[4]:

    st.subheader(
        "📚 Citation Generator"
    )

    citations = (
        st.session_state.citations
    )

    if citations:

        st.markdown(
            "### APA"
        )
        st.code(
            citations["APA"]
        )

        st.markdown(
            "### MLA"
        )
        st.code(
            citations["MLA"]
        )

        st.markdown(
            "### IEEE"
        )
        st.code(
            citations["IEEE"]
        )

        st.markdown(
            "### Chicago"
        )
        st.code(
            citations["Chicago"]
        )

        st.markdown(
            "### BibTeX"
        )
        st.code(
            citations["BibTeX"]
        )

    else:

        st.info(
            "Upload a research paper first."
        )

        # -----------------------------------
# EXPORT TAB
# -----------------------------------

with tabs[5]:

    st.subheader(
        "📥 Export Center"
    )

    if (
        st.session_state.summary
        and
        st.session_state.analysis
        and
        st.session_state.citations
    ):

        report_generator = (
            ReportGenerator()
        )

        files = (
            report_generator.export_complete_report(
                st.session_state.summary,
                st.session_state.analysis,
                st.session_state.citations
            )
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        with open(
            files["txt"],
            "rb"
        ) as f:

            col1.download_button(
                "📄 Download TXT",
                f,
                file_name=
                "research_report.txt"
            )

        with open(
            files["pdf"],
            "rb"
        ) as f:

            col2.download_button(
                "📕 Download PDF",
                f,
                file_name=
                "research_report.pdf"
            )

        with open(
            files["docx"],
            "rb"
        ) as f:

            col3.download_button(
                "📘 Download DOCX",
                f,
                file_name=
                "research_report.docx"
            )

    else:

        st.info(
            "Upload a research paper first."
        )

        # -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    """
🚀 Smart Academic Research Assistant

Built with:
Streamlit • Groq • LangChain • FAISS • HuggingFace
"""
)