import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import datetime

# Фиктивная соц. активность (обычно подгружается из API Twitter/Reddit)
SOCIAL_SENTIMENT = {
    "bitcoin": 76,
    "ethereum": 83,
    "solana": 50,
    "dogecoin": 91,
    "cardano": 60,
    "ripple": 40
}

def fetch_price_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 6,
        "page": 1,
        "sparkline": "true"
    }
    r = requests.get(url, params=params)
    return r.json()

def compute_emotional_turbulence(prices, volume, social_score):
    price_variance = np.std(prices[-10:])
    volume_factor = np.log1p(volume)
    social_factor = social_score / 100.0
    score = (price_variance * 2 + volume_factor * 0.5 + social_factor * 3)
    return round(score, 2)

def build_heatmap(data):
    df = pd.DataFrame(data, columns=["Coin", "Turbulence"])
    df = df.pivot_table(index=["Coin"], values="Turbulence")
    
    plt.figure(figsize=(6,4))
    sns.heatmap(df, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title(f"Crypto Emotional Turbulence Map\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    plt.tight_layout()
    plt.show()

def main():
    print("Fetching data from CoinGecko...")
    market_data = fetch_price_data()
    result = []

    for coin in market_data:
        symbol = coin["id"]
        prices = coin["sparkline_in_7d"]["price"]
        volume = coin["total_volume"]
        social_score = SOCIAL_SENTIMENT.get(symbol, 50)  # Default neutral if unknown

        turbulence = compute_emotional_turbulence(prices, volume, social_score)
        result.append([symbol.capitalize(), turbulence])

    build_heatmap(result)

if __name__ == "__main__":
    main()
