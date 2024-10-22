import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import logging
from typing import Optional

logging.basicConfig(
    filename='./logs/visualization_log.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    level=logging.INFO
)

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    logging.info(f"Loading data from file: {file_path}")
    try:
        data: pd.DataFrame = pd.read_csv(file_path)
        logging.info(f"Data successfully loaded. Number of rows: {len(data)}")
        return data
    except Exception as e:
        logging.error(f"Error loading data from file {file_path}: {e}")
        exit(f"Error: {e}. Program exiting.")

def get_plot_correlation_and_trend(data: pd.DataFrame) -> None:
    logging.info("Starting correlation plot between RAM and price.")

    data = data.dropna(subset=['Price_zl'])
    logging.info(f"Number of laptops after data cleaning: {len(data)}.")

    grouped_data = data.groupby('RAM_Memory_GB').agg({'Price_zl': 'mean'}).reset_index()

    correlation: Optional[float] = grouped_data['RAM_Memory_GB'].corr(grouped_data['Price_zl'])
    logging.info(f"Correlation between RAM and average price: {correlation:.2f}")
    
    plt.figure(figsize=(10, 6))
    
    plt.scatter(grouped_data['RAM_Memory_GB'], grouped_data['Price_zl'], color='blue', marker='o', label='Average Price (PLN)')
    
    z: np.ndarray = np.polyfit(grouped_data['RAM_Memory_GB'], grouped_data['Price_zl'], 1)
    p: np.poly1d = np.poly1d(z)
    plt.plot(grouped_data['RAM_Memory_GB'], p(grouped_data['RAM_Memory_GB']), "r--", label='Trendline')

    plt.xticks(grouped_data['RAM_Memory_GB'])
    plt.xlabel('RAM (GB)')
    plt.ylabel('Average Price (PLN)')
    plt.title('RAM vs Average Price with Trendline')
    plt.grid(True)
    plt.legend()

    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.gca().yaxis.get_major_formatter().set_scientific(False)
    
    graph_output_file: str = './Visualization_of_analysis/ram_price_correlation_graph.pdf'
    plt.tight_layout()
    plt.savefig(graph_output_file, format='pdf')
    logging.info(f"Correlation graph saved as: {graph_output_file}")

    plt.show(block=False)

def get_plot_processor_distribution(data: pd.DataFrame) -> None:
    logging.info("Starting donut chart for processor distribution.")
  
    processor_group: pd.DataFrame = data.groupby('Processor').size().reset_index(name='Count')
    logging.info(f"Number of different processor types: {len(processor_group)}.")
    
    plt.figure(figsize=(8, 8))
    plt.pie(processor_group['Count'], labels=processor_group['Processor'], autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.3))
    plt.title('Processor Distribution')

    graph_output_file: str = './Visualization_of_analysis/plot_processor_distribution.pdf'
    plt.tight_layout()
    plt.savefig(graph_output_file, format='pdf')
    logging.info(f"Donut chart for processors saved as: {graph_output_file}")

    plt.show()

def main() -> None:
    logging.info("-------- Program start ")
    file_path: str = './Processed_data/cleaned_2024-10-18_17-55-11_data_from_file_(Raw_data_2024-10-15_12-16-17).csv'

    data = load_data(file_path)

    get_plot_correlation_and_trend(data)
    get_plot_processor_distribution(data)
    logging.info("-------- Program end ")

if __name__ == "__main__":
    main()
