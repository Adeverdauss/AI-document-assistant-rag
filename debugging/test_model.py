from sentence_transformers import SentenceTransformer
import time

print("Start")

t1 = time.time()

model = SentenceTransformer(
    "BAAI/bge-base-en-v1.5"
)

print("Loaded")

print(time.time() - t1)