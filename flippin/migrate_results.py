import pymysql
import json


# connects to databases from settings file of name items and web
def connect(items, web):
    with open('config.json', 'r') as s:
        data = s.read()
    settings = json.loads(data)

    conn_items = pymysql.connect(host=settings[items]["host"],
                                 user=settings[items]["user"],
                                 password=settings[items]["password"],
                                 db=settings[items]["database"],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    conn_web = pymysql.connect(host=settings[web]["host"],
                               user=settings[web]["user"],
                               password=settings[web]["password"],
                               db=settings[web]["database"],
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
    return settings, conn_items, conn_web


def main(items, web):
    # get connections to databases
    settings, conn_items, conn_web = connect(items, web)

    # get items from item database
    with conn_items.cursor() as cursor:
        query = "SELECT * FROM " + settings[items]["save_table"]
        cursor.execute(query)
        items = cursor.fetchall()
    conn_items.close()

    with conn_web.cursor() as cursor:
        # create dict for city names and id's
        query = "SELECT * FROM " + settings[web]["city_table"]
        cursor.execute(query)
        cities = cursor.fetchall()
        city_lookup = {}
        for city in cities:
            city_lookup[city['name']] = city['id']

        # write all items with non-null profit/resell value to web listings database
        for item in items:
            if item['resell_price'] is None: continue
            query = "INSERT INTO " + settings[web]["save_table"] + \
                    " (name, price, profit, resell_price, url, scan_date, city, source) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            name = item['clean_name']
            price = str(item['price'])
            resell = str(item['resell_price'])
            profit = str(item['profit'])
            url = item['address']
            scan_date = item['date'].strftime('%Y-%m-%d %H:%M:%S')
            city = str(city_lookup.get(item['city']))
            source = item['source']

            cursor.execute(query, (name, price, profit, resell, url, scan_date, city, source))
    conn_web.commit()
    conn_web.close()


if __name__ == "__main__":
    main("LOCAL", "AWS")