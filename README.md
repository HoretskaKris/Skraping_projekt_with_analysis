Data Processing and Scraping Project
This repository contains Python scripts for data scraping, cleaning, and visualization of product data. The project focuses on gathering laptop data from an e-commerce site, normalizing the dataset, and visualizing key correlations and statistics.

Project Structure
1. Data Scraping
The scraping.py script is responsible for collecting data from a specified e-commerce website. The data includes product details such as name, price, and technical specifications (e.g., processor, RAM, SSD capacity).

Key functionality includes:

Connecting to web pages to retrieve product information.
Extracting product details like title, price, and specification links.
Saving the collected data into a CSV file for further processing.
2. Data Cleaning
The data_cleaning.py script normalizes the raw scraped data to make it ready for analysis. Key cleaning operations include:

Removing unnecessary spaces in the data.
Renaming columns to English from other languages for easier use.
Normalizing numerical values (e.g., prices, RAM size, screen size).
Handling missing values and invalid entries.
3. Data Visualization
The visualization.py script provides visual analysis of the cleaned data, focusing on key correlations like:

Correlation between RAM size and average price of laptops.
Distribution of laptops by processor type.
It generates charts, including scatter plots with trend lines and donut charts, which are saved as PDF files.

Requirements
To run the project, you need to install the following Python packages:

bash
Copy code
pip install pandas numpy matplotlib requests beautifulsoup4 lxml
Usage
1. Scraping Data
To scrape data from the e-commerce site, run the scraping.py script:

bash
Copy code
python scraping.py
This will collect product details and save them in a CSV file located in the ./Raw_data directory.

2. Cleaning Data
After scraping, you can clean and normalize the data using the data_cleaning.py script:

bash
Copy code
python data_cleaning.py
This will rename columns, remove unnecessary characters, and save the cleaned data into the ./Processed_data directory.

3. Visualizing Data
Once the data is cleaned, use the visualization.py script to generate visualizations of the key metrics:

bash
Copy code
python visualization.py
This will generate and save visualizations like the correlation between RAM size and price, or the distribution of processors in the ./Visualization_of_analysis directory.

Logging
All scripts log their operations, such as successful connections, data retrieval, and errors, into log files located in the logs directory. Key log files include:

scraping_log.log: Logs related to data scraping.
cleaning_data_log.log: Logs for the data cleaning process.
visualization_log.log: Logs for the visualization script.
File Structure
bash
Copy code
├── Raw_data/
│   └── Raw_data_<timestamp>.csv       # Raw product data from the scraping process
├── Processed_data/
│   └── cleaned_<timestamp>_data.csv   # Cleaned and normalized data
├── Visualization_of_analysis/
│   └── *.pdf                          # Generated graphs and visualizations
├── logs/
│   ├── scraping_log.log               # Logs for the scraping script
│   ├── cleaning_data_log.log          # Logs for the cleaning script
│   └── visualization_log.log          # Logs for the visualization script
├── scraping.py                        # Script for scraping product data
├── data_cleaning.py                   # Script for cleaning and normalizing data
├── visualization.py                   # Script for visualizing data
└── README.md                          # This README file
Future Improvements
Additional data analysis: Add more analysis of product features, such as battery life, display type, etc.
Automated updates: Integrate scheduled scraping to collect up-to-date product data.
Better error handling: Improve error management in the scraping and data processing scripts.
License
This project is licensed under the MIT License.

