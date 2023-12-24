from bs4 import BeautifulSoup
import requests
import sqlite3
import matplotlib.pyplot as plt 
from datetime import datetime
from main import get_title, get_price
import csv

conn = sqlite3.connect('products_tracker.db')
# conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    Product TEXT UNIQUE,
    CurrentPrice REAL,
    InitialPrice REAL,
    PricePercentageChange REAL,
    LastUpdated TEXT
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS price_history (
    price_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    scrape_time TEXT,
    price REAL,
    FOREIGN KEY (product_id) REFERENCES products (product_id)
    )""")

def add_product_to_price_history(product_id, scrape_time, price):
    with conn:
        c.execute("INSERT INTO price_history (product_id, scrape_time, price) VALUES (:product_id, :scrape_time, :price)", {'product_id': product_id, 'scrape_time': scrape_time, 'price': price})

def add_product_to_database(product, price): 
    with conn:
        c.execute("SELECT * FROM products WHERE Product=:Product", {'Product': product})
        existing_product = c.fetchone()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if existing_product:
            c.execute("UPDATE products SET LastUpdated=:LastUpdated WHERE Product=:Product", {'Product': product, 'LastUpdated': current_time})
            product_id = existing_product[0]
            add_product_to_price_history(product_id, current_time, price)
            existing_price = parse_price(existing_product[2])
            initial_price = parse_price(existing_product[3])
            parsed_price = parse_price(price)
            if existing_price and initial_price:
                if existing_price != parsed_price:
                    price_percentage_change = 100 + (parsed_price - initial_price) / initial_price * 100
                    c.execute("""UPDATE products SET CurrentPrice=:CurrentPrice, PricePercentageChange=:PricePercentageChange WHERE Product=:Product""", {'Product': product, 'CurrentPrice': price, 'PricePercentageChange': price_percentage_change})
        else:
            #update both table
            c.execute("INSERT INTO products (Product, CurrentPrice, InitialPrice, PricePercentageChange, LastUpdated) VALUES (:Product, :CurrentPrice, :InitialPrice, :PricePercentageChange, :LastUpdated)", {'Product': product, 'CurrentPrice': price, 'InitialPrice': price, 'PricePercentageChange': 100, 'LastUpdated': current_time})
            #Fetch product id
            c.execute("SELECT product_id FROM products WHERE Product=:Product", {'Product': product})
            product_id = c.fetchone()[0]
            #update table
            add_product_to_price_history(product_id, current_time, price)

def parse_price(price_str):
    """Converts a price string to a float, removing dollar sign and commas."""
    if price_str:
        return float(price_str.replace('$', '').replace(',', ''))
    return None

def read_csv():
    with open('gpu_list.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        return [item[0] for item in reader]

def plot_price_history(product_id):
    with conn:
        c.execute("SELECT scrape_time, price FROM price_history WHERE product_id=:product_id", {'product_id': product_id})
        price_history = c.fetchall()

        if price_history:
            timestamps, prices = zip(*price_history)
            
            # Convert timestamps to datetime objects for better plotting
            timestamps = [datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") for timestamp in timestamps]

            plt.plot(timestamps, prices, label= "Product: " + str(product_id))

if __name__ == '__main__':

    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    # Store the links
    asin_list = read_csv()
    count = 1
    for link in asin_list:
        new_webpage = requests.get("https://www.amazon.ca/dp/" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "lxml")
        title = get_title(new_soup)
        price = get_price(new_soup)
        print(f"Product Title {count}= {title}")
        print(f"Product Price {count}= {price}")
        if title and price:  
            add_product_to_database(title, price)
        print("-----------------------------------")
        count += 1
    
    #graph in matplotlib
    c.execute("SELECT product_id FROM products")
    products = c.fetchall()

    for product_id in products:
        plot_price_history(product_id[0])

    # Customize the plot
    plt.xlabel('Scrape Time')
    plt.ylabel('Price')
    plt.title('Price History for Products')
    plt.legend()
    plt.show()


conn.commit()
conn.close()
