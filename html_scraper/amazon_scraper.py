from datetime import datetime
import requests
import csv
import bs4
import concurrent.futures #both this and 
from tqdm import tqdm     # this is used to convert single treaded to multitreaded to expedite runtime
                          # Instantly make your loops show a smart progress meter

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"
#get user agent of your browser from https://www.whatismybrowser.com/detect/what-is-my-user-agent/
REQUEST_HEADER = { 

    'User-Agent':USER_AGENT,
    'Accept-Language':'en-US, en;q=0.5',

}   
N0_TREADS = 10

def get_page_html(url):
    response = requests.get(url=url, headers=REQUEST_HEADER) # sending url get request
    return response.content # get response will be in the form of html.


def get_product_price(soup):
    main_price_span = soup.find('span', attrs={
        'class': 'a-price a-text-price a-size-medium apexPriceToPay'
    })
    price_spans = main_price_span.find_all('span')
    for i in price_spans:
        price = price_spans.text.strip()
        try:
            return float(price)
        except ValueError:
            print("Value obtained could not be parsed")
            exit()


def get_product_tittle(soup):
    product_tittle = soup.find('span', id = 'productTitle')
    return product_tittle.text.strip()


def get_product_rating(soup):
    product_rating_div = soup.find('div',attrs={"id":'averageCustomerReviews'})
    product_rating_section = product_rating_div.find('i', attrs={'class':'a-icon a-icon-star a-star-4-5'})
    product_rating_span = product_rating_section.find('span')
    try:
        rating = product_rating_span.text.strip().split(' ')
        return float(rating[0]) 
    except ValueError:
        print('Value obtained for rating could not be parsed')
        exit()


def get_product_technical_details(soup):
    details={}
    technical_details_section = soup.find('div', id='prodDetails')
    data_table = technical_details_section.find_all('table', class_='prodDetTable')
    for table in data_table:
        table_rows = table.find_all('tr')
        for row in table_rows:
            row_key = row.find('th').text.strip()
            row_value = row.find('tb').text.strip()
            details[row_key]=row_value
    return details


def extract_product_info(url, output):
    product_info = {}
    print(f'Scraping_URL: {url}') # f-strings in Python - F-strings are faster than the two most commonly used string formatting mechanisms, which are % formatting and str.format(). 
    html = get_page_html(url=url) #creating object of the html scraped
    soup = bs4.BeautifulSoup(html,"lxml") #lxml is a Python library which allows for easy handling of XML and HTML files, and can also be used for web scraping
    product_info['price'] = get_product_price(soup)
    product_info['Tittle'] = get_product_tittle(soup)
    product_info['rating'] = get_product_rating(soup)
    product_info.update(get_product_technical_details(soup))
    output.append(product_info)


if __name__ == '__main__':
    product_data = []
    urls = []
    with open('amazon_products_urls.csv', newline='') as csvfile:
        urls = list(csv.reader(csvfile, delimiter=','))
        #for row in reader:
            #url = row[0] #extracting each url from amazon_products_url.csv
            #product_data.append(extract_product_info(url))

    with concurrent.futures.ThreadPoolExecutor(max_workers=N0_TREADS) as executor:
        for wkn in tqdm(range(0,len(urls))):
            executor.submit(extract_product_info, urls[wkn][0], product_data)
    output_file_name = 'output-{}.csv'.format(datetime.today().strftime("%m-%d-%Y"))
    with open(output_file_name,'w') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(product_data[0].keys())
        for product in product_data:
            writer.writerow(product.values())



