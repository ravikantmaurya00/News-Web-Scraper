# news_scraper.py
# -----------------------------------------------------------
# Task 3: Web Scraper for News Headlines (Multi-Website Version)
# Objective: Scrape top headlines from multiple famous websites
# Tools: Python, requests, BeautifulSoup
# -----------------------------------------------------------

import requests
from bs4 import BeautifulSoup

# 🌐 List of multiple popular news websites
NEWS_SITES = {
    "BBC News": "https://www.bbc.com/news",
    "NDTV": "https://www.ndtv.com/latest",
    "Hindustan Times": "https://www.hindustantimes.com/latest-news",
    "The Times of India": "https://timesofindia.indiatimes.com/home/headlines",
    "CNN": "https://edition.cnn.com/world"
}

def fetch_headlines(url):
    """Fetch headlines from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if site not reachable
        soup = BeautifulSoup(response.text, "html.parser")

        # Try multiple headline tags since sites differ in structure
        headlines = []
        for tag in ['h1', 'h2', 'h3']:
            for h in soup.find_all(tag):
                text = h.get_text(strip=True)
                if text and len(text.split()) > 3:  # Skip very short items
                    headlines.append(text)

        # Remove duplicates using set
        return list(set(headlines))

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching from {url}: {e}")
        return []

def save_to_file(all_headlines, filename="headlines.txt"):
    """Save all scraped headlines into a single text file."""
    with open(filename, "w", encoding="utf-8") as file:
        for site, headlines in all_headlines.items():
            file.write(f"\n{'='*70}\n{site} Headlines\n{'='*70}\n")
            for i, headline in enumerate(headlines, start=1):
                file.write(f"{i}. {headline}\n")
    print(f"\n✅ Headlines from {len(all_headlines)} websites saved to {filename}")

def main():
    """Main driver function."""
    all_headlines = {}
    print("📡 Fetching top headlines from multiple news websites...")

    for site_name, url in NEWS_SITES.items():
        print(f"\n🔹 Scraping {site_name}...")
        headlines = fetch_headlines(url)
        if headlines:
            all_headlines[site_name] = headlines[:10]  # Save only top 10
            for h in headlines[:5]:
                print("•", h)
        else:
            print("⚠️ No headlines found for", site_name)

    save_to_file(all_headlines)

if __name__ == "__main__":
    main()
