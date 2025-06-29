import requests
import sys
from score1 import calculate_score
from score1 import sort_cryptos_by_potential
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        coin_ids=request.form.get("name").strip().split(',')
        try:
            sorted_cryptos = sort_cryptos_by_potential(coin_ids)
            
            # نمایش نتایج
            if sorted_cryptos:
                print("\nSorted Cryptocurrencies by Potential:")
                for crypto in sorted_cryptos:
                    print(f"{crypto['name']} ({crypto['symbol']}): Score = {crypto['score']:.2f}")
            else:
                print("No valid data found for the provided cryptocurrencies.")
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {e}")
        return render_template("sort.html", sorted_cryptos=sorted_cryptos)
    else:
        return render_template("index.html")


