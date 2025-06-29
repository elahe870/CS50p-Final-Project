import requests
import sys

def calculate_score(data):
    try:
        market_data = data.get('market_data', {})
        
        # اطمینان از وجود فیلدها قبل از دسترسی
        price_change_24h = market_data.get('price_change_percentage_24h', 0)
        total_volume = market_data.get('total_volume', {}).get('usd', 0)
        market_cap = market_data.get('market_cap', {}).get('usd', 1)  # 0 division
        price_change_7d = market_data.get('price_change_percentage_7d', 0)
        
        # وزن‌دهی به فیلدها
        score = (
            price_change_24h * 0.3 +  # ۳۰% وزن
            (total_volume / 1e9) * 0.2 +  # ۲۰% وزن (حجم معاملات به میلیارد)
            (1 / market_cap * 1e9) * 0.2 +  # ۲۰% وزن (معکوس سرمایه‌سازی بازار)
            price_change_7d * 0.3  # ۳۰% وزن
        )
        return score
    except Exception as e:
        print(f"Error calculating score for data: {e}")
        return 0

def sort_cryptos_by_potential(coin_ids):
    results = []
    for coin_id in coin_ids:
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            response = requests.get(url)
            response.raise_for_status()  # چک کردن وضعیت HTTP
            data = response.json()
            
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

