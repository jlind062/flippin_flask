import pymysql
import json


# connects to databases from settings file of name items and web
def connect(items, web):
    with open('settings.json', 'r') as s:
        data=s.read()
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
    settings, conn_items, conn_web = connect(items, web)

    # get items
    with conn_items.cursor() as cursor:
        query = "SELECT * FROM " + settings[items]["save_table"]
        cursor.execute(query)
        items = cursor.fetchall()
        print(items[0].keys())
    conn_items.close()

    with conn_web.cursor() as cursor:
        for item in items:
            query = "INSERT INTO " + settings[web]["save_table"] + " (name, price, url, scan_date, city, source) " \
                    "VALUES (%s, %s, %s, %s, %s)"
            name = item['name']
            price = str(item['price'])
            url = item['address']
            scan_date = item['date'].strftime('%Y-%m-%d %H:%M:%S')
            city = '2'
            source = 'Kijiji'

            cursor.execute(query, (name, price, url, scan_date, city, source))
    conn_web.commit()
    conn_web.close()


def get_source(url):
    #https://www.kijiji.ca/v-computer-components/city-of-toronto/xpg-spectrix-d41-ddr4-rgb-16gb-8gbx2-228-pin-ram/1442217377
    return


if __name__ == "__main__":
    main("LOCAL_ITEMS", "LOCAL_WEB")