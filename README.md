# 🏦 ABC Bank Customer Support Assistant (RAG Bot)

A **Retrieval-Augmented Generation (RAG)** based customer support
chatbot built using **Streamlit, LangChain, FAISS, and Hugging Face
models**.\
The bot securely retrieves **customer-specific banking details** such as
account balance, loans, cards, and transactions from structured text
files.

------------------------------------------------------------------------

## 🚀 Features

-   🔐 Secure login-based access\
-   🧍 Per-customer data isolation\
-   📄 Retrieves data from multiple text files\
-   🔍 RAG-based intelligent search (FAISS + embeddings)\
-   💬 Conversational chat interface (Streamlit)\
-   🚫 Prevents access to other customers' data\
-   ⚡ Fully local & open-source (no paid APIs)

------------------------------------------------------------------------

## 🗂 Project Structure

    ABC_Bank_RAG_Bot/
    │
    ├── app.py
    ├── ingest.py
    ├── requirements.txt
    ├── README.md
    │
    ├── data/
    │   ├── bank_records_part1.txt
    │   ├── bank_records_part2.txt
    │   ├── bank_records_part3.txt
    │   └── bank_records_part4.txt
    │
    ├── vectorstore/
    └── screenshots/

------------------------------------------------------------------------

## 📄 Input Data Format

    Customer ID: CUST1001

    === ACCOUNT SUMMARY ===
    Savings Account Balance: 1,25,000 INR
    Account Type: Savings Account

    === LOAN DETAILS ===
    Home Loan: Active
    Outstanding Amount: 18,50,000 INR

    === CARD DETAILS ===
    Debit Card: Active
    Credit Card: Active (Platinum)

    === TRANSACTIONS ===
    - 15,000 debited on 01-Jan-2026
    - 50,000 credited on 28-Dec-2025

------------------------------------------------------------------------

## ⚙️ Installation & Setup

### 1. Clone Repository

``` bash
git clone https://github.com/your-username/ABC_Bank_RAG_Bot.git
cd ABC_Bank_RAG_Bot
```

### 2. Create Virtual Environment

``` bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4. Ingest Data

``` bash
python ingest.py
```

### 5. Run Application

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

## 🔐 Demo Login Credentials

  Customer ID   Password
  ------------- ----------
  CUST1001      CUST1001
  CUST1002      CUST1002
  CUST1003      CUST1003
  CUST1004      CUST1004

------------------------------------------------------------------------

## 💬 Sample Queries

-   Give me my account balance\
-   Do I have any active loans?\
-   Show my credit card details\
-   Give me my recent transaction history

------------------------------------------------------------------------

## 🧠 Tech Stack

-   Python 3.11
-   Streamlit
-   LangChain
-   FAISS
-   Hugging Face Transformers

------------------------------------------------------------------------

## 👩‍💻 Author

**Tejashree Ganesh**\
RAG Bot \| NLP \| Streamlit \| LangChain

------------------------------------------------------------------------

## 📜 License

Educational use only.
