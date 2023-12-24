from bs4 import BeautifulSoup
import requests
import csv

def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'}).text.strip()

    except AttributeError:
        title = ""	

    return title

def get_price(soup):

    try:
        # Outer Tag Object
        price = soup.find("span",{"class":"a-price"}).find("span").text

    except AttributeError:
        price = ""	

    return price

if __name__ == '__main__':
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    search = 'GPU'
    URL = "https://www.amazon.ca/s?k=" + search + "&ref=nb_sb_noss"
    webpage = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "lxml")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))

    count = 0
    # Loop for extracting product details from each link 

    with open('gpu.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for link in links_list:
            if link.startswith("https://"):
                continue
            new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "lxml")
            title = get_title(new_soup)
            price = get_price(new_soup)
            if title != "" and count < 10:
                count += 1
                print(f"Product Title {count}= {title}")
                print(f"Product Price {count}= {price}")
                print("-----------------------------------")
                writer.writerow({'Title': title, 'Price': price})

            if count == 10:    
                break
