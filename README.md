# WebScraping_PythonScript

This repository contains a Python script for web scraping GPU information from amazon. There are two files with two different functionalities. 

# Amazon Product Scraper (main.py)

This Python script (`main.py`) is designed to scrape product titles and prices from Amazon based on a search query. For now the search query has been set to 'GPU'. It utilizes the BeautifulSoup library for web scraping and the requests library to fetch HTML content of the website. It fetches the first 10 products from the query and writes the product title and prices to `gpu.csv`. 

## Prerequisites

Make sure to install the required dependencies by running:

```bash
pip install -r requirements.txt
```

- **Usage:**
  - Run the script: `python main.py`
- **Amazon Search:**
  - The script performs an Amazon search for the specified query (e.g., "GPU") and extracts product links.
- **Web Scraping:**
  - It iterates over the links, fetching the product title and price using web scraping.
- **Printing Details:**
  - The script prints the details of the first 10 products.
- **CSV File:**
  - It writes the product details to a CSV file (`gpu.csv`).
- **CSV Columns:**
  - The CSV file contains columns for product title and price.



# Amazon Product Scraper (sqldb1.py)

This Python script is designed to track the price of Amazon products (asin links or unique identifier for each products stored in gpu_list.csv). The data is a SQLite database. It uses web scraping to extract information such as product title and price, and it creates a price history for each product. The pice history curve can be visualized using matplotlib. 

## Dependencies

Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

- **Usage:**
  - Run the script: `python script_name.py`
- **Input:**
  - The script reads a list of Amazon product links from a CSV file (`gpu_list.csv`).
- **Web Scraping:**
  - For each product link, it fetches the product title and price using web scraping.
- **Database Update:**
  - The script updates a SQLite database (`products_tracker.db`) with the product information.
  - It includes the current price, initial price, and price percentage change.
- **Price History:**
  - The script records the price history in the `price_history` table, leveraging relational database properties.
- **Graphical Representation:**
  - The script generates a graphical representation of the price history for each product using Matplotlib.

- **Database Structure:**
  - **Table: products**
    - `product_id`: Primary key, unique identifier for each product.
    - `Product`: Text, the name of the product.
    - `CurrentPrice`: Real, the current price of the product.
    - `InitialPrice`: Real, the initial price of the product.
    - `PricePercentageChange`: Real, the percentage change in price.
    - `LastUpdated`: Text, timestamp of the last update.
  - **Table: price_history**
    - `price_id`: Primary key, unique identifier for each price entry.
    - `product_id`: Foreign key, references the `product_id` in the `products` table.
    - `scrape_time`: Text, timestamp of the scraping event.
    - `price`: Real, the price of the product at the given timestamp.
