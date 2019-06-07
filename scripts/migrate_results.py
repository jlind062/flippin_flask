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

    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100))
    # price = db.column(db.Integer)
    # url = db.column(db.String(200))
    # scan_date = db.Column(db.TIMESTAMP)
    # city = db.Column(db.Integer(), db.ForeignKey("cities.id"))
    # ['name', 'clean_name', 'price', 'address', 'date', 'category_code', 'category', 'city_code', 'city', 'description',
    #  'comment', 'uploader', 'duplicate', 'profitable', 'last_updated', 'active']

    with conn_web.cursor() as cursor:
        for item in items:
            query = "INSERT INTO " + settings[web]["save_table"] + " (name, price, url, scan_date, city) " \
                    "VALUES (%s, %s, %s, %s, %s)"
            name = item['name']
            price = str(item['price'])
            url = item['address']
            scan_date = item['date'].strftime('%Y-%m-%d %H:%M:%S')
            city = '2'
            print(query, (name, price, url, scan_date, city))
            cursor.execute(query, (name, price, url, scan_date, city))
    conn_web.commit()
    conn_web.close()


if __name__ == "__main__":
    main("LOCAL_ITEMS", "LOCAL_WEB")