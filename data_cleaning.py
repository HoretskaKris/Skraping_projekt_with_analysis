import logging
import pandas as pd
import re
from datetime import datetime
from typing import Dict, Union

logging.basicConfig(
    filename='logs/cleaning_data_log.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8',
    level=logging.INFO
)

translation_dict: Dict[str, str] = {
    'Name': 'Name',
    'Price': 'Price_zl',
    'Seria': 'Series',
    'Przekątna ekranu': 'Screen_Diagonal_inches',
    'Procesor': 'Processor',
    'Pamięć RAM': 'RAM_Memory_GB',
    'Pojemność SSD': 'SSD_Capacity_GB',
    'Producent karty graficznej': 'Graphics Card Manufacturer',
    'Pojemność akumulatora, Wh': 'Battery_Capacity_Wh',
    'Karty sieciowe': 'Network_Cards_Wi-Fi',
    'Krótka charakterystyka': 'Short_Description'
}

processor_cores_dictionary: Dict[str, int] = {
    "Ośmiordzeniowy": 8,
    "10-rdzeniowy": 10,
    "Dwunastordzeniowy": 12,
    "12-rdzeniowy": 12,
    "Jedenасторденіовий": 11,
    "Czternastordzeniowy": 14,
    "Szesnastordzeniowy": 16
}

def download_raw_data(file_name: str) -> pd.DataFrame:
    '''Load raw data for processing'''
    try:
        logging.info("Loading data from file")
        df = pd.read_csv(file_name)
        logging.info(f"Data loaded: {file_name}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_name}")
        exit(f"File {file_name} not found. Exiting program.")
    except Exception as e:
        logging.error(f"Error loading file {file_name}: {e}")
        exit(f"Error: {e}. Exiting program.")

def del_spaces(date_frame: pd.DataFrame) -> pd.DataFrame:
    '''Remove all extra spaces from the data'''
    logging.info("Removing extra spaces")
    date_frame = date_frame.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    return date_frame

def rename_columns(date_frame: pd.DataFrame, translation_dict: Dict[str, str]) -> pd.DataFrame:
    '''Rename all columns to English'''
    logging.info("Renaming columns")
    return date_frame.rename(columns=translation_dict)

def extract_series(series_name: str, pattern: str) -> Union[str, None]:
    '''Extract series name using a regular expression for normalizing the Series column'''
    if isinstance(series_name, str):
        match = re.search(pattern, series_name)
        if match:
            return match.group(0)
    return series_name

def normalize_Seria_column(date_frame: pd.DataFrame) -> pd.DataFrame:
    '''Normalize the Series column'''
    logging.info("Normalizing Series column")

    date_frame['Series'] = date_frame['Series'].fillna(date_frame['Name'])

    seria_pattern = r'(MacBook\s*\w{0,3})'

    date_frame['Series'] = date_frame['Series'].apply(lambda series_name: extract_series(series_name, seria_pattern))

    return date_frame

def normalize_Price_column(date_frame: pd.DataFrame) -> pd.DataFrame:
    '''Normalize the Price column'''
    logging.info("Normalizing Price_zl column")
    date_frame['Price_zl'] = date_frame['Price_zl'].replace({r'\$': '', ',': '', ' ': ''}, regex=True)
    date_frame['Price_zl'] = pd.to_numeric(date_frame['Price_zl'], errors='coerce')
    return date_frame

def normalize_ScreenDiagonal_column(date_frame: pd.DataFrame) -> pd.DataFrame:
    '''Normalize the Screen_Diagonal column'''
    logging.info("Normalizing Screen_Diagonal_inches column")
    date_frame['Screen_Diagonal_inches'] = date_frame['Screen_Diagonal_inches'].replace(r'[^\d.]', '', regex=True)
    date_frame['Screen_Diagonal_inches'] = pd.to_numeric(date_frame['Screen_Diagonal_inches'], errors='coerce')
    return date_frame

def normalize_Processor_column(date_frame: pd.DataFrame, processor_cores_dictionary: Dict[str, int]) -> pd.DataFrame:
    '''Normalize and create Processor and Processor Cores columns'''
    logging.info("Normalizing Processor and creating Processor Cores columns")
    date_frame['Processor_Cores'] = date_frame['Processor'].apply(lambda x: x.split("Apple")[0].strip() if isinstance(x, str) and "Apple" in x else x)
    date_frame['Processor_Cores'] = date_frame['Processor_Cores'].replace(processor_cores_dictionary)
    date_frame['Processor'] = date_frame['Processor'].apply(lambda x: "Apple" + x.split("Apple", 1)[1] if isinstance(x, str) and "Apple" in x else x)
    return date_frame

