from retriever import retrieve

question=input("Question : ")

results=retrieve(question)

print("="*70)

for i,r in enumerate(results,1):

    print(f"Rank : {i}")

    print(f"Score : {r['score']:.4f}")

    print(f"Page : {r['page']}")

    print()

    print(r["text"][:600])

    print("-"*70)