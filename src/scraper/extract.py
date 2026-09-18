import os
import time
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
    os.makedirs(RAW_DIR, exist_ok=True)

    urls_file = os.path.join(RAW_DIR, "movie_urls.csv")
    output_file = os.path.join(RAW_DIR, "movies_raw.json")

    # ==========================================
    # 1. Extract movie URLs
    # ==========================================
    print("Starting URL extraction...")
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    
    url = "https://www.imdb.com/list/ls540701301/"
    driver.get(url)
    time.sleep(15)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    movie_links = soup.find_all("a", href=lambda x: x and "/title/tt" in x)
    movie_urls = []

    for link in movie_links:
        href = link.get("href")
        movie_url = "https://www.imdb.com" + href.split("?")[0]
        movie_urls.append(movie_url)

    movie_urls = list(dict.fromkeys(movie_urls))
    print(f"Movies found: {len(movie_urls)}")

    df = pd.DataFrame({"url": movie_urls})
    df.to_csv(urls_file, index=False, encoding="utf-8-sig")
    driver.quit()

    # ==========================================
    # 2. Extract detailed movie data
    # ==========================================
    print("Starting movie details extraction...")
    chrome_options = Options()
    chrome_options.add_argument("--autoplay-policy=document-user-activation-required")
    prefs = {        
        "profile.managed_default_content_settings.media_stream": 2,  
        "profile.default_content_setting_values.notifications": 2,   
        "profile.managed_default_content_settings.plugins": 2       
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)

    def scrape_movie(movie_url):
        try:
            driver.get(movie_url)
            time.sleep(10)
            html = driver.page_source
            soup = BeautifulSoup(html , "html.parser")
            
            movie_title_elem = soup.find("h1")
            movie_title = movie_title_elem.get_text(strip=True) if movie_title_elem else None

            movie_year_elem = soup.find("a", href=lambda x: x and "/releaseinfo/" in x)
            movie_year = movie_year_elem.get_text(strip=True) if movie_year_elem else None

            movie_rate_elem = soup.find("div", {"data-testid":"hero-rating-bar__aggregate-rating__score"})
            movie_rate = movie_rate_elem.get_text(strip=True) if movie_rate_elem else None

            vote_count_box = soup.find("div", {"data-testid":"hero-rating-bar__aggregate-rating__score"})
            vote_count = None
            if vote_count_box and vote_count_box.find_next_sibling("div") and vote_count_box.find_next_sibling("div").find_next_sibling("div"):
                vote_count = vote_count_box.find_next_sibling("div").find_next_sibling("div").get_text(strip=True)
            
            script_tag = soup.find("script", type="application/ld+json")
            genres = [] 
            if script_tag:
                movie_data = json.loads(script_tag.string)
                genres = movie_data.get("genre", [])
                if isinstance(genres, str):
                    genres = [genres]

            runtime_minutes = None
            try:
                for li in soup.find_all('li', class_='ipc-inline-list__item'):
                    text = li.get_text(strip=True)
                    match = re.match(r'^(?:(\d+)h)?\s*(?:(\d+)m)?$', text, re.IGNORECASE)
                    if match and (match.group(1) or match.group(2)):
                        hours = int(match.group(1)) if match.group(1) else 0
                        minutes = int(match.group(2)) if match.group(2) else 0
                        runtime_minutes = (hours * 60) + minutes
                        break 
            except Exception:
                pass

            director_elem = soup.find("a", href=lambda x: x and "ref_=tt_cst_1_1" in x)
            director = director_elem.get_text(strip=True) if director_elem else None

            actors_elems = soup.find_all("a", {"data-testid":"title-cast-item__actor"})
            actors = [actor.get_text(strip=True) for actor in actors_elems]

            return {
                "Title": movie_title,
                "Year": movie_year,
                "Rating": movie_rate,
                "Votes": vote_count,
                "Genres": genres,
                "Runtime_minutes": runtime_minutes,
                "Director": director,
                "Actors": actors
            }
        except Exception as e:
            print(f"Error scraping {movie_url}: {e}")
            return None

    urls = pd.read_csv(urls_file)
    
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as file:
            movies = json.load(file)
            print(f"Loaded {len(movies)} existing movies from JSON.")
    else:
        movies = []
        print("No existing JSON found. Starting fresh.")

    scraped_urls = {movie["URL"] for movie in movies if "URL" in movie}
    total_urls = len(urls)

    for index, current_url in enumerate(urls["url"], start=1):
        if current_url in scraped_urls:
            print(f"[{index}/{total_urls}] Skipping already scraped movie: {current_url}")
            continue

        print(f"[{index}/{total_urls}] Scraping: {current_url}")
        movie_data = scrape_movie(current_url)

        if movie_data:
            movie_data["URL"] = current_url
            movies.append(movie_data)
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(movies, file, ensure_ascii=False, indent=4)
            print(f"Saved | Total scraped: {len(movies)}")
        else:
            print("Failed")

    driver.quit()
    print("Extraction completed successfully.")

if __name__ == "__main__":
    main()