def normalize_RamMemory_column(date_frame: pd.DataFrame) -> pd.DataFrame:
    '''Normalize the RAM_Memory column'''
    logging.info("Normalizing RAM_Memory_GB column")
    date_frame['RAM_Memory_GB'] = date_frame['RAM_Memory_GB'].apply(lambda x: re.sub(r'\D', '', str(x)))
    date_frame['RAM_Memory_GB'] = pd.to_numeric(date_frame['RAM_Memory_GB'], errors='coerce').astype('Int64')
    return date_frame

def normalize_SSDcapacity_column(date_frame: pd.DataFrame) -> pd.DataFrame:
    '''Normalize the SSD_Capacity column'''
    logging.info("Normalizing SSD_Capacity_GB column")
    date_frame['SSD_Capacity_GB'] = date_frame['SSD_Capacity_GB'].apply(lambda x: re.sub(r'\D', '', str(x)))
    date_frame['SSD_Capacity_GB'] = pd.to_numeric(date_frame['SSD_Capacity_GB'], errors='coerce').astype('Int64')
    date_frame['SSD_Capacity_GB'] = date_frame['SSD_Capacity_GB'].apply(lambda x: x * 1024 if x < 10 else x)
    return date_frame

def normalize_BatteryCapacity_column(date_frame: pd.DataFrame) -> pd.DataFrame:
    '''Normalize the Battery_Capacity column'''
    logging.info("Normalizing Battery_Capacity_Wh column")
    date_frame['Battery_Capacity_Wh'] = pd.to_numeric(date_frame['Battery_Capacity_Wh'], errors='coerce')
    return date_frame

def normalize_Network_Cards_column(date_frame: pd.DataFrame) -> pd.DataFrame:
    '''Normalize and create Network_Cards_Wi-Fi and Network_Cards_Bluetooth_Version columns'''
    logging.info("Normalizing and creating Network_Cards_Wi-Fi and Network_Cards_Bluetooth_Version columns")
    wifi_pattern = r'(6E \(802\.11ax\)|6 \(802\.11ax\)|802\.11a|802\.11ax)'
    bluetooth_pattern = r'Bluetooth \d+\.\d+'

    for index, value in date_frame['Network_Cards_Wi-Fi'].items():
        if isinstance(value, str):
            wifi_matches = re.findall(wifi_pattern, value)
            bluetooth_matches = re.findall(bluetooth_pattern, value)
            wifi_result = f"Wi-Fi {wifi_matches[0]}" if wifi_matches else 'Wi-Fi Unknown'
            bluetooth_result = bluetooth_matches[0] if bluetooth_matches else 'Bluetooth Unknown'
            date_frame.at[index, 'Network_Cards_Wi-Fi'] = wifi_result
            date_frame.at[index, 'Network_Cards_Bluetooth_Version'] = bluetooth_result
        else:
            date_frame.at[index, 'Network_Cards_Wi-Fi'] = 'Wi-Fi Unknown'
            date_frame.at[index, 'Network_Cards_Bluetooth_Version'] = 'Bluetooth Unknown'
    
    return date_frame

def create_new_column_order(date_frame: pd.DataFrame) -> pd.DataFrame:
    '''Rearrange columns in the required order'''
    logging.info("Creating new column order")
    new_order = ['Name', 'Price_zl', 'Series', 'Screen_Diagonal_inches', 'Processor', 'Processor_Cores',
                 'RAM_Memory_GB', 'SSD_Capacity_GB', 'Graphics Card Manufacturer', 'Battery_Capacity_Wh',
                 'Network_Cards_Wi-Fi', 'Network_Cards_Bluetooth_Version', 'Short_Description']
    
    return date_frame[new_order]

def save_clean_data_to_csv(date_frame: pd.DataFrame, raw_data_file: str) -> None:
    '''Save cleaned data to a CSV file'''
    logging.info("Saving cleaned data to CSV")

    raw_file_name = raw_data_file.split('Raw_data/')[1].replace('.csv', '')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'./Processed_data/cleaned_{timestamp}_data_from_file_({raw_file_name}).csv'

    try:
        date_frame.to_csv(filename, sep=',', encoding='utf8', index=False)
        logging.info(f"----------Data successfully saved to file: {filename}")
    except Exception as e:
        logging.error(f"----------Error saving data to CSV: {e}")

def main() -> None:
    '''Bring each column of the table to its normalized form'''
    logging.info("----------Starting program")

    raw_data_file = './Raw_data/Raw_data_2024-10-15_12-16-17.csv'

    df = download_raw_data(raw_data_file)

    df = rename_columns(df, translation_dict)

    df = normalize_Seria_column(df)
    df = normalize_Price_column(df)
    df = normalize_ScreenDiagonal_column(df)
    df = normalize_Processor_column(df, processor_cores_dictionary)
    df = normalize_RamMemory_column(df)
    df = normalize_SSDcapacity_column(df)
    df = normalize_BatteryCapacity_column(df)
    df = normalize_Network_Cards_column(df)

    df = create_new_column_order(df)

    save_clean_data_to_csv(df, raw_data_file)

if __name__ == "__main__":
    main()
