from retriever import retrieve
from reranker import rerank
from llm import generate_answer


def ask(question):

    docs = retrieve(

        question,

        top_k=10

    )

    docs = rerank(

        question,

        docs

    )[:3]

    context = ""

    for doc in docs:

        context += f"""

Document

{doc['document']}

Page

{doc['page']}

Content

{doc['text']}

--------------------------------

"""

    answer = generate_answer(

        question,

        context

    )

    return {

        "question": question,

        "answer": answer,

        "sources": docs

    }