##About @dogepricebot
@dogepricebot is a automated twitter bot that scrapes dogecoin and Bitcoin pricing data from multiple exchanges, averages the data, and tweets it back on an hourly basis.

Current Version: 1.5

###Exchanges supported:
+ BTC-e
+ BTER
+ CoinedUp
+ Cryptsy
+ Vircurex
+ always adding more

---

##How to use
You can simply follow @dogepricebot to get hourly price updates, or you can interact with @dogepricebot to check direct and indirect Dogecoin market rates.

19 supported currencies:
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

The syntax is as follows:

    `@dogepricebot convert 1000 DOGE to USD`  
    `@dogepricebot convert 50 SGD to dogecoin`  

You'll notice that DOGE, dogecoin, and so on are used interchangeably. Any and all of these variations should work, the program is not case sensitive.

However, when defining the alt currency you must use the appropriate currency code - slang terminology isn't quite there yet.

The response should look like:

    `@twitter_user wow such convert: 1000.0 #dogecoin = 0.46 USD`

Or:

    `@twitter_user wow such convert: 50.0 SGD = 90114.45 #dogecoin`

However, it will not respond to users whose tweets are protected. I don't think there's much I can do there, but I will see.

---

##To-do list:
1. ~~Write streaming program~~ **DONE**
2. ~~Create Twitter bot~~ **DONE**
3. ~~Connect Twitter bot with streaming program~~ **DONE**
4. ~~Publicize tweets~~ **DONE**
5. ~~Create twitter profile logo~~ **DONE**
6. ~~Set up database for historical prices~~ **DONE**
7. ~~Migrate .db file onto Raspberry Pi cluster to begin building price database~~ **DONE**
8. Automate .db commit daily into github
9. ~~Set up, test, and launch `@dogepricebot convert` interactive capabilities~~ **DONE**
10.~~Expand currency support~~ **DONE**
11. Pull from database for daily, weekly, and monthly visualizations using plot.ly
12. Post price chart with appropriate doge syntax "such uptick" "very slump" etc. 

