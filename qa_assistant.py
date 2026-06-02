import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class ResearchQA:

    def __init__(
            self,
            vector_store):

        self.vector_store = (
            vector_store
        )

        self.llm = ChatGroq(
            model=
            "llama-3.3-70b-versatile",

            temperature=0.2,

            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

        self.chat_history = []

    # --------------------------------
    # RETRIEVE CONTEXT
    # --------------------------------

    def retrieve_context(
            self,
            question,
            top_k=4):

        docs = (
            self.vector_store.search(
                question,
                k=top_k
            )
        )

        context = "\n\n".join(

            [
                doc.page_content
                for doc in docs
            ]
        )

        return context

    # --------------------------------
    # BUILD PROMPT
    # --------------------------------

    def build_prompt(
            self,
            question,
            context):

        history_text = ""

        for item in (
            self.chat_history[-5:]
        ):

            history_text += f"""

User:
{item['question']}

Assistant:
{item['answer']}
"""

        prompt = f"""
You are an Academic Research Assistant.

You answer ONLY using the
provided research paper context.

If the answer is not available
in the paper say:

"I could not find this information
in the uploaded research paper."

--------------------------------
CHAT HISTORY
--------------------------------

{history_text}

--------------------------------
RESEARCH PAPER CONTEXT
--------------------------------

{context}

--------------------------------
QUESTION
--------------------------------

{question}

--------------------------------
ANSWER
--------------------------------
"""

        return prompt

    # --------------------------------
    # ASK QUESTION
    # --------------------------------

    def ask(
            self,
            question):

        context = (
            self.retrieve_context(
                question
            )
        )

        prompt = (
            self.build_prompt(
                question,
                context
            )
        )

        response = (
            self.llm.invoke(
                prompt
            )
        )

        answer = (
            response.content
        )

        self.chat_history.append(
            {
                "question":
                    question,

                "answer":
                    answer
            }
        )

        return answer

    # --------------------------------
    # GET HISTORY
    # --------------------------------

    def get_history(self):

        return (
            self.chat_history
        )

    # --------------------------------
    # CLEAR HISTORY
    # --------------------------------

    def clear_history(self):

        self.chat_history = []