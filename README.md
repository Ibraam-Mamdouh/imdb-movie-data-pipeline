# IMDb Movie Intelligence

A web scraping and data engineering project that collects movie data from IMDb, processes and normalizes the data using Python, and loads it into a relational SQL Server database for exploration and future AI/ML applications.

## Project Overview

The project builds an end-to-end data pipeline:

IMDb Movie List
→ Selenium + BeautifulSoup
→ Raw JSON
→ Pandas Data Processing
→ Data Normalization
→ CSV / Parquet
→ SQL Server
→ Data Exploration

## Features

- Automated movie URL extraction using Selenium
- Web scraping with Selenium and BeautifulSoup
- Extraction of:
  - Movie title
  - Release year
  - IMDb rating
  - Vote count
  - Genres
  - Runtime
  - Director
  - Cast
- Data cleaning and type conversion using Pandas
- Normalization of movie, actor, genre, and director data
- Relational database design with primary and foreign keys
- SQL Server data loading
- Data quality validation
- Exploratory analysis using Pandas and SQL

## Architecture

```text
IMDb Movie List
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
       ┌──────┼──────────┐
       ▼      ▼          ▼
    Movies  Actors    Genres
       │
       ├── Movie_Actors
       └── Movie_Genres
              │
              ▼
       SQL / Pandas
       Exploration
