# CS50p-Final-Project : Crypto Sort


#### Video Demo:  https://youtu.be/BHTHUViL9dw

#### Description:

    This Python/Flask web application allows users to **enter cryptocurrency IDs**, and the app will **rank them by potential** based on real-time data from the [CoinGecko API](https://www.coingecko.com/en/api).
    The metrics used in this program to calculate performance of selected cryptos are:
     - 24h % price change
     - 7d % price change
     - Trading volume (USD)
     - Inverse of market capitalization (to favor undervalued coins)

    The formula used to calculate the score for each crypto is:
    
            price_change_24h * 0.3 +          # 30% weight: 24-hour price change percentage
            (total_volume / 1e9) * 0.2 +      # 20% weight: trading volume (scaled to billions of USD)
            (1 / market_cap * 1e9) * 0.2 +    # 20% weight: inverse market cap (favoring smaller caps)
            price_change_7d * 0.3             # 30% weight: 7-day price change percentage
        

#### Project address in github: 
    https://github.com/elahe870/CS50p-Final-Project


## CS50p-Final-Project: Crypto Sort

### Purpose:    

    This project can be a start point for generating signals to buy and sell Cryptocurrencies.

### Motivation:

    Interested in Cryptocurrency market, I tried to make a basic program to prepare a potential score and rating according to real-time API data gathered for selected Cryptocurrencies.

### Impact:

    this project can help beginners to practice how some parameters (like Market Cap and Trading Volume) can affect the potential of a coin.
    
### Features: 

    - Real-time data from CoinGecko
    - Custom scoring algorithm
    - Flask-based web User Interface


### Installation Tips:

    - Ensure `flask` and 'requests' and 'pytest' are installed via pip: 
        pip install flask requests pytest

  
### Future Improvements:

    - Add autocomplete part to help with coin selection
    - Add search symbol part to help with coin ID selection
    - Report the result in CSV or PDF format

### Acknowledgements

    During the development of this project, I used ChatGPT AI to assist with idea, design, implementation, and debugging.

    This tool was used to support learning and accelerate development, while ensuring that I understood and implemented all parts of the project myself in accordance with CS50’s academic honesty policy.

### Contact Information:

    es.haghighat95@gmail.com
    github and edx username: elahe870
