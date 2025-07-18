import requests
import sys
#from score1 import calculate_score
#from score1 import sort_cryptos_by_potential
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        
        coin_ids = extract_coin_ids(request.form.get("name"))
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

def extract_coin_ids(form_data):
    #extract input coins
    
    return form_data.strip().split(',')


def calculate_score(data):
    try:
        market_data = data.get('market_data', {})
        
        # check fields availability
        price_change_24h = market_data.get('price_change_percentage_24h', 0)
        total_volume = market_data.get('total_volume', {}).get('usd', 0)
        market_cap = market_data.get('market_cap', {}).get('usd', 1)  # 0 division
        price_change_7d = market_data.get('price_change_percentage_7d', 0)
        
        # وزن‌دهی به فیلدها
        score = (
            price_change_24h * 0.3 +          # 30% weight: 24-hour price change percentage
            (total_volume / 1e9) * 0.2 +      # 20% weight: trading volume (scaled to billions of USD)
            (1 / market_cap * 1e9) * 0.2 +    # 20% weight: inverse market cap (favoring smaller caps)
            price_change_7d * 0.3             # 30% weight: 7-day price change percentage
        )
        
        return score
    except Exception as e:
        print(f"Error calculating score for data: {e}")
        return 0
    
def data_fetch_per_coin(coin_id):
    try: 
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        response = requests.get(url)
        response.raise_for_status()  # چک کردن وضعیت HTTP
        data = response.json()
        return data
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Coin ID '{coin_id}' not found on CoinGecko. Skipping...")
        else:
            print(f"Error fetching data for {coin_id}: {e}")
    except Exception as e:
        print(f"Unexpected error for {coin_id}: {e}")


def sort_cryptos_by_potential(coin_ids):
    results = []
    for coin_id in coin_ids:
        try:
            data = data_fetch_per_coin(coin_id)
            # محاسبه امتیاز
            score = calculate_score(data)
            
            # ذخیره اطلاعات
            results.append({
                'name': data.get('name', 'Unknown'),
                'symbol': data.get('symbol', 'UNKNOWN').upper(),
                'score': score
            })
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Coin ID '{coin_id}' not found on CoinGecko. Skipping...")
            else:
                print(f"Error fetching data for {coin_id}: {e}")
        except Exception as e:
            print(f"Unexpected error for {coin_id}: {e}")
    
    # مرتب‌سازی بر اساس امتیاز
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results


def main():
    app.run()

if __name__ == "__main__":
    main()