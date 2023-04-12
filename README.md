![page_1](https://github.com/AlexandruNitulescu/nba_visualizer_py/blob/main/img/logo.png?raw=true)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://in-malmoe.streamlit.app/)
# NBA Visualizer
by Alexandru Nitulescu
## Abstract
NBA Visualizer is an example of the skills and techniques applied by a data analyst for data-driven decision making. The project follows the general principles of data analysis, starting with asking relevant questions to guide the exploration of data, and then focusing on preparing and processing the data. The project uses scraped data from NBA teams and their results during the 2022-23 seasons to demonstrate these principles.

The data preparation process involves various tasks, including manipulating columns, changing data types, ensuring data integrity, and optimizing tables. The project uses an Entity Relationship (ER) diagram to visualize the structure of the database and applies normalization techniques to minimize redundancy and improve efficiency.

Through this project, the goal is to provide an understanding of the data analysis process, including how to work with larger projects. The project showcases the principles of data analysis in action and serves as a portfolio piece for data analysts seeking to demonstrate their proficiency in these areas.

## Showcase

## Introduction
This project serves as a showcase of my skills in programming with Python, SQL and Power BI, specifically in the areas of database management, data analysis, and data visualization. The goal of this project is to create a reusable and effective project solution that can be applied to various data-driven tasks, such as creating dynamic dashboards and visualizations.

The project consists of three notebooks: prepare.ipynb, process.ipynb, and database.ipynb. The prepare.ipynb notebook focuses on analyzing the data needed to answer specific questions, and using web scraping techniques to retrieve the required data from www.nba.com.

The process.ipynb notebook focuses on cleaning and manipulating the data using Python's pandas library, creating an entity-relationship diagram (ERD) to visualize the relationships between tables, and normalizing the database to minimize redundancy and optimize querying.

The database.ipynb notebook focuses on creating various databases in SQLite, MySQL Workbench, and ElephantSQL, establishing proper database relationships, providing examples of SQL queries, and creating data visualizations using Python's matplotlib library.

Overall, this project demonstrates my ability to derive insights from complex data, design efficient database structures, and create effective data visualizations. These skills make me a strong candidate for roles as a data analyst or scientist, and showcase my ability to create reusable and effective project solutions for various data-driven tasks.


## Data Processing
The data was prepared for analysis using various techniques in Python, such as data type conversion, column splitting, creation of calculated columns, and merging of datasets. These tasks were accomplished efficiently using the pandas library.

## Database Management
The processed data was stored in a database created using SQLite, with a database schema designed to optimize querying and management. Established database design practices were followed, such as normalization to minimize redundancy, establishment of relationships between tables for efficient joining, indexing key columns to speed up queries, and selection of appropriate data types to minimize storage space.

## SQL
The purpose of the SQL section is to showcase some sample SQL queries that can be used to extract insights from the stored data in the database. These queries will demonstrate the power and versatility of SQL in analyzing large and complex datasets, and will serve as examples of how analysts can extract meaningful insights from data through the use of SQL.

## Data Visualisations
Data visualizations play a crucial role in communicating insights and patterns discovered in the data. In this section, we utilize various Python visualization libraries such as Matplotlib, Seaborn, and Plotly to create informative and visually appealing charts, graphs, and other visualizations. These visualizations are designed to effectively communicate insights to stakeholders, such as management or clients, in a clear and concise manner. The selection of visualization types and techniques used will depend on the nature of the data and the intended audience. Our goal is to present the data in an intuitive way that highlights important patterns and relationships, making it easy for viewers to extract valuable insights.

## Dynamic Dashboard
In addition to the data analysis and database management, this project showcases the benefits of using Power BI/web apps to create dynamic and interactive dashboards.
Using Power BI, we can transform the analysis and visualizations created earlier in this project into a dynamic dashboard that is easy to interact with and provides real-time updates as new data becomes available. This dashboard can be shared with others to provide insights and support decision-making.

Overall, using Power BI/web apps to create dynamic dashboards enhances the value of the data analysis and database management work done earlier in the project, and makes it easier to communicate insights to stakeholders.

## Repository structure
```
├── data
│   ├── game_dates.csv        <- CSV file containing dates of NBA games
│   ├── match_info.csv        <- CSV file containing general information about NBA games
│   ├── match_stats.csv       <- CSV file containing detailed stats for each NBA game
│   ├── raw_data.csv          <- CSV file containing raw data collected for NBA games
│   ├── team_info.csv         <- CSV file containing information about NBA teams
│
│
├── modules
│   ├── helper_functions.py   <- Python module containing helper functions used in modeling the Streamlit web app
│
│
├── database.ipynb            <- Step 3: Notebook showcasing the code interaction with a SQLite database
│
│
├── main.py                   <- Python script containing the main script for Streamlit web app
│
│
├── nba.db                    <- SQLite database containing the NBA data
│
│
├── prepare.py                <- Step 1: Notebook showcasing the prepare phase
│
│
├── process.py                <- Step 2: Notebook showcasing the data processing
│
│
├── README.md                 <- This README file
│
│
├── requirements.txt          <- Text file containing a list of all the dependencies with their respective version
│
│
├── team_dashboard.pbix       <- Power BI report containing visualizations of the NBA data
```

## Conclusion
NBA visualizer serves as a testament to the effectiveness of a well-designed data analysis pipeline, from data collection to visualization, and the benefits of utilizing modern tools to create reusable and dynamic solutions. As a data analyst or scientist, this project showcases the ability to tackle complex data challenges and create effective data-driven solutions.

## Contacts
- **Web app** - 
- **Documentation (in progress)** - 
- **Bug reports:** - 

- [LinkedIn](https://www.linkedin.com/in/alexandru-nitulescu-035778153/)
- [GitHub](https://github.com/AlexandruNitulescu)
- [Kaggle](https://www.kaggle.com/anitulescu)