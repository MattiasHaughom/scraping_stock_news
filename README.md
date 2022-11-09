# scraping_stock_news
Scrapes and estimates the sentiment of the stock/market specific news posted on the norwegian newspaper Dagens Næringsliv's overview page.

## Data
The other data I have uploaded into the ".zip" folder:  
all_tickers.xlsx - list of all tickers and their company name in the OBX stock index  
norskDict.xlsx - list of positve and negative words for norwegian stock news, for sentiment analysis  
OBStickers.xlsx - list of tickers and their sector/industry, where these are available  


## Script
The script only outputs the current day's news, and only news regarding norwegian companies. The script also clicks on all the "Les mer" to get more text and information about from each news post. Finally the loop measures the sentiment for each post using the norwegian dictionary and outputs the name of the company and the total sentiment.


