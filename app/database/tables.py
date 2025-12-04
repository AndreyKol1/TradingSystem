def create_crypto_news_table():
    return """CREATE TABLE IF NOT EXISTS crypto_news(
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        publish_time DATE NOT NULL,
                        currency VARCHAR(3) NOT NULL,
                        relevance_score  REAL NOT NULL,
                        ticker_sentiment REAL NOT NULL,

                        CONSTRAINT unique_news_item UNIQUE (currency, title, publish_time)
                        )"""

def create_crypto_prices_table():
    return """CREATE TABLE IF NOT EXISTS crypto_prices(
                        id SERIAL PRIMARY KEY,
                        price_date DATE NOT NULL,
                        currency TEXT NOT NULL,
                        time_period TEXT NOT NULL,
                        open_price REAL NOT NULL,
                        highest_price REAL NOT NULL,
                        lowest_price REAL NOT NULL,
                        close_price REAL NOT NULL,
                        volume REAL NOT NULL,

                        CONSTRAINT unique_price_item UNIQUE (price_date, currency, time_period)
                       )"""

def create_fear_greed_table():
    return """CREATE TABLE IF NOT EXISTS fear_greed_index(
                        id SERIAL PRIMARY KEY,
                        classification TEXT NOT NULL,
                        value INT NOT NULL,
                        time_stamp DATE NOT NULL,

                        CONSTRAINT unique_greed_fear_item UNIQUE(time_stamp)
                        )"""
                        

