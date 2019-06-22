# flippin Deployment and Design: Back to Front

**Name: Josh Lindsay**
Website:  flippinapp.com  
**Project Title: flippin**  
**Instructor**: [Ghassem Tofighi](https://ghassem.com/)  
License: [MIT Licence](https://opensource.org/licenses/MIT)

Video Demo: 

## Technical Requirements:
a) A working deployed Flask website on Heroku
- Deployed on Amazon Web Services.

b) Having a Database connection and at least a CRUD (Create - Read - Update - Delete) operation within the project
- The flippin scripts access multiple databases in order to create, update, read, and delete items. 
- User registration provides does create, items page provides read, and profile management provides update and delete.

c) Bootstrap should be included, and at least 2 plugins of it (such as an image gallery) 
- Used [Data Tables](https://datatables.net/examples/styling/bootstrap4) to display item listings with pagination, filtering, and searching.
- Used [Bootstrap Show Password](http://bootstrap-show-password.wenzhixin.net.cn/home/) to provide toggle password when logging in.
- Used [Bootstrap Maxlength](https://mimo84.github.io/bootstrap-maxlength/) to field space remaining in Contact and Registration page.

d) JQuery library features (at least 2 features)
- Used $(document).ready functions to run javascript functions.
- Used selectors to easily select elements. 
- JQuery used in UI components like navbars.
- JQuery used in plugins like Data Tables.

e) Include an API in your website
- Use the ebay API (wrapped in python module, ebaysdk-python) to estimate resell value of items in flippin backend.
- Included passwordrandom.com api for recommending password during signup and collecting user ip.



## Project Overview

flippin is a SaaS solution aimed at improving used retail arbitrage around the world. 

What is arbitrage?
>"the simultaneous buying and selling of securities, currency, or commodities in different markets or in derivative forms in order to take advantage of differing prices for the same asset."

Just a fancy of way of saying reselling stuff for profit.

flippin isn't designed for big banks and funds selling commodities. It's designed for the actual human beings, you! flippin scans your local used marketplaces like craigslist and kijiji for good deals, Then you can scoop it up and resell for some nice beer money (or I guess avocado money for you gluten free hippies). Or just use the program to get that macbook at a great price!

Anyone can create an account and view the profitable items for their city. Just go to flippinapp.com, create an account, choose a city, and enjoy!

## Document Overview

The program is broken into two parts, the first is the package of scripts, called "flippin", which scans all the local listing websites, finds the profitable items, and uploads them to a web server. The second, "flippin_flask" is the web component which holds the back-end and front-end for the actual website, flippinapp.com. 

Mimicking this, the document is broken into two parts. The first shows how to configure and run flippin followed by an overview of all the scripts. The second part shows how to configure and run flippin_flask followed by an overview of project structure and design details.

After that, there will an appendix section with TODO's, a breakdown of the MYSQL database schema, and dependencies.

# Flippin

```mermaid
graph LR
Y[Craiglslist Scraper] -- scrape.py --> A
X[Kijiji Scraper] -- scrape.py --> A
Z((Config)) --> A

A[Local CSVs] -- upload_results.py --> B[MySQL Server]
B -- profitability.py --> B
Z((Config)) --> B
Z((Config)) --> B]
```

flippin is the package of python scripts that the website is based off of. It uses the Scrapy web framework to create is used a web scraper for each marketplace which collects all the listing info. The scrapers are run by the scrape.py script which stores the data locally in csv files. 

These csv files are the cleaned up and uploaded to a MySQL databse using upload_results.py. Then, the script profitability.py will use the ebay API to estimate the fair market price for all the items in the database and update them with profitability.

Project Structure:

```
flippin
│   config.json
│   scrape.py    
│	upload_results.py
|	profitability.py
└───results 
|   | 	(one source but multiple cities per csv)
│   │   <Kijiji_Output>.csv
│   │   <Craislist_Output>.csv
│   │   ...
│   │
│   └───old
│       │   <Old_Kijiji_Output>.csv
│       │   <Old_Craislist_Output>.csv
│       │   ...
│   
└───scrapers
	|   (one scraper per source)
    │   scraper_craigslist.py
    │   scraper_kijiji.py
    |   ...
```

## How to Run

1. Make sure to configure the config file with your own parameters. You must get your own eBay API key, and configure your own database with the same schema as in the appendix. You must allso fill in the to_scan table with urls you wish to scan.
2. Run scrapers.py to collect all the item data.
3. Run upload_results.py to upload the item data to the server.
4. Run profitability.py to get the estimated item price using the eBay sdk.

## Scripts and Files

### config.json
A JSON file which stores the various settings used by the various scripts. The sections are the following:

  BASIC:
  - result_path: path to scraper csv exports
  - word_filter: python list used to filter product names
  - char_filter: string of characters to filter from product names
  
  CRAWLER:
  - USER_AGENT: emulated browser used during scraping
  - FEED_FORMAT: filetype of scraper export
  - LOG_ENABLED: boolean value denoting logging status
  - DOWNLOAD_DELAY: delay between scraping pages
  
  SCAN:
  - "source": [path to save results, spider class name]
  
  LOCAL:
  - host: MySQL database host
  - user: database username
  - password: database password
  - database": database name
  - scan_table": name of table with urls to scan
  - save_table": name of table to save results 

LOCAL WEB / WEB:
- Same as above but with parameters for web host like AWS or a local web host. This is the database for the flippin_flask website.

EBAY:
- siteid: eBay Country Code
- appid: eBay api ID

### scraper_(source).py

The scraper or 'spider' works by parsing a given web page using html and css tags. The sequence of operations looks something like this:

1.  An initial web page is given to the spider.
2.  Sections of web page's source code is separated by a recurring tag, with each tag (hopefully) representing an item.
3.  Each item's block of source code are then parsed for the desired data.
4.  Items are saved in some format.
5.  The next web page is loaded (by selecting some link on the page, in this case the 'next' button to load the next list page), and the process is repeated until no more web pages are loaded.

All the spiders are used to collect item listing data from various marketplaces like Craigslist and Kijiji. The powerful framework [Scrapy](https://scrapy.org) is used for this which is itself built off of [TwisterReactor](https://twistedmatrix.com/trac/).

### scrape.py

scrape.py is made up of two main classes:

**ScanDBManager**: holds all the relevant functions for querying the database and creating tables. It is built off of pymysql. It also holds information like word filters used to clean up the listing names. It is used in both scrape.py and upload_results.py.

**ScanManager**: manages and runs all of the scrapers. It will load the scraping profiles from the flippin database defined in config.json and run them, saving the results as csvs. 

### upload_results.py

Has one class, CSVManager, which parses through the csv data and uploads it the server. 

### profitability.py

Has no classes, just methods. This script will estimate the price from all the items in the database by querying eBay for the latest 50 sold items. It will remove outliers (those items with different names and prices that vary widely from the average) and compute the average resell price. It will also compute the expected profit and update the database with the results.

### migrate_results.py

This script is used to copy all the item listings with resell data to another database. The main purpose of this is to copy the items to the database used for the flippin_flask backend. Although this is not necessary, it is used to save on server costs by doing most of the brunt work on a local web server, and only uploading what's necessary to the instance of a host like Amazon Web Services.

# flippin_flask

Flippin_flask is the web back-end and front end wrapper for the flippin script package. It is a prototype of SaaS web client where users can browse the flippin results for their city. It can be viewed at flippinapp.com.

It is hosted on Amazon Web Services via Elastic Beanstock with a separate AWS database for more versatility than linking the database directly to the AWS instance.

```mermaid
graph LR
Y[flippin]  --> A[Item Database]
Z((Config)) --> A
Z((Config)) --> B
A --> B[Web Backend]
B --> C[Web Frontend]
C --> B
```

The website currently has the following functionality:
- User account CRUD capabilities with registration, deletion, and profile modification.
- The ability to view flippin results for a chosen city with filtering, pagination, etc.
- A landing page which advertises the product.
- A contact page which sends the users request to a support email.

Project Structure:

```
flippin_flask
│   config.py
│   application.py    
| 	requirements.txt
│	models.py
|	forms.py
└───static 
|   | 	bootstrap-maxlength.js
│   │   bootstrap_flux.css
│   │   ...
│   └───img
│       │   money.svg
│       │   ...
│   
└───templates
|	|   login.html
|   │   home.html
|   │   ...
|   │ 
│   └───includes
|   	| _navbar.html
|       | _footer.html
|       | ...
```

## How to Run

1. Create a MySQL server and configure the config.py file
2. Ensure you are using a python environment (venv encouraged) with the dependencies installed.
3. Run the models.py file to conveniently create the tables for you.
4. Manually insert at least one city into the cities table.
5. Make sure the migrate_results.py script was run so that the listings database will be populated with results.
6. Run the flask application.py or zip the entire project to deploy on a web host like Amazon Web Services.

## Code Overview

## application.py
The main code for the flask application. Contains the routes, web requests, mail server, database instance, and everything else. All the backend logic is here.

Models.py

# Appendix

## TODO's

- Add hamburger toggle for navbar on smaller screens
- Generate page for each item
- Add user guides
- Add category filter for eBay api search
- Add support for different countries and currency
- Unify flippin scripts into one procedure
- Save eBay queries to generate private item database to save on queries and speed up runtime
- Clean up flippin scripts by using kwargs to improve readability
- Add FAQ

## flippin database structure:

Tables:
- scan_results
- to_scan

### scan_results

Field |Type | Null | Key | Default | Extra
--- | --- | --- | --- | --- | ---
| name  | varchar(255) | NO | | NULL  | |
| clean_name  | varchar(255) | YES  | | NULL  | |
| price | int(11)  | NO | | NULL  | |
| resell_price  | float  | YES  | | NULL  | |
| profit  | float  | YES  | | NULL  | |
| address | varchar(255) | NO | PRI | NULL  | |
| source  | varchar(50)  | YES  | | NULL  | |
| date  | date | NO | | NULL  | |
| category_code | varchar(255) | NO | | NULL  | |
| category  | varchar(255) | YES  | | NULL  | |
| city_code | varchar(255) | YES  | | NULL  | |
| city  | varchar(255) | YES  | | NULL  | |
| description | text | YES  | | NULL  | |
| comment | text | YES  | | NULL  | |
| uploader  | varchar(255) | YES  | | NULL  | |
| duplicate | tinyint(1) | YES  | | 0 | |
| profitable  | tinyint(1) | YES  | | NULL  | |
| last_updated  | datetime | YES  | | NULL  | |
| active  | tinyint(1) | YES  | | NULL  | |

### to_scan

Field |Type | Null | Key | Default | Extra
--- | --- | --- | --- | --- | ---
| city | varchar(255) | NO | | NULL  | |
| link | varchar(255) | NO | | NULL  | |
| source | varchar(255) | YES  | | NULL  | |
| info | varchar(255) | YES  | | NULL  | |

## flippin_flask database structure:

Tables:
- cities
- listings
- users

### cities:

Field |Type | Null | Key | Default | Extra
--- | --- | --- | --- | --- | ---
id | int(11) |NO | PRI | Null | auto_increment 
name | varchar(50)  | NO | | NULL  |  |
city_codes | varchar(300) | YES  | | NULL  |  |
last_updated | timestamp  | YES  | | NULL  |

### listings

Field |Type | Null | Key | Default | Extra
--- | --- | --- | --- | --- | ---
| id  | int(11)  | NO | PRI | NULL  | auto_increment |
| name  | varchar(100) | YES  | | NULL  |  |
| price | int(11)  | YES  | | NULL  |  |
| profitability | float  | YES  | | NULL  |  |
| resell_price  | float  | YES  | | NULL  |  |
| url | varchar(200) | YES  | | NULL  |  |
| scan_date | timestamp  | YES  | | NULL  |  |
| city  | int(11)  | YES  | MUL | NULL  |  |
| source  | varchar(50)  | YES  | | NULL  |  |

### users

Field |Type | Null | Key | Default | Extra
--- | --- | --- | --- | --- | ---
| id  | int(11)  | NO | PRI | NULL  | auto_increment  |
| first | varchar(50)  | YES  | | NULL  | |
| last  | varchar(50)  | YES  | | NULL  | |
| email | varchar(75)  | YES  | | NULL  | |
| username  | varchar(50)  | YES  | | NULL  | |
| city  | int(11)  | YES  | MUL | NULL  | |
| password  | varchar(100) | YES  | | NULL  | |
| ip  | varchar(30)  | YES  | | NULL  | |
| register_date | timestamp  | NO | | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |

## flippin example config:
```
{
  "BASIC": {
    "result_path": "/Users/josh/PycharmProjects/flippin/results",
    "word_filter": ["warranty", "new", "like", "condition", "extra", "used", "very", "accessories",
                  "only", "in", "days", "with", "and", "excellent", "brand", "good", "factory",
                  "useable", "clean", "perfect", "&", "+", "/", "usable", "mint", "buy",
                  "from", "asap", "new", "selling", "Selling", "awesome", "deal", "business", "immaculate",
                  "excellent", "lots", "for", "sale", "sealed", "box", "starting", "excelent", "(new)", "rarely",
                  "almost", "-", "_", "[new]", "we", "deliver", "need", "gone"],
    "char_filter": "()!/[].^~"
  },
  "CRAWLER": {
    "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "FEED_FORMAT": "csv",
    "LOG_ENABLED": true,
    "DOWNLOAD_DELAY": "1",
    "RANDOMIZE_DOWNLOAD_DELAY": "1"
  },
  "SCAN": {
    "Kijiji":["/Users/josh/PycharmProjects/flippin/results/Kijiji.csv", "Kijiji.Main()"],
    "Craigslist":["/Users/josh/PycharmProjects/flippin/results/Craigslist.csv", "Craigslist.Main()"]
  },
  "LOCAL": {
    "host":"localhost",
    "user":"root",
    "password":"root",
    "database":"flippin",
    "scan_table":"to_scan",
    "save_table":"scan_results"
  },
  "LOCAL_WEB": {
    "host":"localhost",
    "user":"root",
    "password":"root",
    "database":"flippin_flask",
    "city_table":"cities",
    "save_table":"listings"
  },
  "AWS": {
    "host":"x.amazonaws.com",
    "user":"root",
    "password":"root",
    "database":"flippin",
    "city_table":"cities",
    "save_table":"listings"
  },
  "EBAY": {
    "siteid":"EBAY-ENCA",
    "appid":"(censored)"
  }
}
```

## flippin_flask example config:

```
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'x'
    MAIL_SERVER = "smtp.zoho.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'support@flippinapp.com'
    MAIL_PASSWORD = 'root'


class LocalConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/flippin_flask'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class AWSConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://j1lindsay:root@x:3306/flippin'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## flippin_flask dependencies:
```
blinker==1.4
certifi==2019.6.16
chardet==3.0.4
Click==7.0
Flask==1.0.3
Flask-Mail==0.9.1
Flask-SQLAlchemy==2.4.0
Flask-WTF==0.14.2
idna==2.8
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
passlib==1.7.1
PyMySQL==0.9.3
requests==2.22.0
SQLAlchemy==1.3.3
urllib3==1.25.3
Werkzeug==0.15.4
WTForms==2.2.1
```
