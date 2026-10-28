"""Tiny demo shop API with five planted security issues for live VulnSentry demos. Do not deploy."""
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)

# DEMO-1: hard-coded credential in source code (CWE-798)
PAYMENT_API_KEY = "demo-payment-key-12345"


def find_products(category):
    # DEMO-2: SQL injection, input concatenated into the query (CWE-89)
    conn = sqlite3.connect("shop.db")
    return conn.execute("SELECT name, price FROM products WHERE category = '" + category + "'").fetchall()


@app.route("/products")
def products():
    return {"products": find_products(request.args.get("category", ""))}


@app.route("/invoice")
def invoice():
    # DEMO-3: OS command injection through a shell command (CWE-78)
    order_id = request.args.get("order")
    return subprocess.check_output("cat invoices/" + order_id + ".txt", shell=True)


@app.route("/")
def home():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run()
