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
    """Функція для завантаження даних з файлу CSV."""
    logging.info(f"Завантаження даних з файлу: {file_path}")
    try:
        data: pd.DataFrame = pd.read_csv(file_path)
        logging.info(f"Дані успішно завантажені. Кількість рядків: {len(data)}")
        return data
    except Exception as e:
        logging.error(f"Помилка під час завантаження даних з файлу {file_path}: {e}")
        exit(f"Помилка: {e}. Завершення програми.")

def get_plot_correlation_and_trend(data: pd.DataFrame) -> None:
    """Функція будує графік із трендовою лінією та обчислює кореляцію між середньою ціною ноутбуків та кількістю оперативної пам'яті."""

    logging.info("Початок побудови графіка кореляції між кількістю RAM та ціною.")

    # Очищення даних від записів без ціни
    data = data.dropna(subset=['Price_zl'])
    logging.info(f"Кількість ноутбуків після очищення даних: {len(data)}.")

    # Групування ноутбуків за кількістю RAM та обчислення середньої ціни
    grouped_data = data.groupby('RAM_Memory_GB').agg({'Price_zl': 'mean'}).reset_index()

    # Обчислення кореляції між кількістю RAM та середньою ціною
    correlation: Optional[float] = grouped_data['RAM_Memory_GB'].corr(grouped_data['Price_zl'])
    logging.info(f"Кореляція між кількістю оперативної пам'яті та середньою ціною: {correlation:.2f}")
    
    # Побудова графіка з точками та трендовою лінією
    plt.figure(figsize=(10, 6))
    
    # Графік з точками
    plt.scatter(grouped_data['RAM_Memory_GB'], grouped_data['Price_zl'], color='blue', marker='o', label='Середня ціна (злотих)')
    
    # Додавання трендової лінії
    z: np.ndarray = np.polyfit(grouped_data['RAM_Memory_GB'], grouped_data['Price_zl'], 1)
    p: np.poly1d = np.poly1d(z)
    plt.plot(grouped_data['RAM_Memory_GB'], p(grouped_data['RAM_Memory_GB']), "r--", label='Трендова лінія')

    # Налаштування осей
    plt.xticks(grouped_data['RAM_Memory_GB'])  # Показуємо унікальні значення RAM на осі X
    plt.xlabel('Кількість оперативної пам\'яті (GB)')
    plt.ylabel('Середня ціна (злотих)')
    plt.title('Залежність середньої ціни ноутбуків від кількості оперативної пам\'яті з трендовою лінією')
    plt.grid(True)
    plt.legend()

    # Вимикаємо наукову нотацію для осі Y
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.gca().yaxis.get_major_formatter().set_scientific(False)
    
    # Збереження графіка в PDF
    graph_output_file: str = './Visualization_of_analysis/ram_price_correlation_graph.pdf'
    plt.tight_layout()  # Для кращого відображення графіка без обрізання міток
    plt.savefig(graph_output_file, format='pdf')
    logging.info(f"Графік кореляції RAM та ціни збережено як: {graph_output_file}")

    plt.show(block=False)

def get_plot_processor_distribution(data: pd.DataFrame) -> None:
    """Функція для групування ноутбуків за процесорами, підрахунку їх кількості та побудови бубликового графіка розподілу."""
    logging.info("Початок побудови бубликового графіка розподілу процесорів.")
  
    # Групування ноутбуків за процесором і підрахунок кількості
    processor_group: pd.DataFrame = data.groupby('Processor').size().reset_index(name='Count')
    logging.info(f"Кількість різних типів процесорів: {len(processor_group)}.")
    
    # Візуалізація: побудова бубликового графіка
    plt.figure(figsize=(8, 8))  # Розмір графіка
    plt.pie(processor_group['Count'], labels=processor_group['Processor'], autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.3))
    plt.title('Розподіл ноутбуків за процесорами')

    # Збереження графіка в PDF
    graph_output_file: str = './Visualization_of_analysis/plot_processor_distribution.pdf'
    plt.tight_layout()  # Для кращого відображення графіка без обрізання міток
    plt.savefig(graph_output_file, format='pdf')
    logging.info(f"Бубликовий графік процесорів збережено як: {graph_output_file}")

    # Відображення графіка
    plt.show()

def main() -> None:
    logging.info("-------- Старт програми ")
    file_path: str = './Processed_data/cleaned_2024-10-18_17-55-11_data_from_file_(Raw_data_2024-10-15_12-16-17).csv'

    data = load_data(file_path)

    get_plot_correlation_and_trend(data)
    get_plot_processor_distribution(data)
    logging.info("-------- Завершення програми ")


if __name__ == "__main__":
    main()