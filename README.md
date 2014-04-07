##About @dogepricebot
@dogepricebot is a automated twitter bot that scrapes dogecoin and Bitcoin pricing data from multiple exchanges, averages the data, and tweets it back on an hourly basis.

It's a fun and easy way to stay on top of DOGE and BTC price movements!

###Exchanges supported:
+ BTC-e
+ BTER
+ CoinedUp
+ Cryptsy
+ More on the way!

---

###What to expect:
**UPDATE: You can now use @dogepricebot as a currency conversion calculator**
The conversion functionality is working! Currently the syntax is as follows:

    `@dogepricebot convert XXXX DOGE to USD`  
    `@dogepricebot convert XXXX dogecoins to USD`  
    `@dogepricebot convert XXXX DOGE to dollars`  
    `@dogepricebot convert XXXX dogecoin to dollars`  

Any and all variations should work. The reverse conversion should work as well. The response should look like:

    `@twitter_user wow such convert: XXXX DOGE = $Y.YY USD #dogepricebot`

However, it will not respond to users whose tweets are protected. I don't think there's much I can do there, but I will see.

###Milestones:
1. ~~Write streaming program~~ **DONE**
2. ~~Create Twitter bot~~ **DONE**
3. ~~Connect Twitter bot with streaming program~~ **DONE**
4. ~~Publicize tweets~~ **DONE**
5. ~~Create twitter profile logo~~ **DONE**
6. ~~Set up database for historical prices~~ **DONE**
7. ~~Migrate .db file onto Raspberry Pi cluster to begin building price database~~ **DONE**
8. Automate .db commit daily into github
9. ~~Set up, test, and launch `@dogepricebot convert` interactive capabilities~~ **DONE**
10. Pull from database for daily, weekly, and monthly visualizations using plot.ly
11. Post price chart with appropriate doge syntax "such uptick" "very slump" etc. 

