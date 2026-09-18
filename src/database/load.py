import os
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

def main():
    print("Starting Data Load...")
    
    # 1. Define paths and read the processed Parquet files
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

    movies_df = pd.read_parquet(os.path.join(PROCESSED_DIR, "movies.parquet"))
    director_lookup = pd.read_parquet(os.path.join(PROCESSED_DIR, "directors.parquet"))
    genre_lookup = pd.read_parquet(os.path.join(PROCESSED_DIR, "genres.parquet"))
    actor_lookup = pd.read_parquet(os.path.join(PROCESSED_DIR, "actors.parquet"))
    movie_genres_df = pd.read_parquet(os.path.join(PROCESSED_DIR, "movie_genres.parquet"))
    movie_actors_df = pd.read_parquet(os.path.join(PROCESSED_DIR, "movie_actors.parquet"))

    # 2. Standardize column names to match the database tables (SQL Schema) exactly
    director_lookup = director_lookup.rename(columns={'director_id': 'director_id', 'director': 'dir_name'})
    genre_lookup = genre_lookup.rename(columns={'genre_id': 'genre_id', 'genre': 'gen_name'})
    actor_lookup = actor_lookup.rename(columns={'actor_id': 'actor_id', 'actor': 'act_name'})

    movies_df = movies_df.rename(columns={
        'movie_id': 'movie_id', 
        'director_id': 'director_id',
        'Title': 'title', 
        'Year': 'movie_year', 
        'Rating': 'rating', 
        'Votes': 'votes',
        'Runtime_minutes': 'runtime_minutes'
    })

    movie_genres_df = movie_genres_df.rename(columns={'movie_id': 'movie_id', 'genre_id': 'genre_id'})
    movie_actors_df = movie_actors_df.rename(columns={'movie_id': 'movie_id', 'actor_id': 'actor_id'})

    # 3. Setup database connection (Microsoft SQL Server)
    server = r'DESKTOP-BVMNIQD\MSSQLSERVEREXPRE' 
    database = 'movie_intelligence_db'

    params = urllib.parse.quote_plus(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
    )
    engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

    # 4. Upload data while respecting Foreign Key constraints within a single transaction
    try:
        with engine.begin() as conn:
            print("Uploading Directors...")
            director_lookup[['director_id', 'dir_name']].to_sql('Directors', con=conn, if_exists='append', index=False)
            
            print("Uploading Genres...")
            genre_lookup[['genre_id', 'gen_name']].to_sql('Genres', con=conn, if_exists='append', index=False)
            
            print("Uploading Actors...")
            actor_lookup[['actor_id', 'act_name']].to_sql('Actors', con=conn, if_exists='append', index=False)
            
            print("Uploading Movies...")
            movies_df[['movie_id', 'director_id', 'title', 'movie_year', 'rating', 'votes', 'runtime_minutes']].to_sql(
                'Movies', con=conn, if_exists='append', index=False
            )
            
            print("Uploading Movie_Genres...")
            movie_genres_df[['movie_id', 'genre_id']].to_sql('Movie_Genres', con=conn, if_exists='append', index=False)
            
            print("Uploading Movie_Actors...")
            movie_actors_df[['movie_id', 'actor_id']].to_sql('Movie_Actors', con=conn, if_exists='append', index=False)

        print("✅ All data successfully uploaded to the database!")

    except Exception as e:
        print(f"❌ An error occurred during upload: {e}")

if __name__ == "__main__":
    main()