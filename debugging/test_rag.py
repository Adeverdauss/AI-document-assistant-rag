from rag import ask

while True:

    question = input("\nQuestion : ")

    if question.lower() == "exit":

        break

    result = ask(question)

    print("\n")

    print("=" * 60)

    print("ANSWER")

    print("=" * 60)

    print(result["answer"])

    print()

    print("=" * 60)
    print("SOURCE")
    print("=" * 60)

    if len(result["sources"]) == 0:

        print("Tidak ada source.")

    else:

        for doc in result["sources"]:

            print()

            print("Document :", doc["document"])

            print("Page :", doc["page"])

            print("Similarity :", round(doc["score"],4))

            print("Rerank :", round(doc["rerank_score"],4))