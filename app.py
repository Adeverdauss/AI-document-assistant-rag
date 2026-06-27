import os
import pickle

from collections import defaultdict

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from rag import ask
from add_document import add_document
from retriever import reload

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from retriever import reload

from rag import ask

import json
import os

from add_document import add_document

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    question = request.json["question"]

    result = ask(question)

    return jsonify(result)

from flask import request
import os

UPLOAD_FOLDER="uploads"

os.makedirs(

    UPLOAD_FOLDER,

    exist_ok=True

)

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    path = os.path.join(

        UPLOAD_FOLDER,

        file.filename

    )

    file.save(path)

    result = add_document(path)
    reload()

    return jsonify(result)

from collections import defaultdict

@app.route("/documents")
def documents():

    with open("vector_db/chunks.pkl","rb") as f:
        chunks = pickle.load(f)

    docs = defaultdict(

        lambda:{

            "document":"",
            "pages":set(),
            "chunks":0

        }

    )

    for chunk in chunks:

        name = chunk["document"]

        docs[name]["document"] = name

        docs[name]["pages"].add(

            chunk["page"]

        )

        docs[name]["chunks"] += 1

    result=[]

    for doc in docs.values():

        result.append({

            "document":doc["document"],

            "pages":len(doc["pages"]),

            "chunks":doc["chunks"]

        })

    return jsonify(result)

@app.route("/stats")
def stats():

    with open(

        "vector_db/chunks.pkl",

        "rb"

    ) as f:

        chunks = pickle.load(f)

    documents = len(

        set(

            c["document"]

            for c in chunks

        )

    )

    pages = len(

        set(

            (

                c["document"],

                c["page"]

            )

            for c in chunks

        )

    )

    return jsonify({

        "documents":documents,

        "pages":pages,

        "chunks":len(chunks)

    })
    
if __name__ == "__main__":

    app.run(

        debug=True,

        port=5000

    )