import os
import re

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.document import Document

DATA_DIR = "data"
VECTOR_DB_DIR = "vectorstore"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

documents = []

for file in os.listdir(DATA_DIR):
    if not file.endswith(".txt"):
        continue

    with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
        content = f.read()

    # Split each customer block
    customer_blocks = re.split(r"={10,}", content)

    for block in customer_blocks:
        match = re.search(r"Customer ID:\s*(CUST\d+)", block)
        if not match:
            continue

        customer_id = match.group(1)

        documents.append(
            Document(
                page_content=block.strip(),
                metadata={"customer_id": customer_id}
            )
        )

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local(VECTOR_DB_DIR)

print("✅ Ingestion completed successfully")
