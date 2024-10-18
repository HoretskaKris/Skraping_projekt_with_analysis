import re
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Optional, Union

# Налаштування логування
logging.basicConfig(
    filename='logs/scraping_log.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8',
    level=logging.INFO
)

def connect(url: str) -> BeautifulSoup:
    '''Підключення до ресурсу'''
    try:
        r = requests.get(url)
        r.raise_for_status()  # Перевірка на помилки HTTP
        soup = BeautifulSoup(r.text, 'lxml')
        logging.info(f"Успішне підключення до {url}")
        return soup
    except requests.exceptions.RequestException as e:
        logging.error(f"Помилка підключення до {url}: {e}")
        exit(1)

def get_last_page(url: str) -> int:
    '''Знаходимо останню сторінку з продуктами'''
    try:
        last_page = connect(url).findAll('a', class_='pagination__link ng-star-inserted')
        logging.info("Знайдено останню сторінку з продуктами")
        return int(last_page[-1].text)
    except Exception as e:
        logging.error(f"Не вдалося знайти останню сторінку: {e}")
        exit(1)

def get_product_link(page: BeautifulSoup) -> Optional[str]:
    '''Посилання на окремий продукт'''
    try:
        link = page.find('a', class_='product-link goods-tile__heading').get('href')
        logging.info("Посилання на продукт отримано успішно")
        return link
    except AttributeError:
        logging.warning("Не вдалося знайти посилання на продукт.")
        return None

def get_specification_link(product_url: str) -> Optional[str]:
    '''Посилання на сторінку детальної специфікації кожного продукту'''
    try:
        soup = connect(product_url)
        specification_link_conn = soup.findAll('li', class_='tabs__item ng-star-inserted')
        if specification_link_conn:
            logging.info("Отримано посилання на специфікацію продукту")
            return specification_link_conn[1].find('a', class_='ng-star-inserted').get('href')
    except Exception as e:
        logging.error(f"Не вдалося знайти посилання на специфікацію: {e}")
    return None

def get_product_title(page: BeautifulSoup) -> str:
    '''Назва продукту'''
    try:
        title = page.find('a', class_='product-link goods-tile__heading').text
        logging.info("Назва продукту отримана успішно")
        return title
    except Exception as e:
        logging.error(f"Не вдалося отримати назву продукту: {e}")
        return ""

def get_product_price(page: BeautifulSoup) -> str:
    '''Ціна продукту'''
    try:
        price = re.sub("[^A-Za-z0-9]", "", page.find('span', class_='goods-tile__price-value').text[0:-2])
        logging.info("Ціна продукту отримана успішно")
        return price
    except Exception as e:
        logging.warning(f"Не вдалося отримати ціну продукту.")
        return ""

def pick_heders(link_to_product_specification: str) -> List[str]:
    '''Збір хедерів'''
    try:
        heders = []
        sections = connect(link_to_product_specification).findAll('section', class_='group ng-star-inserted')
        for section in sections:
            specification_name = section.find('dt', class_='label')
            heders.append(specification_name.text)
        logging.info("Хедери зібрані успішно")
        return heders
    except Exception as e:
        logging.error(f"Не вдалося зібрати хедери: {e}")
        return []

def get_specification_details(link_to_product_specification: str, heders_to_chek: List[str]) -> List[str]:
    '''Детальна специфікація продукту'''
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
        logging.info("Детальна специфікація продукту отримана успішно")
        return product_specification_details
    except Exception as e:
        logging.error(f"Не вдалося отримати детальну специфікацію продукту: {e}")
        return []

def save_to_csv(full_product_specification: List[List[Union[str, None]]], heder: List[str]) -> None:
    '''Збереження інформації до файлу'''
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'./Raw_data/Raw_data_{timestamp}.csv'
        df = pd.DataFrame(full_product_specification, columns=heder)
        df.to_csv(filename, sep=',', encoding='utf8', index=False)
        logging.info(f'Збір даних завершено. Загальна кількість зібраних продуктів: {len(full_product_specification)}')
        logging.info(f'--------Дані збережено в файл: {filename}')
    except Exception as e:
        logging.error(f"-------Помилка при збереженні даних до CSV: {e}")

def main() -> None:
    logging.info("--------Початок збору даних по продуктам")
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
        logging.error(f"----Помилка під час збору даних: {e}")

if __name__ == "__main__":
    main()
