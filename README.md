# IMDb Movie Intelligence

An end-to-end web scraping and data engineering pipeline that collects movie data from IMDb, transforms and normalizes the extracted data, and loads it into a relational SQL Server database for exploration and future AI/ML applications.

## Project Overview

**IMDb Movie Intelligence** is a self-initiated data engineering project built to practice the complete data pipeline lifecycle — from automated web data extraction to a structured relational database.

The project uses **Selenium and BeautifulSoup** to collect movie information from IMDb, **Pandas** for data cleaning and transformation, and **SQL Server** for structured storage and querying.

The pipeline was designed with a modular architecture so that each stage of the process can be developed, validated, and maintained independently.

### Pipeline

```text
IMDb
  │
  ▼
Selenium
  │
  ▼
Movie URLs
  │
  ▼
Selenium + BeautifulSoup
  │
  ▼
Raw JSON
  │
  ▼
Pandas
  │
  ├── Cleaning
  ├── Transformation
  └── Normalization
  │
  ▼
CSV / Parquet
  │
  ▼
SQL Server
  │
  ▼
Relational Database
  │
  ▼
SQL + Pandas Exploration
```

## Features

### Data Extraction

* Automated movie URL extraction using Selenium
* Web scraping using Selenium and BeautifulSoup
* Extraction of movie-level information including:

  * Movie title
  * Release year
  * IMDb rating
  * Vote count
  * Runtime
  * Genres
  * Director
  * Cast

### Data Processing

* Data cleaning and transformation using Pandas
* Data type conversion and standardization
* Handling nested movie attributes
* Separation of many-to-many relationships
* Data normalization into relational entities
* Export to CSV and Parquet formats

### Database Engineering

The processed data is loaded into a relational SQL Server database designed around normalized entities:

```text
Movies
├── Movie_Actors ─── Actors
├── Movie_Genres ─── Genres
└── Movie_Directors ─── Directors
```

The database uses:

* Primary keys
* Foreign keys
* Relationship tables
* Normalized entities
* Referential relationships between movies and related entities

### Data Quality

The pipeline includes validation checks to verify:

* Missing values
* Duplicate records
* Invalid data types
* Invalid relationships
* Referential integrity
* Consistency between normalized tables

## Architecture

```text
                         ┌─────────────────┐
                         │      IMDb       │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Selenium     │
                         │ Movie URL Scrape│
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Movie URLs    │
                         └────────┬────────┘
                                  │
                                  ▼
                   ┌──────────────────────────┐
                   │ Selenium + BeautifulSoup │
                   │     Data Extraction      │
                   └────────────┬─────────────┘
                                │
                                ▼
                         ┌─────────────────┐
                         │     Raw JSON    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     Pandas      │
                         │ Cleaning & ETL  │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
                 Cleaning    Transformation  Normalization
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  CSV / Parquet  │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    SQL Server   │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
          Movies              Actors              Genres
              │
       ┌──────┴────────┐
       ▼               ▼
 Movie_Actors    Movie_Directors
       │               │
       ▼               ▼
     Actors         Directors
```

## Database Schema

The final database separates movie attributes and relationships into normalized tables.

### Main Entities

**Movies**

Stores movie-level information such as title, release year, rating, vote count, and runtime.

**Actors**

Stores unique actors extracted from movie cast information.

**Directors**

Stores unique directors associated with movies.

**Genres**

Stores unique movie genres.

### Relationship Tables

**Movie_Actors**

Connects movies with their actors through a many-to-many relationship.

**Movie_Directors**

Connects movies with their directors.

**Movie_Genres**

Connects movies with their genres.

This structure reduces data duplication and makes the dataset easier to query and extend.

## Project Structure

```text
imdb-movie-data-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── imdb_movie_exploration.ipynb
│
├── sql/
│   ├── database_schema.sql
│   └── queries.sql
│
├── src/
│   ├── scraper/
│   ├── transformation/
│   ├── database/
│   └── main.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Tech Stack

| Technology       | Purpose                             |
| ---------------- | ----------------------------------- |
| Python           | Pipeline development                |
| Selenium         | Browser automation and web scraping |
| BeautifulSoup    | HTML parsing                        |
| Pandas           | Data cleaning and transformation    |
| SQL Server       | Relational data storage             |
| SQL              | Database querying and validation    |
| CSV              | Intermediate data storage           |
| Parquet          | Efficient processed-data storage    |
| Jupyter Notebook | Data exploration and validation     |
| Git / GitHub     | Version control                     |

## ETL Workflow

### 1. Extract

Selenium is used to navigate IMDb and collect movie URLs.

The movie pages are then processed using Selenium and BeautifulSoup to extract structured movie information.

The extracted records are initially stored as raw JSON data.

### 2. Transform

Pandas is used to transform the raw data into structured datasets.

The transformation stage includes:

* Cleaning raw fields
* Standardizing data types
* Extracting nested information
* Removing unnecessary duplication
* Separating entities
* Building relationship datasets
* Preparing the data for relational storage

Processed datasets are exported as CSV and Parquet files.

### 3. Load

The transformed datasets are loaded into SQL Server.

The database follows a normalized relational structure with primary and foreign key relationships between the tables.

### 4. Validate & Explore

The final database is validated using SQL queries and explored using Pandas and Jupyter Notebook.

The notebook focuses on:

* Data quality checks
* Dataset structure
* Basic exploration
* SQL-based validation
* Relationships between normalized entities

## Data Quality Validation

Before loading the final datasets, validation checks are performed to ensure that the processed data is suitable for relational storage.

Examples include:

```text
Missing values
Duplicate records
Invalid data types
Duplicate entities
Invalid foreign-key relationships
Inconsistent movie relationships
```

These checks help ensure that the final database is structured and reliable for downstream use.

## Future AI/ML Applications

The project was intentionally designed as a data foundation that can later support machine learning workflows.

Potential future applications include:

* Movie recommendation systems
* Rating prediction
* Genre classification
* Similarity-based movie search
* Movie feature engineering
* Exploratory machine learning on movie attributes

The current project focuses on **data engineering and data preparation**, while the AI/ML layer can be developed separately once the dataset is ready.

## Getting Started

### Prerequisites

Make sure you have:

* Python 3.x
* Google Chrome
* ChromeDriver compatible with your Chrome version
* Microsoft SQL Server
* SQL Server Management Studio (SSMS)

### Installation

Clone the repository:

```bash
git clone https://github.com/Ibraam-Mamdouh/imdb-movie-data-pipeline.git
```

Navigate to the project directory:

```bash
cd imdb-movie-data-pipeline
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Database Setup

1. Create the required database in SQL Server.
2. Run the SQL scripts inside the `sql/` directory.
3. Configure the database connection used by the pipeline.
4. Run the extraction and transformation pipeline.
5. Load the processed datasets into SQL Server.

> The exact database connection settings should be configured locally and should not be committed to the repository.

## Disclaimer

This project is intended for educational and portfolio purposes.

IMDb and its content belong to their respective owners. The project demonstrates web scraping, data engineering, data modeling, and database processing techniques.

## Author

**Ibraam Mamdouh**

Data Engineering | AI & ML

[GitHub](https://github.com/Ibraam-Mamdouh)
