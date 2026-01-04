import re
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from transformers import pipeline

# ======================================
# CONFIG
# ======================================
VECTOR_DB_DIR = "vectorstore"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-base"

BANK_PASSWORDS = {
    "CUST1001": "CUST1001",
    "CUST1002": "CUST1002",
    "CUST1003": "CUST1003",
    "CUST1004": "CUST1004",
}

st.set_page_config(page_title="ABC Bank Assistant", page_icon="🏦")
st.title("🏦 ABC Bank Customer Support Assistant")

# ======================================
# SESSION
# ======================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "customer_id" not in st.session_state:
    st.session_state.customer_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ======================================
# LOAD VECTORSTORE
# ======================================
@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return FAISS.load_local(
        VECTOR_DB_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

# ======================================
# LOAD LLM
# ======================================
@st.cache_resource
def load_llm():
    pipe = pipeline(
        "text2text-generation",
        model=LLM_MODEL,
        max_new_tokens=200,
        do_sample=False
    )
    return HuggingFacePipeline(pipeline=pipe)

llm = load_llm()

# ======================================
# HELPERS
# ======================================
def extract_section(text, section):
    pattern = rf"===\s*{section}\s*===(.*?)(===|$)"
    match = re.search(pattern, text, re.S | re.I)
    return match.group(1).strip() if match else None

def detect_intent(query):
    q = query.lower()
    if "balance" in q or "account" in q:
        return "ACCOUNT SUMMARY"
    if "card" in q:
        return "CARD DETAILS"
    if "loan" in q:
        return "LOAN DETAILS"
    if "transaction" in q:
        return "TRANSACTIONS"
    return None

def is_policy_question(query):
    q = query.lower()
    return any(w in q for w in ["apply", "eligibility", "eligible"])

# ======================================
# LOGIN
# ======================================
if not st.session_state.logged_in:
    st.subheader("🔐 Customer Login")

    cid = st.text_input("Customer ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        cid = cid.upper()
        if cid in BANK_PASSWORDS and BANK_PASSWORDS[cid] == pwd:
            st.session_state.logged_in = True
            st.session_state.customer_id = cid
            st.session_state.chat_history = []
            st.success("Login successful. Press Login again to continue.")
        else:
            st.error("Invalid credentials")
    st.stop()

# ======================================
# CHAT
# ======================================
for role, msg in st.session_state.chat_history:
    st.chat_message(role).write(msg)

query = st.chat_input("Ask your banking question related to Balance,Loan, Cards and transactions.")

if query:
    st.chat_message("user").write(query)
    st.session_state.chat_history.append(("user", query))

    # LOGOUT
    if query.lower() == "logout":
        st.session_state.clear()
        st.chat_message("assistant").write("Logged out successfully.")
        st.stop()

    # 🔒 BLOCK ACCESS TO OTHER CUSTOMERS
    mentioned = re.search(r"CUST\d+", query.upper())
    if mentioned and mentioned.group() != st.session_state.customer_id:
        answer = "To avoid security issues,you are not authorized to access another customer's details.\nTry Logging out and Login again using that customer's credentials.\n"

    # ✅ POLICY QUESTIONS (NO RAG)
    elif is_policy_question(query):
        answer = (
            "Customers can apply for loans or cards through online banking or "
            "by visiting the nearest branch.\n\n"
            "Loan eligibility depends on credit score, income, and existing liabilities.\n\n"
            "Credit card eligibility depends on account history and income verification.\nFor further queries contact\nPhone: 0000 1111\nEmail: abcbank@gmail.com\n"
        
        )

    else:
        docs = retriever.invoke(query)

        customer_docs = [
            d for d in docs
            if d.metadata.get("customer_id") == st.session_state.customer_id
        ]

        intent = detect_intent(query)
        sections = []

        for d in customer_docs:
            sec = extract_section(d.page_content, intent)
            if sec:
                sections.append(sec)

        if not sections:
            answer = "I could not find relevant information for your request.\nFor further queries contact\nPhone: 0000 1111\nEmail: abcbank@gmail.com\n"
        else:
            combined = "\n".join(sections)

            # ✅ FIX YES/NO CURRENT ACCOUNT ERROR
            if "current account" in query.lower():
                answer = "Yes" if "Current Account" in combined else "No"
            else:
                prompt = f"""
Answer clearly using ONLY the context below.

Context:
{combined}

Question:
{query}

Answer:
"""
                answer = llm.invoke(prompt).strip()

    st.chat_message("assistant").write(answer)
    st.session_state.chat_history.append(("assistant", answer))

