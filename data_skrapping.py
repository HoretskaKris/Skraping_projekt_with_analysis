import re
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Optional, Union

logging.basicConfig(
    filename='logs/scraping_log.log',
    filemode='a',
    format='%(asctime)s - %(levellevel)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8',
    level=logging.INFO
)

def connect(url: str) -> BeautifulSoup:
    '''Connect to the resource'''
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'lxml')
        logging.info(f"Successful connection to {url}")
        return soup
    except requests.exceptions.RequestException as e:
        logging.error(f"Connection error to {url}: {e}")
        exit(1)

def get_last_page(url: str) -> int:
    '''Find the last page with products'''
    try:
        last_page = connect(url).findAll('a', class_='pagination__link ng-star-inserted')
        logging.info("Last page with products found")
        return int(last_page[-1].text)
    except Exception as e:
        logging.error(f"Failed to find the last page: {e}")
        exit(1)

def get_product_link(page: BeautifulSoup) -> Optional[str]:
    '''Link to the individual product'''
    try:
        link = page.find('a', class_='product-link goods-tile__heading').get('href')
        logging.info("Product link retrieved successfully")
        return link
    except AttributeError:
        logging.warning("Failed to find the product link.")
        return None

def get_specification_link(product_url: str) -> Optional[str]:
    '''Link to the detailed product specification page'''
    try:
        soup = connect(product_url)
        specification_link_conn = soup.findAll('li', class_='tabs__item ng-star-inserted')
        if specification_link_conn:
            logging.info("Product specification link retrieved")
            return specification_link_conn[1].find('a', class_='ng-star-inserted').get('href')
    except Exception as e:
        logging.error(f"Failed to find the specification link: {e}")
    return None

def get_product_title(page: BeautifulSoup) -> str:
    '''Product title'''
    try:
        title = page.find('a', class_='product-link goods-tile__heading').text
        logging.info("Product title retrieved successfully")
        return title
    except Exception as e:
        logging.error(f"Failed to retrieve product title: {e}")
        return ""

def get_product_price(page: BeautifulSoup) -> str:
    '''Product price'''
    try:
        price = re.sub("[^A-Za-z0-9]", "", page.find('span', class_='goods-tile__price-value').text[0:-2])
        logging.info("Product price retrieved successfully")
        return price
    except Exception as e:
        logging.warning(f"Failed to retrieve product price.")
        return ""

def pick_heders(link_to_product_specification: str) -> List[str]:
    '''Retrieve headers'''
    try:
        heders = []
        sections = connect(link_to_product_specification).findAll('section', class_='group ng-star-inserted')
        for section in sections:
            specification_name = section.find('dt', class_='label')
            heders.append(specification_name.text)
        logging.info("Headers retrieved successfully")
        return heders
    except Exception as e:
        logging.error(f"Failed to retrieve headers: {e}")
        return []

def get_specification_details(link_to_product_specification: str, heders_to_chek: List[str]) -> List[str]:
    '''Detailed product specification'''
    try:
        product_specification_details = []
        pick_heders = []
        sections = connect(link_to_product_specification).findAll('section', class_='group ng-star-inserted')
        for section in sections:
            specification_name = section.find('dt', class_='label')
            pick_heders.append(specification_name.text)
            specification_value = section.find('dd', class_='value')
            product_specification_details.append(specification_value.text)
        missing_indices = [heders_to_chek.index(item) for item in heders_to_chek if item not in pick_heders]
        for i in missing_indices:
            product_specification_details.insert(i, "")
        logging.info("Product specification details retrieved successfully")
        return product_specification_details
    except Exception as e:
        logging.error(f"Failed to retrieve product specification details: {e}")
        return []

def save_to_csv(full_product_specification: List[List[Union[str, None]]], heder: List[str]) -> None:
    '''Save the information to a file'''
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'./Raw_data/Raw_data_{timestamp}.csv'
        df = pd.DataFrame(full_product_specification, columns=heder)
        df.to_csv(filename, sep=',', encoding='utf8', index=False)
        logging.info(f'Data collection completed. Total products collected: {len(full_product_specification)}')
        logging.info(f'--------Data saved to file: {filename}')
    except Exception as e:
        logging.error(f"-------Error saving data to CSV: {e}")

def main() -> None:
    logging.info("--------Starting product data collection")
    try:
        url_main = "https://rozetka.pl/laptopy-80004/c80004/page={page};producer=apple/"
        last_page = int(get_last_page(url_main))
        full_product_specification = []
        heders: List[str] = []
        for page in range(1, last_page + 1):
            products = connect(url_main.format(page={page})).findAll('li', class_='catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted')
            if heders == []:
                heders.extend(pick_heders(get_specification_link(get_product_link(products[0]))))
            for product in products:
                spec_link_product = get_specification_link(get_product_link(product))
                specification_detail = get_specification_details(spec_link_product, heders)
                specification_detail.insert(0, get_product_title(product))
                specification_detail.insert(1, get_product_price(product))
                full_product_specification.append(specification_detail)
        heder = ['Name', 'Price'] + heders
        save_to_csv(full_product_specification, heder)
    except Exception as e:
        logging.error(f"----Error during data collection: {e}")

if __name__ == "__main__":
    main()
