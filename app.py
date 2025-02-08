from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import mysql.connector
import os

app = Flask(__name__)

# Database Connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "supplier_db",
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Open-source LLM (Hugging Face API)
llm = ChatOpenAI(model_name="mistralai/Mistral-7B-Instruct")

# LangGraph-based workflow
def get_product_info(product_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM products WHERE name = %s"
    cursor.execute(query, (product_name,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return product

def get_supplier_info(supplier_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM suppliers WHERE name = %s"
    cursor.execute(query, (supplier_name,))
    supplier = cursor.fetchone()
    cursor.close()
    conn.close()
    return supplier

# LLM Summarization
def summarize_supplier_info(supplier_data):
    template = """Summarize the following supplier details:
    {supplier_data}
    """
    prompt = PromptTemplate(template=template, input_variables=["supplier_data"])
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(supplier_data=supplier_data)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query")

    if "product" in user_query.lower():
        product_name = user_query.split("product")[-1].strip()
        product = get_product_info(product_name)
        return jsonify({"response": product if product else "Product not found."})

    elif "supplier" in user_query.lower():
        supplier_name = user_query.split("supplier")[-1].strip()
        supplier = get_supplier_info(supplier_name)
        summary = summarize_supplier_info(supplier) if supplier else "Supplier not found."
        return jsonify({"response": summary})

    return jsonify({"response": "Invalid query format."})

if __name__ == "__main__":
    app.run(debug=True)
