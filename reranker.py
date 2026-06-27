from sentence_transformers import CrossEncoder

print("Loading CrossEncoder...")

reranker = CrossEncoder(

    "cross-encoder/ms-marco-MiniLM-L-6-v2"

)

print("Reranker Ready")


def rerank(question, docs):

    pairs = []

    for d in docs:

        pairs.append(

            [

                question,

                d["text"]

            ]

        )

    scores = reranker.predict(

        pairs

    )

    for score, doc in zip(

        scores,

        docs

    ):

        doc["rerank_score"] = float(score)

    docs = sorted(

        docs,

        key=lambda x: x["rerank_score"],

        reverse=True

    )

    return docs