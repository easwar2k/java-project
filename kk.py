"""Tiny demo shop API with five planted security issues for live VulnSentry demos. Do not deploy."""
import sqlite3
import subprocess
import os

from flask import Flask, request

app = Flask(__name__)

# DEMO-1: hard-coded credential in source code (CWE-798)
PAYMENT_API_KEY = os.environ.get("PAYMENT_API_KEY")



def find_products(category):
    # DEMO-2: SQL injection, input concatenated into the query (CWE-89)
    conn = sqlite3.connect("shop.db")
    return conn.execute("SELECT name, price FROM products WHERE category = '" + category + "'").fetchall()


@app.route("/products")
def products():
    return {"products": find_products(request.args.get("category", ""))}


@app.route("/invoice")
def invoice():
    # Fixed: no shell, and the order id must be a number, so it cannot inject commands or paths.
    try:
        order_id = int(request.args.get("order", ""))
    except ValueError:
        return {"error": "invalid order id"}, 400
    with open(f"invoices/{order_id}.txt") as f:
        return f.read()




@app.route("/")
def home():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run()

