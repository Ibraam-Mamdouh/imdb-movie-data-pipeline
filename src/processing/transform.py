import pandas as pd
import json
import os

def main():
    print("Starting Data Transformation...")
    
    # 1. Read raw data
    df = pd.read_json("../../data/raw/movies_raw.json")

    # 2. Clean basic data
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df["Rating"] = df["Rating"].str.replace("/10", "", regex=False).astype(float)
    df["Runtime_minutes"] = pd.to_numeric(
        df["Runtime_minutes"].astype(str).str.replace(" min", "", regex=False), 
        errors="coerce"
    ).astype("Int64")

    def convert_votes(value):
        if pd.isna(value):
            return None
        value = str(value).strip().upper()
        if value.endswith("M"):
            return int(float(value[:-1]) * 1_000_000)
        if value.endswith("K"):
            return int(float(value[:-1]) * 1_000)
        return int(float(value))

    df["Votes"] = df["Votes"].apply(convert_votes).astype("Int64")
    df["Title"] = df["Title"].str.strip()
    df["Director"] = df["Director"].str.strip()

    # Ensure the processed directory exists
    os.makedirs("../../data/processed", exist_ok=True)

    # ==========================================
    # 3. Build relational tables (Data Modeling)
    # ==========================================
    
    # Base movies table (Movies Table)
    movies_df = df[["Title", "Year", "Rating", "Votes", "Runtime_minutes", "Director"]].copy()
    movies_df.insert(0, "movie_id", range(1, len(movies_df) + 1))

    # Genres lookup table
    genres_df = df[["Title", "Genres"]].explode("Genres")
    genres_df = genres_df.rename(columns={"Title": "movie_title", "Genres": "genre"})
    genres_df = genres_df.drop_duplicates().reset_index(drop=True)
    genres_df = genres_df.merge(movies_df[["movie_id", "Title"]], left_on="movie_title", right_on="Title", how="left")
    
    genre_lookup = genres_df[["genre"]].drop_duplicates().sort_values("genre").reset_index(drop=True)
    genre_lookup.insert(0, "genre_id", range(1, len(genre_lookup) + 1))

    # Movie genres mapping table (Movie Genres Fact)
    movie_genres_df = genres_df.merge(genre_lookup, on="genre", how="left")
    movie_genres_df = movie_genres_df[["movie_id", "genre_id"]].drop_duplicates()

    # Actors lookup table
    actors_df = df[["Title", "Actors"]].explode("Actors")
    actors_df = actors_df.rename(columns={"Title": "movie_title", "Actors": "actor"}).drop_duplicates()
    actors_df = actors_df.merge(movies_df[["movie_id", "Title"]], left_on="movie_title", right_on="Title", how="left")

    actor_lookup = actors_df[["actor"]].drop_duplicates().sort_values("actor").reset_index(drop=True)
    actor_lookup.insert(0, "actor_id", range(1, len(actor_lookup) + 1))

    # Movie actors mapping table (Movie Actors Fact)
    movie_actors_df = actors_df.merge(actor_lookup, on="actor", how="left")
    movie_actors_df = movie_actors_df[["movie_id", "actor_id"]].drop_duplicates()

    # Directors lookup table
    directors_df = df[["Title","Director"]].copy()
    directors_df = directors_df.rename(columns={"Title": "movie_title","Director": "director"})
    directors_df = directors_df.drop_duplicates()
    directors_df = directors_df.merge(movies_df[["movie_id", "Title"]],left_on="movie_title",right_on="Title",how="left")
    directors_df = directors_df[["movie_id", "director"]]
    director_lookup = (directors_df[["director"]].drop_duplicates().sort_values("director").reset_index(drop=True))
    director_lookup.insert(0,"director_id",range(1, len(director_lookup) + 1))

    movies_df = movies_df.merge(
    director_lookup,
    left_on="Director",
    right_on="director",
    how="left"
)
    movies_df = movies_df.drop(columns=["Director"])

    movies_df = movies_df[
        [
            "movie_id",
            "director_id",
            "Title",
            "Year",
            "Rating",
            "Votes",
            "Runtime_minutes"
        ]
    ]

    # ==========================================
    # 4. Export tables to Parquet format and csv
    # ==========================================
    print("Saving modeled tables to Parquet formats and csv...")
    
    # Save the full consolidated dataframe as a reference
    # Movies
    movies_df.to_csv(
        "../../data/processed/movies.csv",
        index=False,
        encoding="utf-8-sig"
    )

    movies_df.to_parquet(
        "../../data/processed/movies.parquet",
        index=False
    )


    # Directors
    director_lookup.to_csv(
        "../../data/processed/directors.csv",
        index=False,
        encoding="utf-8-sig"
    )

    director_lookup.to_parquet(
        "../../data/processed/directors.parquet",
        index=False
    )


    # Actors
    actor_lookup.to_csv(
        "../../data/processed/actors.csv",
        index=False,
        encoding="utf-8-sig"
    )

    actor_lookup.to_parquet(
        "../../data/processed/actors.parquet",
        index=False
    )


    # Genres
    genre_lookup.to_csv(
        "../../data/processed/genres.csv",
        index=False,
        encoding="utf-8-sig"
    )

    genre_lookup.to_parquet(
        "../../data/processed/genres.parquet",
        index=False
    )


    # Movie Actors
    movie_actors_df.to_csv(
        "../../data/processed/movie_actors.csv",
        index=False,
        encoding="utf-8-sig"
    )

    movie_actors_df.to_parquet(
        "../../data/processed/movie_actors.parquet",
        index=False
    )


    # Movie Genres
    movie_genres_df.to_csv(
        "../../data/processed/movie_genres.csv",
        index=False,
        encoding="utf-8-sig"
    )

    movie_genres_df.to_parquet(
        "../../data/processed/movie_genres.parquet",
        index=False
    )

    print("Transformation completed and DataFrames successfully saved as .parquet and csv files.")

if __name__ == "__main__":
    main()