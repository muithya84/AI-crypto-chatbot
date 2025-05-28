
import requests
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

# Ethics disclaimer
def ethics_disclaimer():
    print("\nDisclaimer: Crypto investments are risky always do your own research (DYOR)!\n")

# Real-time price fetch from CoinGecko API
def get_real_time_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        price = data[coin_id]["usd"]
        return price
    except Exception:
        return None

# Static crypto dataset with sustainability and market info
crypto_data = {
    "bitcoin": {
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 4,
    },
    "ethereum": {
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6,
    },
    "cardano": {
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 9,
    },
    "solana": {
        "market_cap": "high",
        "energy_use": "low",
        "sustainability_score": 8,
    }
}

# NLP: Detect user intent using NLTK tokens
def detect_intent(query):
    tokens = word_tokenize(query.lower())
    if "long-term" in tokens and "growth" in tokens:
        return "long_term_growth"
    if "price" in tokens or "current" in tokens:
        return "price_check"
    if "trending" in tokens or "rising" in tokens:
        return "trending_up"
    if "sustainable" in tokens or "energy" in tokens:
        return "sustainability"
    if "help" in tokens:
        return "help"
    return "unknown"

# Business logic: recommend coins for long term growth
def recommend_long_term():
    recommended = []
    for coin, data in crypto_data.items():
        if (data["market_cap"] == "high" and
            data["energy_use"] == "low" and
            data["sustainability_score"] > 7):
            recommended.append(coin)

    if not recommended:
        for coin, data in crypto_data.items():
            if data["market_cap"] == "high":
                recommended.append(coin)
    return recommended

# Respond to user queries based on detected intent
def respond_to_query(query):
    intent = detect_intent(query)

    if intent == "long_term_growth":
        recs = recommend_long_term()
        if recs:
            coins = ", ".join([c.title() for c in recs])
            return f"CryptoBuddy: {coins} are good choices for long-term growth based on market cap and sustainability!"
        else:
            return "CryptoBuddy: Sorry, no cryptocurrencies meet the criteria right now."

    elif intent == "price_check":
        for coin in crypto_data.keys():
            if coin in query.lower():
                price = get_real_time_price(coin)
                if price:
                    return f"CryptoBuddy: The current price of {coin.title()} is ${price} USD."
                else:
                    return f"CryptoBuddy: Sorry, I couldn't fetch the price for {coin.title()} right now."
        return "CryptoBuddy: Please specify a cryptocurrency name to check the price."

    elif intent == "trending_up":
        trending = ["bitcoin", "cardano", "solana"]  # static list; could be dynamic from API
        coins = ", ".join([c.title() for c in trending])
        return f"CryptoBuddy: These cryptocurrencies are trending up: {coins}"

    elif intent == "sustainability":
        sustainable = [c for c, d in crypto_data.items() if d["energy_use"] == "low" and d["sustainability_score"] > 7]
        if sustainable:
            coins = ", ".join([c.title() for c in sustainable])
            return f"CryptoBuddy: Most sustainable cryptocurrencies: {coins}"
        else:
            return "CryptoBuddy: No sustainable coins found in the current dataset."

    elif intent == "help":
        return ("CryptoBuddy: Try asking:\n"
                "- Which crypto should I buy for long-term growth?\n"
                "- What's the current price of Bitcoin?\n"
                "- Which crypto is trending up?\n"
                "- What is the most sustainable coin?")

    else:
        return "CryptoBuddy: Sorry, I didn't understand that. Try asking about prices, trends, or sustainability."

# Chatbot loop with ethics disclaimer
def chatbot():
    print("Welcome to CryptoBuddy!")
    ethics_disclaimer()
    print("Type 'exit' to quit or 'help' for examples.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = respond_to_query(user_input)
        print(response)
        ethics_disclaimer()

# Run chatbot
if __name__ == "__main__":
    chatbot()
