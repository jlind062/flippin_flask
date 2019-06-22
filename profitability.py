from ebaysdk.finding import Connection as Finding
from fuzzywuzzy import fuzz
from scrape import ScanDBManager
import json


# searches ebay to get estimated price of item
def search_ebay(title, api):
    response = api.execute('findCompletedItems', {'keywords': title},
                           {'itemFilter': [{'name': 'Condition', 'value': 'Used'},
                                           {'name': 'SoldItemsOnly', 'value': 'true'}]})
    results = response.dict()["searchResult"].get("item")
    prices = []
    for item in results:
        name = str.lower(item['title'])
        price = float(item["sellingStatus"]["currentPrice"]["value"])
        # remove irrelevant listing with fuzzy string matching
        if fuzz.ratio(str.lower(title), name) > 30:
            prices.append(price)
    return avg_price(prices)


# finds the average price after filtering junk low prices
def avg_price(prices):
    avg = sum(prices)/len(prices)
    better_prices = [p for p in prices if p > avg/2.5]
    return sum(better_prices)/len(better_prices)


# updates the items in the database with estimated resell price and profitability
def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    api = Finding(siteid=config["EBAY"]["siteid"], appid=config["EBAY"]["appid"], config_file=None)
    db = ScanDBManager(config["LOCAL"], config["BASIC"])
    for item in db.get_items():
        try:
            resell_price = search_ebay(item[1], api)
            profit = resell_price - item[2]
        # if fails (usually because name is too dirty or item is not common on ebay), write null
        except Exception as e:
            print("error finding price for item %s" % item[1])
            resell_price = "NULL"
            profit = "NULL"
        db.update_price(item[5], resell_price, profit)


if __name__=="__main__":
    main()
