import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def preprocess_data(data):
    """
    Функція для очищення даних від записів без ціни.
    
    Аргументи:
    data (pd.DataFrame): DataFrame з інформацією про ноутбуки, де є стовпці 'RAM_Memory_GB' та 'Price_zl'.
    
    Повертає:
    pd.DataFrame: Очищений DataFrame без записів з відсутніми цінами.
    """
    # Видалення записів з відсутніми значеннями ціни (NaN)
    cleaned_data = data.dropna(subset=['Price_zl'])
    return cleaned_data

    """
    Функція будує графік залежності середньої ціни ноутбуків від кількості оперативної пам'яті.
    
    Аргументи:
    data (pd.DataFrame): DataFrame з інформацією про ноутбуки, де є стовпці 'RAM_Memory_GB' та 'Price_zl'.
    """
    # Групування ноутбуків за кількістю RAM та обчислення середньої ціни
    grouped_data = data.groupby('RAM_Memory_GB').agg({'Price_zl': 'mean'}).reset_index()

    # Побудова графіка з точками, але без з'єднання
    plt.figure(figsize=(10, 6))
    
    # Графік без ліній між точками
    plt.scatter(grouped_data['RAM_Memory_GB'], grouped_data['Price_zl'], color='blue', marker='o', label='Середня ціна (злотих)')
    
    # Налаштування осей
    plt.xticks(grouped_data['RAM_Memory_GB'])  # Показуємо унікальні значення RAM на осі X
    plt.xlabel('Кількість оперативної пам\'яті (GB)')
    plt.ylabel('Середня ціна (злотих)')
    plt.title('Залежність середньої ціни ноутбуків від кількості оперативної пам\'яті')
    plt.grid(True)
    plt.legend()

    # Вимикаємо наукову нотацію для осі Y
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.gca().yaxis.get_major_formatter().set_scientific(False)
    
    # Збереження графіка в PDF
    graph_output_file = '/Users/KrisMur/Desktop/PetProjekt1/Skraping_projekt/Processed_data/avg_price_vs_ram_graph.pdf'
    plt.tight_layout()  # Для кращого відображення графіка без обрізання міток
    plt.savefig(graph_output_file, format='pdf')
    print(f"Графік збережено як: {graph_output_file}")
    
    plt.show()

def plot_correlation_and_trend(data):
    """
    Функція будує графік із трендовою лінією та обчислює кореляцію між середньою ціною ноутбуків та кількістю оперативної пам'яті.
    
    Аргументи:
    data (pd.DataFrame): DataFrame з інформацією про ноутбуки, де є стовпці 'RAM_Memory_GB' та 'Price_zl'.
    
    Повертає:
    float: Кореляція між RAM та середньою ціною.
    """
    # Групування ноутбуків за кількістю RAM та обчислення середньої ціни
    grouped_data = data.groupby('RAM_Memory_GB').agg({'Price_zl': 'mean'}).reset_index()
    
    # Обчислення кореляції між кількістю RAM та середньою ціною
    correlation = grouped_data['RAM_Memory_GB'].corr(grouped_data['Price_zl'])
    print(f"Кореляція між кількістю оперативної пам'яті та середньою ціною: {correlation:.2f}")
    
    # Побудова графіка з точками та трендовою лінією
    plt.figure(figsize=(10, 6))
    
    # Графік з точками
    plt.scatter(grouped_data['RAM_Memory_GB'], grouped_data['Price_zl'], color='blue', marker='o', label='Середня ціна (злотих)')
    
    # Додавання трендової лінії
    z = np.polyfit(grouped_data['RAM_Memory_GB'], grouped_data['Price_zl'], 1)
    p = np.poly1d(z)
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
    graph_output_file = '/Users/KrisMur/Desktop/PetProjekt1/Skraping_projekt/Processed_data/ram_price_correlation_graph.pdf'
    plt.tight_layout()  # Для кращого відображення графіка без обрізання міток
    plt.savefig(graph_output_file, format='pdf')
    print(f"Графік збережено як: {graph_output_file}")
    
    plt.show()
    
    return correlation

# Приклад використання функцій
file_path = '/Users/KrisMur/Desktop/PetProjekt1/Skraping_projekt/Processed_data/cleaned_2024-10-16_13-46-10_data_from_file_(Raw_data_2024-10-15_12-16-17).csv'
data = pd.read_csv(file_path)

# Очищення даних від записів без ціни
cleaned_data = preprocess_data(data)


# Виклик другої функції для обчислення кореляції та побудови графіка з трендовою лінією
plot_correlation_and_trend(cleaned_data)
