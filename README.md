##About @dogepricebot
@dogepricebot is a automated twitter bot that scrapes dogecoin and Bitcoin pricing data from multiple exchanges, averages the data, and tweets it back on an hourly basis.

Current Version: 2.0

###Exchanges supported:
+ BTC-e
+ BTER
+ Cryptsy
+ Vircurex
+ always adding more

---

##How to use
You can simply follow @dogepricebot to get hourly price updates, or you can interact with @dogepricebot to check direct and indirect Dogecoin market rates.

@dogepricebot will accurately quote the market rate of dogecoin in any of the 168 global currencies, including:
+ Australian Dollar (AUD)
+ Brazilian Real (BRL)
+ Canadian Dollar (CAD)
+ Swiss Franc (CHF)
+ Chinese Yuan (CNY)
+ Euro (EUR)
+ British Pound Sterling (GBP)
+ Hong Kong Dollar (HKD)
+ Israeli Shekel (ILS)
+ Japanese Yen (JPY)
+ Norwegian Krone (NOK)
+ New Zealand Dollar (NZD)
+ Polish Zloty (PLN)
+ Russian Rubles (RUB)
+ Swedish Krona (SEK)
+ Singaporean Dollar (SGD)
+ Turkish Lira (TRY)
+ United States Dollar (USD)
+ South African Rand (ZAR)
+ And all the rest.

www.bitcoinaverage.com is used as a proxy for bitcoin price quotes, which are then requoted in dogecoin using the market DOGE:BTC rate.

In order to convert, all you need to know is the three character currency code for the currency you are trying to quote dogecoin in.

Here are some examples of the syntax:

    @dogepricebot convert 1000 DOGE to USD  
    @dogepricebot convert 50 SGD to dogecoin
    @dogepricebot convert 12000 dogecoin to CNY  

You'll notice that DOGE, dogecoin, and so on are used interchangeably. Any and all of these variations should work, the program is not case sensitive.

However, when defining the quoted currency you must use the appropriate currency code - slang terminology isn't quite there yet.

There are some examples responses:

    @twitter_user wow such convert: 1000.0 #dogecoin = 0.46 USD
    @twitter_user wow such convert: 50.0 SGD = 90114.45 #dogecoin
    @twitter_user wow such convert: 12000.0 #dogecoin = 11.80 CNY

However, it will not respond to users whose tweets are protected. I don't think there's much I can do there, but I will see.

---

##To-do list for v2.0
~~1. Write `scraper.py`~~

~~2. Write `assembler.py`  to average rates and create output~~

~~3. Write `streamer.py` to continuously post to twitter~~

~~4. Set up, test, and launch '@dogepricebot convert' interactive capabilities (`converter.py`)~~

~~5. Set up database for historical prices, ReplyIDs~~
6. Automate .db daily commit into github

##Milestones for v2.1
1. Expand conversion support to dynamically include other cryptocurrencies
2. Build plot.ly streaming illustrator
3. Connect `illustrator.py` to .db for continuous streaming

